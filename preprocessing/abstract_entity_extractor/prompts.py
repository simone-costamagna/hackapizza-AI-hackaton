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