from langchain_core.runnables import RunnablePassthrough

abstract_entity_extractor = (
    RunnablePassthrough.assign(
        json_templates=process_files
    )
)