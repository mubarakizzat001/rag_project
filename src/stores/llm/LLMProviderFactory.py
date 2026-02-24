from .LLMEnums import LLMEnums
from .providers import OpenAIProvider,CoHereProvider

class LLMProviderFactory:
    def __init__(self,config:dict):
        self.config=config


    def create(self,provider:str):

        if provider==LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_charecters=self.config.OPENAI_DEFAULT_INPUT_MAX_CHARECTERS,
                default_output_max_tokens=self.config.OPENAI_DEFAULT_OUTPUT_MAX_TOKENS,
                default_temperature=self.config.OPENAI_DEFAULT_TEMPERATURE
            )
        if provider==LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_charecters=self.config.COHERE_DEFAULT_INPUT_MAX_CHARECTERS,
                default_output_max_tokens=self.config.COHERE_DEFAULT_OUTPUT_MAX_TOKENS,
                default_temperature=self.config.COHERE_DEFAULT_TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")