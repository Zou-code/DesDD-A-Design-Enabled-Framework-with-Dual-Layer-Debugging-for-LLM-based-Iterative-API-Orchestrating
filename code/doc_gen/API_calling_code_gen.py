import pandas as pd
import sys
import os
from util.llm_util import LLM_util
from config import Config
from util.log import Logger
from prompt.prompt_api_code import prompt_API_code
from prompt.prompt_code_refactor import prompt_code_refactor
from tqdm import tqdm
import re
import time
import logging

# # 获取当前时间并格式化
# current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
#
# # 定义日志文件名
# log_filename = f"../logs/log_API_calling_code/log_{current_time}.log"
#
# # 配置日志记录器
# logging.basicConfig(
#     level=logging.DEBUG,  # 设置日志级别
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
#     handlers=[
#         logging.FileHandler(log_filename),  # 文件处理器
#         logging.StreamHandler()  # 控制台处理器
#     ]
# )


class CallingCode:
    def __init__(self):
        self.model = LLM_util()


    @staticmethod
    def code_extract(code):
        code = re.sub(r'^```json\n|\n```$', '', code)
        code = re.sub(r'^```\n|\n```$', '', code)
        code = re.sub(r'^```python\n|\n```$', '', code)
        return code

    def generate_api_calling_code(self):
        """
        遍历../data/tools.csv文件中的所有tool以及该tool下的所有API，调用LLM生成API调用代码
        生成的API调用代码保存在../Tools文件中,其中Tools文件中每个子文件夹都对应一个tool
        :return:
        """
        df_tools = pd.read_csv(Config.tool_path)
        df_apis = pd.read_csv(Config.api_path)

        for _,row_tool in tqdm(df_tools.iterrows(), total=len(df_tools),desc="Tool Loop"):
            tool_name = row_tool['tool_name']
            head = row_tool['head']
            # 查找当前tool下的所有API
            api_columns = df_apis.loc[(df_apis['tool_name'] == tool_name)]
            if api_columns.empty:
                logging.error(f"No API found for tool {tool_name}")
            else:
                for _,row_api in tqdm(api_columns.iterrows(), total=len(api_columns),desc='API Loop', leave=False):
                    api_name = row_api['api_name']
                    api_description = row_api['api_description']
                    required_parameters = row_api['required_parameters']
                    endpoint_name = row_api['endpoint_name']
                    query_string = row_api['query_string']
                    response_schema = row_api['json_schema']

                    # 将tool name 和api name中的空格替换为下划线
                    tool_name = tool_name.replace(' ', '_')
                    api_name = api_name.replace(' ', '_')
                    API_doc = f'''\
API_name: {api_name}
API_description: {api_description}
required_parameters: {required_parameters}
response_schema: 
{response_schema}
'''
                    API_request_code = row_api['example_calling_code']
                    prompt = prompt_API_code(API_doc, API_request_code)
                    code = self.model.model_gpt4o(prompt)
                    code = CallingCode.code_extract(code)
                    prompt_refactor = prompt_code_refactor(code,api_name, response_schema, api_description)
                    code = self.model.model_deepseek_coder(prompt_refactor)
                    code = CallingCode.code_extract(code)
                    file_path = f'../Tools/{tool_name}/{api_name}.py'

                    #获取文件所在的目录
                    dir_path = os.path.dirname(file_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(code)
                        f.close()

if __name__ == '__main__':
    calling = CallingCode()
    calling.generate_api_calling_code()
