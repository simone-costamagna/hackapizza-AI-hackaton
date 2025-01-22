from langchain_core.prompts import ChatPromptTemplate

PROMPT_PARSE_LEGAL_CODES = ChatPromptTemplate([
        ("system", """You are an assistant tasked with rewriting documents in Markdown format.\n
        Your goal is to produce a well-structured and clearly formatted Markdown file that is easy to read and optimized 
        for creating a RAG (Retrieve-Augment-Generate) approach.
        """),
        ("human", "Rewrite in an .md format this content: {content}"),
])
