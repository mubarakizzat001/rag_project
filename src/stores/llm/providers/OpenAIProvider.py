from ..LLMInterface import LLMInterface
from openai import OpenAI
from ..LLMEnums import OpenAIEnums
import logging

logger=logging.getLogger(__name__)

class OpenAIProvider(LLMInterface):
    def __init__(
        self,
        api_key:str,
        api_url:str,
        default_input_max_charecters:int=1000,
        default_output_max_tokens:int=1000,
        default_temperature:float=0.1
        
    ):
        self.api_key=api_key
        self.api_url=api_url
        self.default_input_max_charecters=default_input_max_charecters
        self.default_output_max_tokens=default_output_max_tokens
        self.default_temperature=default_temperature
        self.generate_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None
        self.client=OpenAI(api_key=self.api_key,base_url=self.api_url)
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
            self.logger.error("OpenAI client not initialized")
            return None
        if not self.generate_model_id:
            self.logger.error("Generate model not set")
            return None
        max_output_tokens=max_output_tokens if max_output_tokens else self.default_output_max_tokens
        temperature=temperature if temperature else self.default_temperature
        
        chat_history.append(
            self.construct_prompt(prompt=prompt,role=OpenAIEnums.SYSTEM.value)
        )
        
        response=self.client.chat.completions.create(
            model=self.generate_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message or not response.choices[0].message.content:
            self.logger.error("Failed to get response")
            return None
        return response.choices[0].message.content

    def embed_text(self,text:str,document_type:str=None):
        if not self.client:
            self.logger.error("OpenAI client not initialized")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model not set")
            return None
        response=self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )
        if not response or not response.data or len(response.data)==0 or not response.data[0].embedding:
            self.logger.error("Failed to get embedding")
            return None
        embedding=response.data[0].embedding
        if not embedding:
            self.logger.error("Embedding is None")
            return None
        if len(embedding)!=self.embedding_size:
            self.logger.error("Embedding size does not match")
            return None
        return embedding
  
        
    def construct_prompt(self,prompt:str,role:str):
        return {
            "role":role,
            "content":self.process_text(prompt)
        }