WATSONX = "WATSONX"
MISTRAL = "mistralai/mistral-large"

BEDROCK = "BEDROCK"
CLAUDE_3_5_SONNET = "anthropic.claude-3-5-sonnet-20240620-v2:0"

OPENAI = "OPENAI"
GPT_40 = "gpt-4o"
GPT_40_MINI = "gpt-4o-mini"
GPT_01_MINI = "o1-mini"
GPT_03_MINI = "o3-mini"

MODELS = {
    WATSONX: [MISTRAL],
    BEDROCK: [CLAUDE_3_5_SONNET],
    OPENAI: [GPT_40, GPT_40_MINI, GPT_01_MINI, GPT_03_MINI]
}
