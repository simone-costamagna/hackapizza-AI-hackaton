from langchain_core.prompts import ChatPromptTemplate

PROMPT_PARSE_LEGAL_CODES = ChatPromptTemplate([
    ("system", """Sei un assistente esperto nella conversione di documenti in formato Markdown ben strutturato e leggibile. 
    Il tuo obiettivo è creare un file Markdown ottimizzato per un approccio RAG (Retrieve-Augment-Generate).\n
    Evita di modificare il contenuto del testo."""),
    ("human", "Converti questo contenuto in formato .md: {content}"),
])


