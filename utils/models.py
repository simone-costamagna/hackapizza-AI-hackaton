WATSONX = "WATSONX"
MISTRAL = "mistralai/mistral-large"

BEDROCK = "BEDROCK"
CLAUDE_SONNET_3_5 = ""

OPENAI = "OPENAI"
GPT_40 = "gpt-4o"
GPT_40_MINI = "gpt-4o-mini"

MODELS = {
    WATSONX: [MISTRAL],
    BEDROCK: [CLAUDE_SONNET_3_5],
    OPENAI: [GPT_40, GPT_40_MINI]
}