from langchain_core.prompts import ChatPromptTemplate

PROMPT_EXTRACT_ENTITY = ChatPromptTemplate([
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

