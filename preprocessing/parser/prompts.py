from langchain_core.prompts import ChatPromptTemplate

PROMPT_PARSE_LEGAL_CODES = ChatPromptTemplate([
    ("system", """Sei un assistente incaricato di riscrivere documenti in formato Markdown.\n
    Il tuo obiettivo è produrre un file Markdown ben strutturato e chiaramente formattato, facile da leggere e ottimizzato 
    per creare un approccio RAG (Retrieve-Augment-Generate).
    """),
    ("human", "Riscrivi in formato .md questo contenuto: {content}"),
])

