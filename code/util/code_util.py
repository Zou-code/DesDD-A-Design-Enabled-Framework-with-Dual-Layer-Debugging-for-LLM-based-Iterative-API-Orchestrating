import pandas as pd
from config import Config
import numpy as np
import re
from util.llm_util import LLM_util
from prompt.prompt_json_data_extract import prompt_json_data_extract
from prompt.prompt_code_extract import prompt_code_extract
import json
import time
import logging

class CodeUtil:

    @staticmethod
    def get_api_doc(df_tools):
        """
        组装第三步骤task plan 所需的工具和API文档的信息
        示例：
        Tool name: Advanced Movie Search
        Tool description: Search for movies via advanced queries like genre, name, etc. And get all their details
            API name: Search by Genre
            API description: This API allows users to discover movies by their genre.
            scenario: If a user wants to find all movies in the 'Action' genre, they would use this API.
            parameters:
                with_genres: (String) This is an optional parameter where the user can specify the genre of the movie they are looking for.
                page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

            API name: Search by Name
            API description: This API allows users to search for a movie by its name.
            scenario: If a user wants to find a movie named 'Kong', they would use this API.
            parameters:
                query: (String) This is a required parameter where the user can specify the name of the movie they are searching for.
                page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

            API name: Get Detailed Response
            API description: This API provides detailed information about a movie based on its ID.
            scenario: If a user wants to get detailed information about a movie with the ID '399566', they would use this API.
            parameters:
                movie_id: (Number) This is a required parameter where the user can specify the ID of the movie they want detailed information about.
        :return:
        """
        df_apis = pd.read_csv(Config.api_path)
        # df_tools = pd.read_csv(Config.tool_path)
        api_doc = ''

        for _, tool_row in df_tools.iterrows():
            tool_name = tool_row['tool_name']
            tool_desc = tool_row['tool_description']
            tool_str = f'''\
        Tool name: {tool_name}
        Tool description: {tool_desc}
'''
            api_doc = api_doc + tool_str
            # url = tool_row['head']
            apis = df_apis.loc[df_apis['tool_name'] == tool_name]
            apis_prefix = ''''''
            for index, api_row in apis.iterrows():
                api_name = api_row['api_name'].strip()
                api_desc = api_row['api_description'].strip()
                scenario = api_row['scenario'].strip()
                API_dependency = api_row['calling_dependency'].strip()
                required_parameters = api_row['required_parameters']
                parameters_lines = []
                if isinstance(required_parameters, float) and np.isnan(required_parameters):
                    parameters_lines = []
                elif isinstance(required_parameters, str):
                    parameters_lines = required_parameters.split('\n')
                else:
                    parameters_lines = []

                # parameters = '            \n'.join(parameters_lines)
                parameters = ''
                for line in parameters_lines:
                    p = f'''\
                {line.strip()}'''
                    parameters = parameters + p + '\n'
                    # parameters = '          ' + parameters.strip() + line + '\n'
                api_str = f'''\
            API name: {api_name}
            API description: {api_desc}
            API_dependency: {API_dependency}
            scenario: {scenario}
            parameters:
{parameters}\n'''
                apis_prefix = apis_prefix + api_str
            api_doc = api_doc + apis_prefix
        return api_doc

    # WARN 下面这个方法已弃用，目前Approach下没有适用的
    @staticmethod
    def get_tool_doc(tool_name):
        """
        组装生成需要进行扩写的api文档
        示例：
        tool_name: Advanced Movie Search
tool_description:Search for movies via advanced queries like genre, name, etc. And get all their details
    api_name: Search by Genre
    api_description: This API allows users to discover movies by their genre.
    scenario: ...
    parameters:
        with_genres: (String) This is an optional parameter where the user can specify the genre of the movie they are looking for.
        page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

    api_name: Search by Name
    api_description: This API allows users to search for a movie by its name.
    scenario: ...
    parameters:
        query: (String) This is a required parameter where the user can specify the name of the movie they are searching for.
        page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

    api_name: Get Detailed Response
    api_description: This API provides detailed information about a movie based on its ID.
    scenario: ...
    parameters:
        movie_id: (Number) This is a required parameter where the user can specify the ID of the movie they want detailed information about.

        :param tool_name:
        :return:
        """

        df_tools = pd.read_csv(Config.tool_original_path)
        df_apis = pd.read_csv(Config.api_first_expan_path)

        df_selected_tool = df_tools.loc[df_tools['tool_name'] == tool_name]
        tool_description = ''
        for _,row in df_selected_tool.iterrows():
            tool_description = row['tool_description']

        tool_doc = f'''\
tool_name: {tool_name}
tool_description:{tool_description}'''
        apis = df_apis.loc[df_apis['tool_name'] == tool_name]
        api_doc = ''
        for _,row_api in apis.iterrows():
            api_name = row_api['api_name']
            api_description = row_api['api_description']
            response_schema = row_api['json_schema']

            required_parameters = row_api['required_parameters']

            # 确保当参数为空的情况下的处理
            if isinstance(required_parameters, float) and np.isnan(required_parameters):
                parameters_lines = []
            elif isinstance(required_parameters, str):
                parameters_lines = required_parameters.split('\n')
            else:
                parameters_lines = []

            parameters = ''
            if parameters_lines == []:
                parameters = 'None'

            for line in parameters_lines:
                p = f'''\
        {line.strip()}'''
                parameters = parameters + p + '\n'
            api_str = f'''
    api_name: {api_name}
    api_description: {api_description}
    scenario: ...
    parameters: 
{parameters}
    response_schema: 
    {response_schema}'''
            api_doc = api_doc + api_str
        tool_doc = tool_doc + api_doc
        return tool_doc

    @staticmethod
    def get_API_doc_for_error_judge(tool_API_pairs):
        """
        组装生成对可运行代码进行错误判断的API文档，即在task plan阶段选择了的API的文档
        :param tool_API_pairs: JSON格式的选中的API的及API对应的tool  {"API1":["API_name", "tool_name"], ...}
        :return:
        """
        df_APIs = pd.read_csv(Config.api_path)
        API_doc = ''
        # tool_API_pairs = json.loads(tool_API_pairs)
        for values in tool_API_pairs.values():
            tool_name = values[-1]
            API_name = values[0]
            df_selected_API = df_APIs.loc[(df_APIs['api_name'] == API_name) & (df_APIs['tool_name'] == tool_name)]
            for _,row in df_selected_API.iterrows():
                API_doc = API_doc + f'''\
        API_name: {API_name}
        API_description: {row['api_description']}
        use_scenario: {row['scenario']}
        required_parameters: {row['required_parameters']}
        API_calling_dependency: {row['calling_dependency']}
        response_schema:
        {row['json_schema']}
'''
        return API_doc


    @staticmethod
    def string_clean(original_string):
        """
        去掉给定的字符串中的markdown代码
        :param original_string:
        :return:
        """
        cleaned_string = re.sub(r'^```json\n|\n```$', '', original_string)
        cleaned_string = re.sub(r'^```\n|\n```$', '', cleaned_string)
        cleaned_string = re.sub(r'^```python\n|\n```$', '', cleaned_string)
        return cleaned_string

    @staticmethod
    def remove_docstrings(source_code):
        """
        去掉给定的Python源代码中的多行注释
        :param source_code:
        :return:
        """
        pattern = re.compile(r'""".*?"""', re.DOTALL)

        # 去掉多行字符串
        cleaned_code = pattern.sub('', source_code)

        return cleaned_code

    @staticmethod
    def json_string_extract(input_string):
        '''
        提取json字符串
        :return:
        '''
        model = LLM_util()
        prompt = prompt_json_data_extract(input_string)
        json_string = model.model_deepseek_coder(prompt)
        json_string = re.sub(r'^```json\n|\n```$', '', json_string)
        json_string = re.sub(r'^```\n|\n```$', '', json_string)
        return json_string

    @staticmethod
    def get_error_example(pseudocode,error_report,tool_API_doc):
        """
        根据错误报告和API文档生成错误示例, 这部分信息会注入到task_plan_error的prompt中
        :param pseudocode: 伪代码
        :param error_report: 错误报告
        :param tool_API_doc: API文档
        :return:
        """
        error_example = f'''\
        tool_API_documentation:
        {tool_API_doc}
        pseudocode:
        {pseudocode}
        error_report: {error_report}
'''
        return error_example

    @staticmethod
    def configure_logging(log_dir):
        # 获取当前时间并格式化
        current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        # 定义日志文件名
        log_filename = f"{log_dir}/log_{current_time}.log"

        # 配置日志记录器
        logging.basicConfig(
            level=logging.INFO,  # 设置日志级别
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),  # 文件处理器
                logging.StreamHandler()  # 控制台处理器
            ]
        )

    @staticmethod
    def get_code_from_string(original_string):
        """
        提取字符串中的代码
        :param original_string:
        :return:
        """
        model = LLM_util()
        prompt = prompt_code_extract(original_string)
        result = model.model_deepseek_coder(prompt)

        json_data = re.sub(r'^```json\n|\n```$', '', result)
        json_data = re.sub(r'^```\n|\n```$', '', json_data)

        code = json.loads(json_data)

        code = code.get("Python_code")
        return code


    @staticmethod
    def get_API_doc_foe_code_repair(tool_API_pairs):
        """
        根据传入的API列表，获取对应的API文档，用于代码修复
        :param tool_API_pairs: JSON格式的选中的API的及API对应的tool  {"API1":["API_name", "tool_name"], ...}
        :return:
        """
        df_APIs = pd.read_csv(Config.api_path)
        API_doc = ''
        for values in tool_API_pairs.values():
            tool_name = values[1]
            API_name = values[0]
            df_selected_API = df_APIs.loc[(df_APIs['api_name'] == API_name) & (df_APIs['tool_name'] == tool_name)]
            for _, row in df_selected_API.iterrows():
                API_doc = API_doc + f'''\
    API_name:{API_name}
    API_description:{row['api_description']}
    required_parameters:{row['required_parameters']}
    response_schema:{row['json_schema']}
'''
        return API_doc


    @staticmethod
    def get_api_doc_for_codeact(df_tools):
        """
        组装第三步骤task plan 所需的工具和API文档的信息
        示例：
        Tool name: Advanced Movie Search
        Tool description: Search for movies via advanced queries like genre, name, etc. And get all their details
            API name: Search by Genre
            API description: This API allows users to discover movies by their genre.
            scenario: If a user wants to find all movies in the 'Action' genre, they would use this API.
            parameters:
                with_genres: (String) This is an optional parameter where the user can specify the genre of the movie they are looking for.
                page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

            API name: Search by Name
            API description: This API allows users to search for a movie by its name.
            scenario: If a user wants to find a movie named 'Kong', they would use this API.
            parameters:
                query: (String) This is a required parameter where the user can specify the name of the movie they are searching for.
                page: (Number) This is an optional parameter where the user can specify the page number of the search results they want to view.

            API name: Get Detailed Response
            API description: This API provides detailed information about a movie based on its ID.
            scenario: If a user wants to get detailed information about a movie with the ID '399566', they would use this API.
            parameters:
                movie_id: (Number) This is a required parameter where the user can specify the ID of the movie they want detailed information about.
        :return:
        """
        df_apis = pd.read_csv(Config.api_path)
        # df_tools = pd.read_csv(Config.tool_path)
        api_doc = ''

        for _, tool_row in df_tools.iterrows():
            tool_name = tool_row['tool_name']
            tool_desc = tool_row['tool_description']
            tool_str = f'''\
        Tool name: {tool_name}
        Tool description: {tool_desc}
'''
            api_doc = api_doc + tool_str
            # url = tool_row['head']
            apis = df_apis.loc[df_apis['tool_name'] == tool_name]
            apis_prefix = ''''''
            for index, api_row in apis.iterrows():
                api_name = api_row['api_name'].strip()
                response_schema = api_row['json_schema'].strip()
                api_desc = api_row['api_description'].strip()
                scenario = api_row['scenario'].strip()
                API_dependency = api_row['calling_dependency'].strip()
                API_request_code = api_row['example_calling_code'].strip()
                required_parameters = api_row['required_parameters']
                parameters_lines = []
                if isinstance(required_parameters, float) and np.isnan(required_parameters):
                    parameters_lines = []
                elif isinstance(required_parameters, str):
                    parameters_lines = required_parameters.split('\n')
                else:
                    parameters_lines = []

                # parameters = '            \n'.join(parameters_lines)
                parameters = ''
                for line in parameters_lines:
                    p = f'''\
                {line.strip()}'''
                    parameters = parameters + p + '\n'
                    # parameters = '          ' + parameters.strip() + line + '\n'
                api_str = f'''\
            API name: {api_name}
            API description: {api_desc}
            API_dependency: {API_dependency}
            API_request_code:{API_request_code}
            scenario: {scenario}
            parameters:
{parameters}
            respoonse_schema: {response_schema}\n'''
                apis_prefix = apis_prefix + api_str
            api_doc = api_doc + apis_prefix
        return api_doc




if __name__ == '__main__':
    # print(CodeUtil.get_api_doc())
    APIs = '''{
        "API1": ["Search By Genre", "Advanced Movie Search"],
        "API2": ["Get Detailed Response", "Advanced Movie Search"],
        "API3": ["Title Details", "OTT Details"],
        "API4": ["Additional Title Details", "OTT Details"]
    }'''
    # print(CodeUtil.get_API_doc_for_error_judge(APIs))
    from prompt.prompt_error_judge import prompt_error_judge
    print(prompt_error_judge(CodeUtil.get_API_doc_for_error_judge(APIs),"1","1","1"))