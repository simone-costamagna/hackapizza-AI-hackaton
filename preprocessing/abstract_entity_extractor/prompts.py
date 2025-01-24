from langchain_core.prompts import ChatPromptTemplate

ABSTRACT_JSON_TEMPLATE = {
    "ProgettoRicerca": {
    "Titolo": "string",
    "AreaDiRicerca": "string",
    "Responsabile": "string",
    "DataInizio": "date",
    "DataFine": "date|null"
    },
    "Collaborazioni": [
    {
      "Organizzazione": "string",
      "Ruolo": "string"
    }
    ],
    "Pubblicazioni": [
    {
      "Titolo": "string",
      "Anno": "integer"
    }
    ],
    "Finanziamenti": [
    {
      "Ente": "string",
      "Importo": "float"
    }
    ]
}

PROMPT_EXTRACT_ENTITY_I = ChatPromptTemplate([
    ("system", """Il tuo compito è generare un template JSON astratto che possa organizzare le informazioni presenti 
                nel documento fornito, adattandolo al contesto specifico. Considera che i concetti di 'Skill', 'Certificazione' e
                'Licenza' devono essere trattati come equivalenti sotto un'unica categoria astratta.\n
                Specifiche dell'output:\n
                Il template JSON deve essere strutturato in modo chiaro e flessibile. Accanto ad ogni concetto astratto deve essere 
                indicato il tipo (stringa, intero, ecc).\n
                Mantieni l'output in italiano.\n
                Assicurati che il risultato sia adatto a una vasta gamma di documenti con contenuti variabili.\n\n
                Contesto: {contesto}
                """),
    ("human", "Documento: {documento}.\n"
              "L'output deve essere il template JSON astratto basato sul documento fornito e rispettando il contesto "
              "sopra descritto."),
])

PROMPT_EXTRACT_ENTITY = ChatPromptTemplate([
    ("system", """Il tuo compito è generare un template JSON astratto che rappresenti i concetti chiave di un ristorante, adattandolo 
    al contesto specifico.\n
    Specifiche dell'output:\n
    - Il template JSON deve essere chiaro, flessibile e indicare il tipo di ogni concetto (stringa, intero, ecc.).\n
    - L'output deve essere scritto in italiano.\n
    - Il risultato deve adattarsi a documenti simili con contenuti variabili.\n
    - Il template non deve contenere concetti che non riguardano il contesto del ristorante\n
    - I concetti astratti devono essere semplici, chiari ed intuitivi.\n\n
    
    Esempio di un json astratto referente ad un altro contesto:
    {abstract_json_template}
    
    Contesto: {contesto}"""),
    ("human", "Documento: {documento}.\n"
              "Genera il template JSON astratto basato sul documento fornito, rispettando il contesto sopra descritto."),
])

PROMPT_JSON_TEMPLATES_I = ChatPromptTemplate([
    ("system", """Sei un assistente esperto nella progettazione di template json astratti.\n"
    "Riceverai in input una serie di template astratti.\n"
    "Il tuo compito è:\n"
    "- Analizzare i template forniti.\n"
    "- Identificare i concetti e gli attributi più comuni.\n"
    "- Normalizzare i nomi dei concetti e degli attributi.\n"
    "- Unificare i concetti con significati simili per evitare duplicati.\n"
    "Genera un template json finale coerente, ottimizzato e intuitivo."""),
    ("human", "Templates: {json_templates}.\n"
              "Genera il template JSON astratto basato sui template forniti."),
])

PROMPT_JSON_TEMPLATES_II = ChatPromptTemplate([
    ("system", """Sei un assistente specializzato nella sintesi e ottimizzazione di template JSON.\n"
    "Riceverai in input una lista di template JSON. Il tuo compito è:\n"
    "- Analizzare i template per identificare concetti e attributi rilevanti.\n"
    "- Eliminare ridondanze unificando concetti simili o duplicati.\n"
    "- Normalizzare i nomi di concetti e attributi per renderli più chiari e consistenti.\n"
    "- Astrarre i dettagli superflui, mantenendo un livello generale utile per la maggior parte dei casi d'uso.\n"
    "- Restituire un template JSON finale, semplice, coerente e ben organizzato."""),

    ("human", "Input templates: {json_templates}.\n"
              "Crea un template JSON astratto ottimizzato, basandoti sui template forniti."),
])

PROMPT_JSON_TEMPLATES = ChatPromptTemplate([
    ("system", """Sei un assistente specializzato nell'ottimizzazione e nella sintesi di template JSON.\n"
    "Il tuo compito è:\n"
    "- Analizzare i template forniti per identificare concetti simili o duplicati (es. 'Licenze', 'Certificazioni', 'Competenze').\n"
    "- Unificare i concetti simili in un unico concetto chiaro.\n"
    "- Normalizzare i nomi di attributi e concetti per garantirne la coerenza e leggibilità.\n"
    "- Rimuovere attributi e concetti troppo specifici, mantenendo solo i concetti e attributi più comuni e generici.\n"
    "- Importante: restituire un template JSON finale astratto e ottimizzato rappresentativo dei concetti che sono comuni in tutti i template forniti."""),

    ("human", "Input templates: {json_templates}.\n"
              "Unifica i template forniti e genera un JSON astratto, eliminando ridondanze e semplificando i concetti."),
])

PROMPT_CLEANER_TEMPLATE_I = ChatPromptTemplate([
    ("system", """"Sei un assistente esperto nella pulizia di json template.\n"
    "Il tuo compito è:\n"
    "- Identificare relazioni o nodi con significati simili e mantenerne solo uno.\n"
    "- Rilevare attributi duplicati e conservarne solo uno.\n"
    "- Garantire che ogni concetto sia espresso in un unico punto del template.\n"
    "Assicurati che il template finale sia coerente, ottimizzato e privo di ridondanze.\n
    Utilizza il contesto del progetto per aiutarti nel compito.\n\n
    Contesto: {contesto}
    "
    """),
    ("human", "Input templates: {json_templates}.\n"
              "Unifica i template forniti e genera un JSON astratto, eliminando ridondanze e semplificando i concetti."),
])

PROMPT_CLEANER_TEMPLATE = ChatPromptTemplate([
    ("system", """
    Dato un file JSON in input, puliscilo rimuovendo i concetti duplicati o ridondanti e produci un file JSON in output 
    più snello e ottimizzato, senza perdere informazioni essenziali.\n
    Segui queste regole:\n\n
    Elimina le sezioni o i campi che rappresentano concetti già presenti in altre parti del JSON.\n
    Mantieni una struttura coerente e leggibile, garantendo che il risultato rappresenti un template compatto.\n
    Se un dettaglio è troppo specifico o irrilevante per il contesto generale, rimuovilo per semplificare il file.\n
    Non modificare il significato dei campi rimanenti.\n
    Aiutati con il contesto del progetto:\n
    Contesto: {contesto}
    """),
    ("human", "Json da ottimizzare: {json_template}.\n"
              "Genera il json template ottimizzato:"),
])