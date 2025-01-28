from langchain_core.prompts import ChatPromptTemplate

prompt_responder = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''
            Sei un assistente il cui compito è estrarre in modo strutturato una lista di piatti caratterizzati da un nome.
            In input riceverai una lista scritta in linguaggio naturale da cui deve essere estrapola una struttura dati 
            contenente le stesse informazioni.
            
            Esempio:
            [Input]
            'I piatti che include le Chocobo Wings come ingrediente sono:\n
            - Galassia di Sapori: Il Viaggio Senza Tempo,\n
            - Sinfonia Cosmica di Andromeda,\n
            - Porta Celestiale alle Stelle.
            
            [Output]
            Output(piatti=[Piatto(nome='Galassia di Sapori: Il Viaggio Senza Tempo'), 
            Piatto(nome='Sinfonia Cosmica di Andromeda'), Piatto(nome='Porta Celestiale alle Stelle')])
            '''
        ),
        ("placeholder", "{messages}"),
    ]
)

prompt_responder = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''
            Sei un assistente specializzato nell'estrazione strutturata di informazioni. Il tuo compito è trasformare 
            un elenco di piatti scritto in linguaggio naturale in una struttura dati organizzata, mantenendo fedelmente 
            le informazioni fornite.

            **Istruzioni**:
            - Riceverai un input contenente un elenco di piatti scritto in linguaggio naturale.
            - Estrai una struttura dati nel formato richiesto.
            - Assicurati che i nomi dei piatti siano copiati esattamente come nell'input, senza alterazioni.\n\n

            Esempio:
            [Input]
            "I piatti che includono le Chocobo Wings come ingrediente sono:
            - Galassia di Sapori: Il Viaggio Senza Tempo,
            - Sinfonia Cosmica di Andromeda,
            - Porta Celestiale alle Stelle."

            [Output]
            Output(piatti=[
                Piatto(nome='Galassia di Sapori: Il Viaggio Senza Tempo'),
                Piatto(nome='Sinfonia Cosmica di Andromeda'),
                Piatto(nome='Porta Celestiale alle Stelle')
            ])
            '''
        ),
        ("placeholder", "{messages}"),
    ]
)
