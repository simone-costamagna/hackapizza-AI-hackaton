""""
            [Input]\n
            'Quali piatti sono preparati con almeno una delle tecniche di taglio e necessitano della licenza t non base per la preparazione?\n
            [Output]\n
            AIMessage(content='Devo cercare quali sono le tecniche di taglio', tool_calls=[{'args': {'k': 3, 'question': 'Tecniche di Taglio'}, 'name': 'retrieve_functional_context'}
            ])\n 
            ToolMessage(content='Vector Store content: 1. Taglio dimensionale a lame fotofiliche; 2. Taglio a risonanza sonica rigenerativa\n\n')
            AIMessage(content='Ora voglio cercare la licenza t sul manuale di cucina, per poter capire il nome completo dalla sigla e qual è il livello base', tool_calls=[{'args': {'k': 3, 'question': 'Licenza Temporale'}, 'name': 'retrieve_functional_context'}
            ])
            ToolMessage(content='Vector Store content: Temporale (t) - **Livello I**: effetti temporali relativi al presente come dilatazione o accelerazione del tempo.
            - **Livello II**: Livello I + effetti temporali che riguardano linee temporali future.
            - **Livello III**: Livello II + effetti temporali che riguardano linee temporali passate.\n\n')          
            AIMessage(content='Ho capito che il livello base è 1. Ora voglio conoscere quali tecniche di preparazione necessitano della licenza t non base. Per farlo devo leggere la regolamentazione', tool_calls=[{'args': {'k': 3, 'question': 'Licenze e Tecniche di Preparazione - regolamentazione'}, 'name': 'retrieve_functional_context'}])\n 
            ToolMessage(content='Vector Store content: Le disposizioni di cui ai successivi articoli individuano e disciplinano, in via tassativa ed esaustiva, le metodologie di preparazione alimentare per le quali è richiesto il possesso di licenze diverse o di livello superiore rispetto a quelle conferite ope legis.  
            4.1 Marinatura: - La marinatura temporale sincronizzata richiede una licenza temporale (t) di livello I
            4.2 Affumicatura: - L’affumicatura a stratificazione quantica richiede una licenza quantistica (Q) di livello 3 - L’affumicatura temporale risonante richiede una licenza temporale (t) di secondo (II) livello\n\n')\n
            AIMessage(content='So che la tecnica 'affumicatura temporale risonante' richiede la licenza temporale non base. Ora valido tutte le entità', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('affumicatura temporale risonante')) < 3
            MATCH (t1:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t1.Nome, LOWER('taglio dimensionale a lame fotofiliche')) < 3
            MATCH (t2:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t2.Nome, LOWER('Taglio a risonanza sonica rigenerativa')) < 3
            RETURN t, t1, t2', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {Nome: "affumicatura temporale risonante"})│["Certificazione"], (:TecnicaPreparazione {Nome: "taglio dimensionale a lame fotofiliche"}, (:TecnicaPreparazione {Nome: "taglio a risonanza sonica rigenerativa"}\n\n')
            AIMessage(content='Ho validato le entità. Genero la query finale. Utilizzo un alias t1 per validare che il piatto utilizzi una tecnica di taglio ed un alias t2 per validare che utilizzi una tecnica che richieda la licenza t', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t1:TecnicaPreparazione), (p)-[:PREPARATO_CON]->(t2:TecnicaPreparazione) WHERE (apoc.text.levenshteinDistance(t1.Nome, 'affumicatura temporal risonante') < 3) AND (apoc.text.levenshteinDistance(t2.Nome, 'taglio a risonanza sonica rigenerativa') < 3 OR apoc.text.levenshteinDistance(t2.Nome, 'taglio dimensionale a lame fotofiliche') < 3) RETURN DISTINCT p.Nome', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: panetto di carne\n\n')         
            AIMessage(content='I piatti che necessitano della licenza temporale non base sono: panetto di carne')\n

            [Input]\n
            "Quali piatti sono cucinati da chef con licenza Mx di grado 1 e che contengono Erba Pipa?"\n 
            [Output]\n
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
            AIMessage(content="Ho trovato tutte le entità, genero la query per ottenere l'elenco dei piatti che soddisfano la domanda", tool_calls=[{'args': {'query_cypher': 'MATCH (p:Piatto)<-[:SERVE]-(r:Ristorante)-[:HA_CHEF]->(s:Chef)-[ce:HA_CERTIFICAZIONE]->(c:Certificazione) WHERE ce.Livello = '1' AND apoc.text.levenshteinDistance(c.Nome, 'magnetico') < 5 MATCH (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'erba pipa') < 5  RETURN p.Nome', 'name': 'retrieve_technical_context'},])
            ToolMessage(content="Graph DB content: 'pioggia di andromeda', 'galassia spaziale')
            AIMessage(content="I piatti che hanno l'erba pipa e sono cucinati con licenza magnetica di grado almeno 1 sono: pioggia di andromeda e galassia spaziale)\n
            
            [Input]\n
            "Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento di Sirius Cosmo"\n
            [Output]\n
            AIMessage(content='Devo cercare quali sono le tecniche di surgelamento', tool_calls=[{'args': {'k': 3, 'question': 'Tecniche di Surgelamento'}, 'name': 'retrieve_functional_context'}
            ])\n 
            ToolMessage(content='Vector Store content: Tecniche di Surgelamento: Cryo-Tessitura Energetica Polarizzata, Congelamento Bio-Luminiscente Sincronico\n\n')
            AIMessage(content='Valido le tecniche trovate e l'ingrediente presente nella domanda sul grafo', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Cryo-Tessitura Energetica Polarizzata')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Congelamento Bio-Luminiscente Sincronico')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}}
            {'args': {'query_cypher': 'MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('Spaghi del Sole')) < 3 RETURN i, labels(i) AS entita', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "cryo-tessitura energetica polarizzata│["TecnicaPreparazione"]\n\n')        
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "congelamento bio-luminiscente sincronico│["TecnicaPreparazione"]}}\n\n')        
            ToolMessage(content='Graph DB content: (:Ingrediente {{Provenienza: "unknown",Nome: "carne di balena spaziale"}})\n\n')        
            AIMessage(content='Ora so con certezza che le entità esistono e so come si scrivono. Posso creare la query per ottenere i piatti e rispondere alla domanda', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t:TecnicaPreparazione), (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'spaghi del sole') < 3 AND (apoc.text.levenshteinDistance(t.Nome, 'Cryo-Tessitura Energetica Polarizzata') < 3 OR apoc.text.levenshteinDistance(t.Nome, 'taglio dimensionale a lame fotofiliche') < 3) RETURN p.Nome', 'name': 'retrieve_technical_context'}
            ])
            ToolMessage(content='Graph DB content: galassia aurorale\n\n')
            AIMessage(content="I piatti che utilizzano almeno una tecnica di surgelamento e includono gli spaghi del sole sono: galassia aurorale)\n
"""

examples = """
            [Input]\n
            'Quali piatti sono preparati con almeno una delle tecniche di $NOME_TECNICA e necessitano della licenza $NOME_LICENZA non base per la preparazione?\n
            [Output]\n
            AIMessage(content='Devo cercare quali sono le tecniche di $NOME_TECNICA', tool_calls=[{'args': {'k': 3, 'question': 'Tecniche di $NOME_TECNICA'}, 'name': 'retrieve_functional_context'}
            ])\n 
            ToolMessage(content='Vector Store content: 1. $TECNICA_1; 2. $TECNICA_2\n\n')
            AIMessage(content='Ora voglio cercare la licenza $NOME_LICENZA sul manuale di cucina, per poter capire il nome completo dalla sigla e qual è il livello base', tool_calls=[{'args': {'k': 2, 'question': 'Licenza $NOME_LICENZA'}, 'name': 'retrieve_functional_context'}
            ])
            ToolMessage(content='Vector Store content: $NOME_LICENZA ha: **Livello I**, **Livello II** e **Livello III**')          
            AIMessage(content='Ho capito che il livello base è 1. Ora voglio conoscere quali tecniche di preparazione necessitano della licenza $NOME_LICENZA non base. Per farlo devo leggere la regolamentazione', tool_calls=[{'args': {'k': 2, 'question': 'Licenze e Tecniche di Preparazione - regolamentazione'}, 'name': 'retrieve_functional_context'}])\n 
            ToolMessage(content='Vector Store content: Le disposizioni di cui ai successivi articoli individuano e disciplinano, in via tassativa ed esaustiva, le metodologie di preparazione alimentare per le quali è richiesto il possesso di licenze diverse o di livello superiore rispetto a quelle conferite ope legis.  
            4.1 $NOME_CATEGORIA_TECNICA_1: - La $TECNICA_3 richiede una licenza $NOME_LICENZA di livello I
            4.2 $NOME_CATEGORIA_TECNICA_2: - La $TECNICA_4 richiede una licenza $NOME_LICENZA_2 di livello I - La $TECNICA_5 richiede una $NOME_LICENZA di secondo (II) livello\n\n')\n
            AIMessage(content='So che la tecnica $TECNICA_5 richiede la licenza $NOME_LICENZA non base. Ora valido tutte le entità', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('$TECNICA_5')) < 3
            MATCH (t1:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t1.Nome, LOWER('$TECNICA_1')) < 3
            MATCH (t2:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t2.Nome, LOWER('$TECNICA_2')) < 3
            RETURN t, t1, t2', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {Nome: "$TECNICA_5"})│["Certificazione"], (:TecnicaPreparazione {Nome: "$TECNICA_1"}, (:TecnicaPreparazione {Nome: "$TECNICA_2"}\n\n')
            AIMessage(content='Ho validato le entità. Genero la query finale. Utilizzo un alias t1 per validare che il piatto utilizzi una tecnica di $NOME_TECNICA ed un alias t2 per validare che utilizzi una tecnica che richieda la licenza $NOME_LICENZA', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t1:TecnicaPreparazione), (p)-[:PREPARATO_CON]->(t2:TecnicaPreparazione) WHERE (apoc.text.levenshteinDistance(t1.Nome, '$TECNICA_5') < 3) AND (apoc.text.levenshteinDistance(t2.Nome, '$TECNICA_1') < 3 OR apoc.text.levenshteinDistance(t2.Nome, '$TECNICA_2') < 3) RETURN DISTINCT p.Nome', 'name': 'retrieve_technical_context'}})
            ToolMessage(content='Graph DB content: panetto di carne\n\n')         
            AIMessage(content='I piatti che necessitano della licenza temporale non base sono: panetto di carne')\n

            [Input]\n
            "Quali piatti sono cucinati da chef con licenza Mx di grado 1 e che contengono Erba Pipa?"\n 
            [Output]\n
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
            AIMessage(content="Ho trovato tutte le entità, genero la query per ottenere l'elenco dei piatti che soddisfano la domanda", tool_calls=[{'args': {'query_cypher': 'MATCH (p:Piatto)<-[:SERVE]-(r:Ristorante)-[:HA_CHEF]->(s:Chef)-[ce:HA_CERTIFICAZIONE]->(c:Certificazione) WHERE ce.Livello = '1' AND apoc.text.levenshteinDistance(c.Nome, 'magnetico') < 5 MATCH (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'erba pipa') < 5  RETURN p.Nome', 'name': 'retrieve_technical_context'},])
            ToolMessage(content="Graph DB content: 'pioggia di andromeda', 'galassia spaziale')
            AIMessage(content="I piatti che hanno l'erba pipa e sono cucinati con licenza magnetica di grado almeno 1 sono: pioggia di andromeda e galassia spaziale)\n

            [Input]\n
            "Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento di Sirius Cosmo"\n
            [Output]\n
            AIMessage(content='Devo cercare quali sono le tecniche di surgelamento', tool_calls=[{'args': {'k': 3, 'question': 'Tecniche di Surgelamento'}, 'name': 'retrieve_functional_context'}
            ])\n 
            ToolMessage(content='Vector Store content: Tecniche di Surgelamento: Cryo-Tessitura Energetica Polarizzata, Congelamento Bio-Luminiscente Sincronico\n\n')
            AIMessage(content='Valido le tecniche trovate e l'ingrediente presente nella domanda sul grafo', tool_calls=[
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Cryo-Tessitura Energetica Polarizzata')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}
            {'args': {'query_cypher': 'MATCH (t:TecnicaPreparazione) WHERE apoc.text.levenshteinDistance(t.Nome, LOWER('Congelamento Bio-Luminiscente Sincronico')) < 3 RETURN t, labels(t) AS entita', 'name': 'retrieve_technical_context'}}
            {'args': {'query_cypher': 'MATCH (i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, LOWER('Spaghi del Sole')) < 3 RETURN i, labels(i) AS entita', 'name': 'retrieve_technical_context'}}
            ])
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "cryo-tessitura energetica polarizzata│["TecnicaPreparazione"]\n\n')        
            ToolMessage(content='Graph DB content: (:TecnicaPreparazione {{Nome: "congelamento bio-luminiscente sincronico│["TecnicaPreparazione"]}}\n\n')        
            ToolMessage(content='Graph DB content: (:Ingrediente {{Provenienza: "unknown",Nome: "carne di balena spaziale"}})\n\n')        
            AIMessage(content='Ora so con certezza che le entità esistono e so come si scrivono. Posso creare la query per ottenere i piatti e rispondere alla domanda', tool_calls=[
            {'args': {'query_cypher': 'MATCH (p:Piatto)-[:PREPARATO_CON]->(t:TecnicaPreparazione), (p)-[:CONTIENE]->(i:Ingrediente) WHERE apoc.text.levenshteinDistance(i.Nome, 'spaghi del sole') < 3 AND (apoc.text.levenshteinDistance(t.Nome, 'Cryo-Tessitura Energetica Polarizzata') < 3 OR apoc.text.levenshteinDistance(t.Nome, 'taglio dimensionale a lame fotofiliche') < 3) RETURN p.Nome', 'name': 'retrieve_technical_context'}
            ])
            ToolMessage(content='Graph DB content: galassia aurorale\n\n')
            AIMessage(content="I piatti che utilizzano almeno una tecnica di surgelamento e includono gli spaghi del sole sono: galassia aurorale)\n
"""

