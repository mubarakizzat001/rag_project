from ..LLMInterface import LLMInterface
import cohere
import logging
from ..LLMEnums import CohereEnums,DocumentType

logger=logging.getLogger(__name__)

class CoHereProvider(LLMInterface):
    def __init__(
        self,
        api_key:str,
        default_input_max_charecters:int=1000,
        default_output_max_tokens:int=1000,
        default_temperature:float=0.1
        
    ):
        self.api_key=api_key
        self.default_input_max_charecters=default_input_max_charecters
        self.default_output_max_tokens=default_output_max_tokens
        self.default_temperature=default_temperature
        self.generate_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None

        self.client=cohere.Client(api_key=self.api_key)

        self.logger=logging.getLogger(__name__)

    def set_generate_model(self,model_id:str):
        self.generate_model_id=model_id
    def set_embedding_model(self,model_id:str,embedding_size:int):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size
    def process_text(self,text:str):
        return text[:self.default_input_max_charecters].strip()

    def generate_text(
        self,
        prompt:str,
        chat_history:list=[],
        max_output_tokens:int=None,
        temperature:float=None
    ):
        if not self.client:
            self.logger.error("Cohere not initialized")
            return None
        if not self.generate_model_id:
            self.logger.error("Generate model not set")
            return None
        response=self.client.chat(
            model=self.generate_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            max_tokens=max_output_tokens,
            temperature=temperature

        )
        if not response or not response.text:
            self.logger.error("No response from Cohere")
            return None
        return response.text

    def embed_text(self,text:str,document_type:str=None):
        if not self.client:
            self.logger.error("Cohere not initialized")
            return None
        if not self.embedding_model_id:
            self.logger.error("embedding model not set")
            return None

        input_type=DocumentType.DOCUMENT if document_type==DocumentType.DOCUMENT else DocumentType.QUERY
        
        response=self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"]
        )
        if not response or not response.embeddings or response.embeddings.float:
            self.logger.error("No response from Cohere")
            return None
        return response.embeddings.float[0]

    def construct_prompt(self,prompt:str,role:str):
        return {
            "role":role,
            "text":self.process_text(prompt)
        }