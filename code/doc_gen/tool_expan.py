import re

import pandas as pd

from util.llm_util import LLM_util
from util.code_util import CodeUtil
from config import Config
from prompt.prompt_json_schema import prompt_json_schema
from prompt.prompt_tool_doc_generation import prompt_tool_doc_gen
from prompt.prompt_api_doc_generation import prompt_api_doc_generation
from prompt.prompt_tool_doc import prompt_tool_doc
from prompt.prompt_api_dependency_gen import prompt_dependency

class ToolExpan:

    # WARN 下面的这个方法已经弃用
    @staticmethod
    def Tool_doc_expan(tool_name):
        """
        根据 tool_name调用返回工具的各种信息，但不进行原始csv文件的插入处理
        返回的结果是LLM生成的原生的json数据，不进行json的处理
        :param
        tool_name: 工具的名称
        :return: json格式的tool的各种信息
        """
        tool_doc = CodeUtil.get_tool_doc(tool_name)
        print(tool_doc)
        prompt = prompt_tool_doc_gen(tool_doc)
        print(prompt)
        llm = LLM_util()
        tool_info = llm.model_deepseek_chat(prompt)
        return tool_info


    @staticmethod
    def json_schema_generation(json_data):
        """
        调用模型，生成json数据的schema,直接返回，不会插入到原始csv文件中
        :param
        json_data: 输入的json数据
        :return:
        """
        llm = LLM_util()
        num_tokens = LLM_util.num_tokens_from_prompt(json_data)
        if num_tokens > 8000:
            json_tokens = LLM_util.get_top_k_tokens(json_data, 6000)
            json_data = LLM_util.tokens_to_text(json_tokens)
        prompt = prompt_json_schema(json_data)
        json_schema = llm.model_deepseek_coder(prompt)
        return json_schema

    @staticmethod
    def API_doc_generation(api_doc):
        """
        调用模型，生成API的文档，直接返回，不会插入到原始csv文件中
        :param
        api_doc: 需要进行扩展的API的信息
        :return:
        """

        llm = LLM_util()
        prompt = prompt_api_doc_generation(api_doc)
        # print(prompt)
        expan_api_doc = llm.model_deepseek_chat(prompt)
        # print(expan_api_doc)
        expan_api_doc = re.sub(r'^```json\n|\n```$', '', expan_api_doc)
        expan_api_doc = re.sub(r'^```\n|\n```$', '', expan_api_doc)
        # print(expan_api_doc)

        return expan_api_doc

    @staticmethod
    def tool_doc_generation(tool_doc):
        llm = LLM_util()
        prompt = prompt_tool_doc(tool_doc)
        expan_tool_doc = llm.model_deepseek_coder(prompt)
        expan_tool_doc = re.sub(r'^```json\n|\n```$', '', expan_tool_doc)
        expan_tool_doc = re.sub(r'^```\n|\n```$', '', expan_tool_doc)
        # print(expan_tool_doc)
        return expan_tool_doc

    @staticmethod
    def API_dependency_generation(API_doc):
        llm = LLM_util()
        prompt = prompt_dependency(API_doc)
        API_dependency = llm.model_deepseek_chat(prompt)
        API_dependency = re.sub(r'^```json\n|\n```$', '', API_dependency)
        API_dependency = re.sub(r'^```\n|\n```$', '', API_dependency)
        return API_dependency


if __name__ == '__main__':
    # tool_info = ToolExpan.Tool_doc_generation('Movies API')
    # print(tool_info)

    tool_doc = '''\
'''

    # print(ToolExpan.API_doc_generation())
