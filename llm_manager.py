"""
    LLM
"""
# pylint: disable=C0301,C0103,C0303,C0411,R0903

from dataclasses import dataclass
import os

import langchain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
from langchain.cache import SQLiteCache
from langchain.callbacks import get_openai_callback

import prompts
import llm_utils

@dataclass
class OutputItem:
    """Output item"""
    result : str
    explanation : str
    error  : str
    tokens_used : int

class LlmManager():
    """LLM Manager"""
    llm_style    : ChatOpenAI
    style_prompt : PromptTemplate
    style_chain  : LLMChain

    _MODEL_NAME = "gpt-3.5-turbo" # gpt-3.5-turbo-16k

    def __init__(self):
        langchain.llm_cache = SQLiteCache()

        self.llm_style = ChatOpenAI(
                openai_api_key= self.__get_api_key(),
                model_name  = self._MODEL_NAME,
                temperature = 0.5,
                max_tokens  = 1000
        )
        self.style_prompt = PromptTemplate.from_template(prompts.apply_style_prompt_template)
        self.style_chain  = self.style_prompt | self.llm_style | StrOutputParser()

    def __get_api_key(self):
        return os.environ["OPENAI_API_KEY"]

    def apply_style(self, input_text : str, style : str) -> OutputItem:
        """Apply style to text input"""

        with get_openai_callback() as llm_callback:
            result_str = self.style_chain.invoke({
                    "style" : style, 
                    "text" : input_text
                })

            total_tokens = llm_callback.total_tokens
            try:
                result_json = llm_utils.get_llm_json(result_str)
                return OutputItem(
                            result_json['new_text'],
                            result_json['explanation'],
                            None,
                            total_tokens
                        )
            except Exception as error: # pylint: disable=W0718
                return OutputItem(None, None, error, total_tokens)