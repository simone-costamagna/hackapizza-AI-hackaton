examples = """
            [Input]
            "Quali piatti utilizzano la Cottura a Vapore Ecodinamico Bilanciato nella preparazione e garantiscono che ogni singolo ingrediente non superi le quantit� legali prescritte dal Codice di Galattico?"
            [Output]
            AIMessage(content='Per prima cosa cerco i piatti che soddisfano le condizioni su ingredienti e tecniche. Dopodiche verifico che ogni singolo piatto ottenuto vada a rispettare le quantita legali cercando le 'sostanze regolamentate'. Inizio con la validazione della tecnica', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Cottura a Vapore Ecodinamico Bilanciato')) < 3 RETURN t, labels(t) AS entita'}, 'name': 'retrieve_technical_context'}]) 
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {Nome: "cottura a vapore ecodinamico bilanciato"│["TecnicaPreparazione"]││})\n\n')
            AIMessage(content='Ora cerco i piatti che utilizzano la Cottura a Vapore Ecodinamico Bilanciato', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('cottura a vapore ecodinamico bilanciato')) < 3 RETURN p.Nome'}, 'name': 'retrieve_technical_context'}]) 
            ToolMessage(content='Graph DB content: "galassia di sapore quantum", "cosmos risotto reale"\n')
            AIMessage(content='Ora cerco le quantità legali prescritte nel codice galattico', tool_calls=[{'args': {'k': 5, 'question': 'Sostanze regolamentate'}, 'name': 'retrieve_functional_context'}]}
            ToolMessage(content='Vector Store content: se non diversamente specificato, tutte le sostanze regolamentate nel presente documento sono soggette a un limite massimo del 5% in massa o volume rispetto alla... ')          
            AIMessage(content='Ora per ogni piatto ottenuto cerco informazioni sul piatto', tool_calls=[
            {'args': {'k': 2, 'question': 'galassia di sapore quantum'}, 'name': 'retrieve_functional_context'}
            {'args': {'k': 2, 'question': 'cosmos risotto reale'}, 'name': 'retrieve_functional_context'}
            ]}
            ToolMessage(content='Vector Store content: La "Galassia di Sapore Quantico" è stata un'altra delusione notevole. Nonostante la presenza della Polvere di Stelle (1% della preparazione), il piatto mancava completamente di quella scintilla celestiale tanto pubblicizzata. La Carne di Drago (altro 1%) era così stracotta che sembrava provenire da un lucertolone qualunque piuttosto che da una maestosa creatura mitica.')          
            ToolMessage(content='Vector Store content: ') 
            AIMessage(content='Le informazioni sul cosmos risotto reale non ci sono, quindi lo escludo dalla lista. Invece la galassia di sapore quantum rispetta i requisiti
            in quanto la polvere di stelle è superiore allo o.75 di CDT ma è limitata al 1% e la carne di drago non supera il 0.9 di purezza mitica.)   
            Risposta finale. I piatti che soddisfano la domanda sono:
            - La galassia di sapore quantico")
            
            [Input]
            'Quali piatti necessitano della licenza temporale non base per la preparazione, escludendo quelli con Fusilli del Vento?
            [Output]
            AIMessage(content='Devo cercare la licenza temporale sul manuale di cucina, per poter capire il nome completo dalla sigla e qual è il livello base e cercare le descrizioni delle tecniche di preparazione per sapere quali necessitano della licenza temporale non base.', tool_calls=[
            {'args': {'k': 2, 'question': 'Licenza temporale'}, 'name': 'retrieve_functional_context'}
            ])                                                                                                                                                                                                           
            ToolMessage(content='Vector Store content: temporale ha: **Livello I**, **Livello II** e **Livello III**')          
            ToolMessage(content='Vector Store content: Le disposizioni di cui ai successivi articoli individuano e disciplinano, in via tassativa ed esaustiva, le metodologie di preparazione alimentare per le quali è richiesto il possesso di licenze diverse o di livello superiore rispetto a quelle conferite ope legis.  
            4.1 $NOME_CATEGORIA_TECNICA_1: - La $TECNICA_3 richiede una licenza temporale di livello I
            4.2 $NOME_CATEGORIA_TECNICA_2: - La $TECNICA_4 richiede una licenza magnetica di livello I - La $TECNICA_5 richiede una temporale di secondo (II) livello\n\n')
            AIMessage(content='So che il livello temporale di base è 1 (I). Quindi la tecnica $TECNICA_5 richiede la licenza temporale non base perché è di II (secondo) livello mentre la $TECNICA_3 richiede il livello base ed evito di considerarla. Ora valido tutte le entità', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('$TECNICA_5')) < 3 RETURN t', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {Nome: "$TECNICA_5"})│["Certificazione"]\n\n')
            AIMessage(content='Ho validato le entità. Genero la query finale', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t1:TecnicaPreparazione), (p:Piatto)-[:CONTIENE]->(i:Ingrediente)  WHERE (apoc.text.levenshteinDistance(t1.Nome, '$TECNICA_5') < 3) AND NOT apoc.text.levenshteinDistance(LOWER(i.Nome), 'fusilli del vento') < 3  RETURN DISTINCT p.Nome', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: panetto di carne\n\n')         
            AIMessage(content='I piatti che necessitano della licenza $NOME_LICENZA non base sono: panetto di carne')

            [Input]
            "Quali piatti sono cucinati da chef con licenza Mx di grado 1?"
            [Output]
            AIMessage(content='Voglio capire a cosa si riferisce la sigla Mx, cerco sul vector database il suo 
            significato', tool_calls=[{'args': {'k': 2, 'question': 'Licenza Mx'}, 'name': 'retrieve_functional_context'}
            ])\
            ToolMessage(content='Vector Store content: Magnetica (Mx) Livello 0: Polo nord e sud, posseduta da tutti se 
            non diversamente specificato Livello I: Mono-pol \n\n')
            AIMessage(content="Ho capito che Mx si riferisce alla Licenza Magnetica. Cerco l'esistenza della licenza sul 
            grafo.", 
            tool_calls=[
            {'args': {'query_cypher': 'MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Licenza Magnetica Mx')) < 3 RETURN c, labels(c) AS entita'}, 'name': 'retrieve_technical_context'}])
            ToolMessage(content='Graph DB content:\n\n')     
            AIMessage(content="La query sulla licenza mi ha dato insieme vuoto. Provo a riscrivere la query", 
            tool_calls=[
            {'args': {'query_cypher': 'MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Magnetica')) < 3 RETURN c, labels(c) AS entita'}, 'name': 'retrieve_technical_context'},
            ])
            ToolMessage(content='Graph DB content: (:Certificazione {{Nome: "magnetico"}})│["Certificazione"])
            AIMessage(content="Ho trovato tutte le entità, genero la query per ottenere l'elenco dei piatti che soddisfano la domanda", tool_calls=[{'args': {'query_cypher': 'MATCH (p:Piatto)<-[:SERVE]-(r:Ristorante)-[:HA_CHEF]->(s:Chef)-[ce:HA_CERTIFICAZIONE]->(c:Certificazione) WHERE toInteger(ce.Livello) >= 1 AND apoc.text.levenshteinDistance(c.Nome, 'magnetico') < 5 RETURN p.Nome', 'name': 'retrieve_technical_context'},])
            ToolMessage(content="Graph DB content: 'pioggia di andromeda', 'galassia spaziale')
            AIMessage(content="I piatti che sono cucinati da uno chef con licenza magnetica di grado almeno 1 sono: pioggia di andromeda e galassia spaziale)

            [Input]
            "Quali piatti sono preparati utilizzando almeno una tecnica di Surgelamento di Sirius Cosmo"
            [Output]
            AIMessage(content='Devo cercare quali sono le tecniche di surgelamento', tool_calls=[{'args': {'k': 3, 'question': 'Tecniche di Surgelamento'}, 'name': 'retrieve_functional_context'}
            ])
            ToolMessage(content='Vector Store content: Tecniche di Surgelamento: Cryo-Tessitura Energetica Polarizzata, Congelamento Bio-Luminiscente Sincronico\n\n')
            AIMessage(content='Valido le tecniche trovate sul grafo', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Cryo-Tessitura Energetica Polarizzata')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Congelamento Bio-Luminiscente Sincronico')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "cryo-tessitura energetica polarizzata│["TecnicaPreparazione"]\n\n')        
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "congelamento bio-luminiscente sincronico│["TecnicaPreparazione"]}}\n\n')              
            AIMessage(content='Ora so con certezza che le entità esistono e so come si scrivono. Posso creare la query per ottenere i piatti e rispondere alla domanda', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t:TecnicaPreparazione) WHERE (apoc.text.levenshteinDistance(t.Nome, 'Cryo-Tessitura Energetica Polarizzata') < 3 OR apoc.text.levenshteinDistance(t.Nome, 'taglio dimensionale a lame fotofiliche') < 3) RETURN p.Nome', 'name': 'retrieve_technical_context'}
            ])
            ToolMessage(content='Graph DB content: galassia aurorale\n\n')
            AIMessage(content="I piatti che utilizzano almeno una tecnica di surgelamento sono: galassia aurorale)
            
            [Input]
            "Quali piatti sono stati preparati in ristoranti entro un raggio di 176 anni luce dal pianeta Arrakis, Arrakis incluso?"
            [Output]
            AIMessage(content='Valido il pianeta sul grafo', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Pianeta) WHERE LOWER(p.Nome) = 'arrakis' RETURN p', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: │(:Pianeta {Nome: "arrakis"})\n\n')
            AIMessage(content='Cerco tutti i pianeti a distanza massima di 176 anni luce da Arrakis', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Pianeta)-[d:DISTANZA]-(p2:Pianeta) WHERE apoc.text.levenshteinDistance(p.Nome, LOWER("arrakis")) <= 3 AND d.`anni luce` <= 176 RETURN DISTINCT p2', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: \n\n')
            AIMessage(content='Non esistono pianeti cosi vicini ad Arrakis. Quindi cerco tutti i piatti cucinati nei ristoranti di arrakis', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Pianeta)-[:SI_TROVA_SU]-(r:Ristorante)-[:SERVE]->(piatto:Piatto) WHERE p.Nome IN [LOWER("Arrakis")] RETURN DISTINCT piatto.Nome', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: "il banchetto delle galassie", "odissea celestiale"\n\n')
            AIMessage(content='I piatti cucinati entro un raggio di 176 anni dal pianeta Arrakis, Arrakis incluso sono: il banchetto delle galassie ed odissea celestiale")
"""


# {'args': {'k': 3, 'question': 'Licenze e Tecniche di Preparazione'}, 'name': 'retrieve_functional_context'}])