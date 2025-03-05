import csv
import json
import logging
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_neo4j import Neo4jVector, Neo4jGraph
from neo4j import GraphDatabase
from tqdm import tqdm
from config import OUTPUT_KB_ENTITIES_FOLDER, OUTPUT_KB_GRAPH_SCHEMA
from knowledge_base.config import GRAPH_DB, TEMPLATE, EXAMPLE_PATH
from knowledge_base.graph_db.prompts import PROMPT_EXTRACT_ENTITY
from utils.wrapper import LLMWrapper, EmbeddingWrapper

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DB = os.getenv("NEO4J_DB")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

wrapper = LLMWrapper()
wrapper.activate_json_mode()

embeddingWrapper = EmbeddingWrapper()

runnable_get_json_templates = (
    PROMPT_EXTRACT_ENTITY | wrapper.llm | wrapper.parser
)


def replace_none(data):
    if isinstance(data, dict):
        return {key: replace_none(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_none(item) for item in data]
    elif data is None:
        return "unknown"
    else:
        return data


def extract_entity(status):
    """
    Extracts entities from documents based on a predefined JSON template.
    This function processes files categorized under GRAPH_DB, applying a template to extract structured entities.
    If a pre-existing extraction exists, it loads it; otherwise, it generates new entities and saves them.
    """
    logging.info(f"Extracting entities using json template")

    graph_db_entites = []

    template = status['files'][TEMPLATE][0][1]
    for file in tqdm(status['files'][GRAPH_DB], desc="Extracting json entities from files"):
        file_name = os.path.basename(file[0])

        if file_name != 'Distanze.csv':
            entity_json_file_path = os.path.join(OUTPUT_KB_ENTITIES_FOLDER, os.path.splitext(file_name)[0] + '.json')
            if os.path.exists(entity_json_file_path):
                with open(entity_json_file_path, 'r', encoding='utf-8') as json_file:
                    entities = json.load(json_file)
                    entities = replace_none(entities)
            else:
                try:
                    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
                        examples = f.read()
                except UnicodeDecodeError as ex:
                    with open(EXAMPLE_PATH, "r", encoding="ISO-8859-1") as f:
                        examples = f.read()

                input = {
                    "template": template,
                    "example": examples.replace("{", "{{").replace("}", "}}"),
                    "documento": file[1]
                }

                entities = runnable_get_json_templates.invoke(input)

                with open(entity_json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(entities, json_file, ensure_ascii=False, indent=4)

            graph_db_entites.append(entities)
        else:
            entity_json_file_path = os.path.join(OUTPUT_KB_ENTITIES_FOLDER, os.path.splitext(file_name)[0] + '.csv')
            with open(entity_json_file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(file[1])
                graph_db_entites.append(file[1])

    logging.info(f"Entities extracted.")

    return graph_db_entites


def get_delete_query():
    return ["MATCH (n) DETACH DELETE n;"]


def escape_single_quotes(value):
    """Escape single quotes for Cypher queries."""
    return value.replace("'", "\\'") if isinstance(value, str) else value


def generate_node_queries(data):
    queries = []

    if isinstance(data, dict):
        ristorante = data["Ristorante"]
        queries.append(
            f"MERGE (r:Ristorante {{Nome: '{escape_single_quotes(ristorante['Nome']).lower()}', "
            f"AnnoApertura: '{ristorante['AnnoApertura']}'}})"
        )

        queries.append(
            f"MERGE (p:Pianeta {{Nome: '{escape_single_quotes(ristorante['Pianeta']).lower()}'}})"
        )

        chef = ristorante["Chef"]
        queries.append(
            f"MERGE (c:Chef {{Nome: '{escape_single_quotes(chef['Nome']).lower()}', "
            f"Cognome: '{escape_single_quotes(chef['Cognome']).lower()}'}})"
        )

        for cert in chef["Certificazioni"]:
            queries.append(
                f"MERGE (cert:Certificazione {{Nome: '{escape_single_quotes(cert['Tipo']).lower()}'}})"
            )

        for piatto in ristorante["Menu"]:
            queries.append(
                f"MERGE (pi:Piatto {{Nome: '{escape_single_quotes(piatto['NomePiatto']).lower()}'}})"
            )

            for ingrediente in piatto["Ingredienti"]:
                queries.append(
                    f"MERGE (ing:Ingrediente {{Nome: '{escape_single_quotes(ingrediente['Nome']).lower()}',"
                    f"Provenienza: '{escape_single_quotes(ingrediente['Provenienza']).lower()}'}})"
                )

            for tecnica in piatto["TecnichePreparazione"]:
                queries.append(
                    f"MERGE (tec:TecnicaPreparazione {{Nome: '{escape_single_quotes(tecnica['Nome']).lower()}'}})"
                )
    else:
        for item in data[0][1:]:
            queries.append(
                f"MERGE (p:Pianeta {{Nome: '{escape_single_quotes(item).lower()}'}})"
            )

    return queries


def generate_relationship_queries(data):
    queries = []

    if isinstance(data, dict):
        ristorante = data["Ristorante"]
        queries.append(
            f"MATCH (r:Ristorante {{Nome: '{escape_single_quotes(ristorante['Nome']).lower()}'}}), "
            f"(p:Pianeta {{Nome: '{escape_single_quotes(ristorante['Pianeta']).lower()}'}}) "
            f"MERGE (r)-[:SI_TROVA_SU]->(p)"
        )

        chef = ristorante["Chef"]
        queries.append(
            f"MATCH (r:Ristorante {{Nome: '{escape_single_quotes(ristorante['Nome']).lower()}'}}), "
            f"(c:Chef {{Nome: '{escape_single_quotes(chef['Nome']).lower()}', "
            f"Cognome: '{escape_single_quotes(chef['Cognome']).lower()}'}}) "
            f"MERGE (r)-[:HA_CHEF]->(c)"
        )

        for cert in chef["Certificazioni"]:
            queries.append(
                f"MATCH (c:Chef {{Nome: '{escape_single_quotes(chef['Nome']).lower()}', "
                f"Cognome: '{escape_single_quotes(chef['Cognome']).lower()}'}}), "
                f"(cert:Certificazione {{Nome: '{escape_single_quotes(cert['Tipo']).lower()}'}}) "
                f"MERGE (c)-[:HA_CERTIFICAZIONE {{Livello: '{escape_single_quotes(cert['Livello'])}', "
                f"AnnoConseguimento: '{cert['AnnoConseguimento']}'}}]->(cert)"
            )

        for piatto in ristorante["Menu"]:
            queries.append(
                f"MATCH (r:Ristorante {{Nome: '{escape_single_quotes(ristorante['Nome']).lower()}'}}), "
                f"(pi:Piatto {{Nome: '{escape_single_quotes(piatto['NomePiatto']).lower()}'}}) "
                f"MERGE (r)-[:SERVE]->(pi)"
            )

            for ingrediente in piatto["Ingredienti"]:
                queries.append(
                    f"MATCH (pi:Piatto {{Nome: '{escape_single_quotes(piatto['NomePiatto']).lower()}'}}), "
                    f"(ing:Ingrediente {{Nome: '{escape_single_quotes(ingrediente['Nome']).lower()}'}}) "
                    f"MERGE (pi)-[:CONTIENE]->(ing)"
                )

            for tecnica in piatto["TecnichePreparazione"]:
                queries.append(
                    f"MATCH (pi:Piatto {{Nome: '{escape_single_quotes(piatto['NomePiatto']).lower()}'}}), "
                    f"(tec:TecnicaPreparazione {{Nome: '{escape_single_quotes(tecnica['Nome']).lower()}'}}) "
                    f"MERGE (pi)-[:PREPARATO_CON]->(tec)"
                )
    else:
        items = data[0][1:]

        for i in range(1, len(data)):
            source_planet = data[i][0]
            for j, distance in enumerate(data[i][1:]):
                target_planet = items[j]
                if source_planet != target_planet:
                    queries.append(
                        f"MATCH (p1:Pianeta {{Nome: '{escape_single_quotes(source_planet).lower()}'}}), "
                        f"(p2:Pianeta {{Nome: '{escape_single_quotes(target_planet).lower()}'}}) "
                        f"MERGE (p1)-[:DISTANZA {{anni luce: {distance}}}]->(p2)"
                    )

    return queries


def generate_queries(status):
    """
    Generates database queries deterministically based on extracted entities.
    This function creates delete, node, and relationship queries from the extracted entities.
    It ensures a structured and consistent approach to query generation for database operations.
    """
    logging.info("Generating queries started")

    entities = status['entities']
    delete_queries = get_delete_query()
    node_queries = []
    relationship_queries = []

    for data in tqdm(entities, desc="Generating queries"):
        node_queries.extend(generate_node_queries(data))
        relationship_queries.extend(generate_relationship_queries(data))

    queries = {
        'delete': delete_queries,
        'node': node_queries,
        'relationship': relationship_queries
    }

    logging.info("Queries generated")

    return queries


def execute_queries(status):
    """
    Executes generated queries in the Neo4j database.
    This function runs delete, node, and relationship queries sequentially
    using the Neo4j driver session to modify the database accordingly.
    """
    logging.info("Executing queries started")

    queries = status['queries']

    with neo4j_driver.session(database=NEO4J_DB) as session:
        for query in tqdm(queries['delete'], desc="Deleting queries"):
            session.run(query)

        for query in tqdm(queries['node'], desc="Node queries"):
            session.run(query)

        for query in tqdm(queries['relationship'], desc="Relationship queries"):
            session.run(query)

    logging.info("Executed queries")


def store_schema(status):
    """
    Stores the Neo4j database schema to a file.
    This function retrieves the current schema from the Neo4j database
    and saves it as a text file for future reference.
    """
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)
    graph.refresh_schema()
    schema = graph.schema

    file_path = os.path.join(OUTPUT_KB_GRAPH_SCHEMA, 'schema.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(schema if isinstance(schema, str) else str(schema))

    logging.info(f"Schema has been successfully stored")


graph_db = (
    RunnablePassthrough.assign(entities=extract_entity)
    | RunnablePassthrough.assign(queries=generate_queries)
    | RunnablePassthrough(execute_queries)
    | RunnablePassthrough(store_schema)
)