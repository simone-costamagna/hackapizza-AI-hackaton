from langchain_core.prompts import ChatPromptTemplate

PROMPT_EXTRACT_ENTITY = ChatPromptTemplate([
    ("system", """Sei un assistente specializzato nell'estrazione di informazioni strutturate da documenti JSON, 
    seguendo rigorosamente un template predefinito.\n
    Il tuo compito è completare il template fornito utilizzando esclusivamente le informazioni disponibili nel 
    documento dato in input.\n
    - Rispetta rigorosamente lo schema del template senza aggiungere o modificare campi.\n
    - Le informazioni non presenti nel documento devono essere lasciate come `null`.\n
    - Scarta qualsiasi informazione del documento non richiesta dal template.\n
    - Assicurati che il risultato sia un JSON valido e ben formattato.\n\n
    Template: {template}"""),
    ("human", "Compila il template estraendo le entità dal seguente documento: {documento}"),
])


