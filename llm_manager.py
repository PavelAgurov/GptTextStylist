"""
    LLM
"""
# pylint: disable=C0301,C0103,C0303,C0411,R0903,C0304

from dataclasses import dataclass
import os

import tiktoken

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
    title  : str
    explanation : str
    error  : str
    tokens_input : int
    tokens_used : int
    debug_str : str = None

class LlmManager():
    """LLM Manager"""
    llm_style    : ChatOpenAI
    style_prompt : PromptTemplate
    style_chain  : LLMChain
    token_estimator : tiktoken.core.Encoding

    _MODEL_NAME = "gpt-3.5-turbo" # gpt-3.5-turbo-16k
    _MAX_TOKENS = 1000

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
        self.token_estimator = tiktoken.encoding_for_model(self._MODEL_NAME)

    def __get_api_key(self):
        return os.environ["OPENAI_API_KEY"]

    def len_function(self, text : str) -> int:
        """Lenght function"""
        return len(self.token_estimator.encode(text))

    def apply_style(self, input_text : str, style : str) -> OutputItem:
        """Apply style to text input"""

        input_len = self.len_function(input_text)
        if input_len > self._MAX_TOKENS:
            error_tokens = "Sorry, it's only PoC, text is too long"
            return OutputItem(None, None, None, error_tokens, input_len, 0)

        total_tokens = 0
        result_str = None
        try:
            with get_openai_callback() as llm_callback:
                result_str = self.style_chain.invoke({
                        "style" : style, 
                        "text" : input_text
                    })
            total_tokens = llm_callback.total_tokens
        except Exception as error: # pylint: disable=W0718
            return OutputItem(None, None, error, input_len, total_tokens, result_str)

        result_dict = llm_utils.parse_llm_xml(result_str, ['changed_text', 'proposed_title', 'explanation'])
        return OutputItem(
                    result_dict['changed_text'],
                    result_dict['proposed_title'],
                    result_dict['explanation'],
                    None,
                    input_len,
                    total_tokens
                )
