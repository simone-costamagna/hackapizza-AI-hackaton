WATSONX = "WATSONX"
MISTRAL = "mistralai/mistral-large"

BEDROCK = "BEDROCK"
CLAUDE_3_5_SONNET = "anthropic.claude-3-5-sonnet-20240620-v1:0"

OPENAI = "OPENAI"
GPT_40 = "gpt-4o"
GPT_40_MINI = "gpt-4o-mini"

MODELS = {
    WATSONX: [MISTRAL],
    BEDROCK: [CLAUDE_3_5_SONNET],
    OPENAI: [GPT_40, GPT_40_MINI]
}
