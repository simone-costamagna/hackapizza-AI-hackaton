examples = """
            [Input]\n
            "Quali piatti sono cucinati da chef con licenza Mx di grado 1 e che contengono Erba Pipa?"\n 
            [Behavior]\n
            AIMessage(content='Voglio capire a cosa si riferisce la sigla Mx, cerco sul vector database il suo 
            significato', tool_calls=[{'args': {'k': 3, 'question': 'Licenza Mx'}, 'name': 'retrieve_functional_context'}
            ])\n 
            ToolMessage(content='Vector Store content: Magnetica (Mx) Livello 0: Polo nord e sud, posseduta da tutti se 
            non diversamente specificato Livello I: Mono-pol \n\n')
            AIMessage(content="Ho capito che Mx si riferisce alla Licenza Magnetica. Cerco l'esistenza della licenza sul 
            grafo. Inoltre ipotizzo che 'Erba Pipa' sia un ingrediente. Cerco di validare il nome e l'ipotesi", 
            tool_calls=[
            {'args': {'query_cypher': 'MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Licenza Magnetica Mx')) < 3 RETURN c, labels(c) AS entita'}, 'name': 'retrieve_technical_context'},
            {'args': {'query_cypher': 'MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('erba pipa')) < 3 RETURN i, labels(i) AS entita'}, 'name': 'retrieve_technical_context'},
            ])
            ToolMessage(content='Graph DB content:\n\n')
            ToolMessage(content='Graph DB content: (:Ingrediente {{Provenienza: "unknown",Nome: "erba pipa"}})│["Ingrediente"]\n\n')        
            AIMessage(content="Ho individuato l'ingrediente ma la query sulla licenza mi ha dato insieme vuoto. Provo a
            riscrivere la query", 
            tool_calls=[
            {'args': {'query_cypher': 'MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Magnetica')) < 3 RETURN c, labels(c) AS entita'}, 'name': 'retrieve_technical_context'},
            ])
            ToolMessage(content='Graph DB content: (:Certificazione {{Nome: "magnetico"}})│["Certificazione"])
            AIMessage(content="Ho trovato tutte le entità, genero la query per ottenere l'elenco dei piatti che soddisfano
            la domanda", 
            tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)<-[:SERVE]-(r:Ristorante)-[:HA_CHEF]->(s:Chef)-[ce:HA_CERTIFICAZIONE]->(c:Certificazione) WHERE ce.Livello = '1' AND apoc.text.levenshteinDistance(c.Nome, 'magnetico') < 5 MATCH (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'erba pipa') < 5  RETURN p.Nome', 'name': 'retrieve_technical_context'},
            ])
            ToolMessage(content="Graph DB content: 'pioggia di andromeda', 'galassia spaziale')
            AIMessage(content="I piatti che hanno l'erba pipa e sono cucinati con licenza magnetica di grado almeno 1 sono: pioggia di andromeda e galassia spaziale)
"""



"""
            [Input]
            "Quali piatti sono cucinati da chef con licenza Mx di grado 1 e che contengono Erba Pipa?"
            [Behavior]
            1. Ricerca su Vector db tool. Domanda: 'Licenza Mx'; k: 3. Risposta: Magnetica (Mx). Livello 0: Polo nord e sud, posseduta da tutti se non diversamente specificato. Livello I: Mono-polo. Intuizione: capisco che tutti gli chef hanno la licenza magentica di livello 0 anche se non specificato. Io però sto cercando di livello 1.
            2. Ricerca su Graph db tool. Domanda: MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Licenza Magnetica di livello 1')) < 3 RETURN c, labels(c) AS entita. Risposta: []. Intuizione: la licenza non si chiama 'Licenza Magnetica di livello 0' sul grafo.
            3. Ricerca su Graph db too. Domanda: MATCH (c:Certificazione) RETURN c.Nome. Risposta: magnetico │ psionica │ temporale │ gravitazionale │ antimateria │ quantistica │ luce │ ltk. Intuizione: conosco il nome di tutte le licenze possibili. Capisco che quella che cerco si chiama 'magnetico'.
            4. Ricerca su Graph db tool. Domanda: MATCH (c:Certificazione) WHERE apoc.text.levenshteinDistance(c.Nome, LOWER('Magnetico')) < 3 RETURN c, labels(c) AS entita. Risposta: (:Certificazione {{Nome: "magnetico"}})│["Certificazione"]. Intuizione: ho trovato la certificazione.
            4. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('erba pipa')) < 3 RETURN i, labels(i) AS entita. Risposta: (:Ingrediente {{Provenienza: "unknown",Nome: "erba pipa"}})│["Ingrediente"]. Intuizione: esiste l'ingrediente 'Erba Pipa'.
            5. Ricerca su Graph db tool. Domanda: MATCH (p:Piatto)<-[:SERVE]-(r:Ristorante)-[:HA_CHEF]->(s:Chef)-[ce:HA_CERTIFICAZIONE]->(c:Certificazione) WHERE ce.Livello = '1' AND apoc.text.levenshteinDistance(c.Nome, 'magnetico') < 5 MATCH (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'erba pipa') < 5  RETURN p.Nome. Risposta: 'pioggia di andromenda', 'galassia spaziale'. Intuizione: lavoro completato.
            [Output]
            Piatto 1: 'pioggia di andromenda'
            Piatto 2: 'galassia spaziale'
            ...
            
            [Input]
            'Quali piatti della galassia posso preparare che combinano la Carne di Balena spaziale, l'Essenza di Tachioni e le Uova di Fenice?'
            [Behavior]
            1. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('carne di balena')) < 3 RETURN i, labels(i) AS entita. Risposta: []. Intuizione: l'ingrediente non si scrive 'carne di balena'.
            2. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('carne di balena spaziale')) < 5 RETURN i, labels(i) AS entita. Risposta: (:Ingrediente {{Provenienza: "unknown",Nome: "carne di balena spaziale"}})│["Ingrediente"]. Intuizione: ingrediente trovato. 
            3. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('essenza di tachioni')) < 3 RETURN i, labels(i) AS entita. Risposta: (:Ingrediente {{Provenienza: "unknown",Nome: "essenza di tachioni"}})│["Ingrediente"]. Intuizione: ingrediente trovato.
            4. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('uova di fenice')) < 3 RETURN i, labels(i) AS entita. Risposta: (:Ingrediente {{Provenienza: "unknown",Nome: "uova di fenice"}})│["Ingrediente"]││(:Ingrediente {{Provenienza: "unknown",Nome: "uovo di fenice"}})│["Ingrediente"]. Intuizione: ingrediente trovato.
            5. Ricerca su Graph db tool. Domanda: MATCH (p:Piatto)-[:CONTIENE]->(i1:Ingrediente), (p)-[:CONTIENE]->(i2:Ingrediente), (p)-[:CONTIENE]->(i3:Ingrediente) WHERE apoc.text.levenshteinDistance(i1.Nome, 'foglie di nebulosa') < 3 AND apoc.text.levenshteinDistance(i2.Nome, 'amido di stellarion') < 3 AND apoc.text.levenshteinDistance(i3.Nome, 'uova di fenice') < 3  RETURN p.Nome. Risposta: []. Intuzione: devo riscrivere la query.
            6. Ricerca su Graph db tool. Domanda: MATCH (p:Piatto)-[:CONTIENE]->(i1:Ingrediente), (p)-[:CONTIENE]->(i2:Ingrediente), (p)-[:CONTIENE]->(i3:Ingrediente) WHERE apoc.text.levenshteinDistance(i1.Nome, 'foglie di nebulosa') < 3 AND apoc.text.levenshteinDistance(i2.Nome, 'amido di stellarion') < 3 AND apoc.text.levenshteinDistance(i3.Nome, 'uovo di fenice') < 3  RETURN p.Nome. Risposta: "galassia aurorale". Intuzione: lavoro completato.
            [Output]
            Piatto 1: 'galassia aurorale'
            ...
            
            [Input]
            "Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento del di Sirius Cosmo"
            [Behavior]
            1. Ragionamento: non sono specificate tecniche o licenze specifiche. Devo cercare sul vector db le 'tecniche di surgelamento' esistenti. Ricerca: Vector db tool. Domanda: 'Tecniche di Surgelamento'; k: 8. Risposta: Nel cosmo, il surgelamento non è solo un metodo di conservazione, ma una tecnica che sfrutta ecc. Intuizione: le tecniche di surgelamento esistenti sono: Cryo-Tessitura Energetica Polarizzata, Congelamento Bio-Luminiscente Sincronico ecc.
            2. Ricerca su Graph db tool. Domanda: MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('Cryo-Tessitura Energetica Polarizzata')) < 3 RETURN t, labels(t) AS entita. Risposta: (:TecnicaPreparazione {{Nome: "congelamento bio-luminiscente sincronico│["TecnicaPreparazione"]}}. Intuizione: tecnica trovato.
            3. Ricerca su Graph db tool. Domanda: MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('Congelamento Bio-Luminiscente Sincronico')) < 3 RETURN t, labels(t) AS entita. Risposta: (:TecnicaPreparazione {{Nome: "congelamento bio-luminiscente sincronico│["TecnicaPreparazione"]}}. Intuizione: tecnica trovata.
            4. Ricerca su Graph db tool. Domanda: MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('spaghi del sole')) < 3 RETURN i, labels(i) AS entita. Risposta: (:Ingrediente {{Provenienza: "unknown",Nome: "carne di balena spaziale"}}) . Intuizione: ingrediente trovato. 
            5. Ricerca su Graph db tool. Domanda: MATCH (p:Piatto)-[:PREPARATO_CON]->(t:TecnicaPreparazione), (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'spaghi del sole') < 3 AND (apoc.text.levenshteinDistance(t.Nome, 'Cryo-Tessitura Energetica Polarizzata') < 3 OR apoc.text.levenshteinDistance(t.Nome, 'taglio dimensionale a lame fotofiliche') < 3) RETURN p.Nome. Risposta: "hamburgher di soia". Intuzione: lavoro completato.
            [Output]
            Piatto 1: 'hamburger di soia'
            ...
"""