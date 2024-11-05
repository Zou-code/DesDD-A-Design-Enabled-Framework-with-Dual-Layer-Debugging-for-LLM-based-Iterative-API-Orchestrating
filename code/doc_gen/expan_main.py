import pandas as pd
from tool_expan import ToolExpan
from tqdm import tqdm
import json
from config import Config
import numpy as np
from util.code_util import CodeUtil
from tool_embedding import Embedding


# WARN 下面这个代码已经被弃用了
def tool_api_desc_expan():
    """
    对tool的csv文件进行遍历，调用LLM生成文档描述，并对返回的json结果进行解析，获取tool的描述和api的描述，保存到新的csv文件中
    :return:
    """

    # 读取原始的tool和api的csv文件，此时读取的是没有经过扩展的文件的API
    df_original_tools = pd.read_csv(Config.tool_original_path)
    df_apis_with_schema = pd.read_csv(Config.api_first_expan_path)

    # df_new_tools = pd.DataFrame(columns=['tool_name', 'tool_description', 'head', 'api_call_logical'])
    # df_new_apis = pd.DataFrame(
    #     columns=['tool_name', 'api_name', 'endpoint_name', 'api_description', 'query_string', 'required_parameters',
    #              'scenario', 'response_example', 'json_schema'])

    for _, row_tool in tqdm(iterable=df_original_tools.iterrows(), total=len(df_original_tools)):

        # 进行扩展后，需要保存的位置
        df_new_tools = pd.read_csv(Config.tool_expan_path)
        df_new_apis = pd.read_csv(Config.api_second_expan_path)

        tool_name = row_tool['tool_name']
        json_text = ToolExpan.Tool_doc_expan(tool_name)
        json_text = json_text.strip()[3:-3]
        json_data = json.loads(json_text)

        # 对json数据进行处理，获取不同部分的信息
        tool_description = json_data.get('tool_description')
        api_call_logical = json_data.get('api_call_logical')
        head = row_tool['head']
        row_new_tool = {
            'tool_name': tool_name,
            'tool_description': tool_description,
            'head': head,
            'api_call_logical': api_call_logical
        }

        # 将新的工具信息添加到df_new_tools数据框中
        df_new_tools = df_new_tools.append(row_new_tool, ignore_index=True)

        # TODO 保存扩展后的Tools文件到一个一新的csv 文件中
        df_new_tools.to_csv('../data/new_tools.csv', index=False)

        # 对当前tool下的API的信息进行逐个收集并处理
        api_list = json_data.get('api_list')
        for api in api_list:
            api_name = api.get('api_name')
            api_description = api.get('api_description')
            scenario = api.get('scenario')
            parameters = api.get('parameters')

            original_api = df_apis_with_schema.loc[
                df_apis_with_schema['api_name'] == api_name and df_apis_with_schema['tool_name'] == tool_name]

            endpoint_name = original_api['endpoint_name'].values[0]
            query_string = original_api['query_string'].values[0]
            response_example = original_api['response_example'].values[0]
            API_function_summary = original_api['API_function_summary'].values[0]

            row_new_api = {
                'tool_name': tool_name,
                'api_name': api_name,
                'endpoint_name': endpoint_name,
                'api_description': api_description,
                'query_string': query_string,
                'required_parameters': parameters,
                'scenario': scenario,
                'response_example': response_example,
                'json_schema': 'None',
                'API_function_summary': API_function_summary
            }

            df_new_apis = df_new_apis.append(row_new_api, ignore_index=True)

            # 保存扩展后的api文件到一个新的csv
            df_new_apis.to_csv('../data/new_apis.csv', index=False)


def response_schema_to_csv():
    """
    调用LLM根据生成api的 json_schema，并将结果保存到新的csv文件中
    :param path_apis_csv: 保存api的csv信息的文件路径
    :return:
    """
    df_apis = pd.read_csv(Config.api_original_path)

    for _, row_api in tqdm(iterable=df_apis.iterrows(), total=len(df_apis), desc='API response schema generation'):
        try:
            df_apis_with_schema = pd.read_csv('../data/new_apis_with_schema.csv')
            json_data = row_api['response_example']
            response = ToolExpan.json_schema_generation(json_data)
            response_summary = response.split('########################')[-1]
            json_schema = response.split('########################')[0]
            row_api['json_schema'] = json_schema
            row_api['response_summary'] = response_summary.strip()

            df_apis_with_schema = pd.concat([df_apis_with_schema, row_api.to_frame().T], ignore_index=True)

            df_apis_with_schema.to_csv('../data/new_apis_with_schema.csv', index=False)

        except Exception as e:
            print(f"Error processing row {row_api['api_name']}: {e}")
            df_error = pd.read_csv(Config.error_apis_schema)
            df_error = pd.concat([df_error, row_api.to_frame().T], ignore_index=True)
            df_error.to_csv(Config.error_apis_schema, index=False)


def api_expan_to_csv():
    """
    调用LLM根据生成api的描述，并将结果保存到新的csv文件中
    需要新插入的列有：api_description, required_parameters, scenario
    :return:
    """
    df_apis_with_schema = pd.read_csv(Config.api_first_expan_path)

    for _, row in tqdm(iterable=df_apis_with_schema.iterrows(), total=len(df_apis_with_schema), desc='API second expan'):
        try:
            df_apis_new = pd.read_csv(Config.api_second_expan_path)
            required_parameters = row['required_parameters']

            # 确保当参数为空的情况下的处理
            if isinstance(required_parameters, float) and np.isnan(required_parameters):
                parameters_line = []
            elif isinstance(required_parameters, str):
                parameters_line = required_parameters.split('\n')
            else:
                parameters_line = []

            parameters_str = ''
            if not parameters_line:
                parameters_str = 'None'
            else:
                for line in parameters_line:
                    parameters_str = parameters_str + f'        {line}\n'

            api_doc = f'''\
API_name: {row['api_name']}
response_summary: {row['response_summary']}
API_description: {row['api_description']}
required_parameters: {parameters_str} 
'''

            expan_api_doc = ToolExpan.API_doc_generation(api_doc)
            expan_api_doc = json.loads(expan_api_doc)

            row['api_description'] = expan_api_doc.get("API_description")
            row['required_parameters'] = expan_api_doc.get("required_parameters")
            row['scenario'] = expan_api_doc.get("scenario")

            df_apis_new = pd.concat([df_apis_new, row.to_frame().T], ignore_index=True)

            df_apis_new.to_csv(Config.api_second_expan_path, index=False)
        # df_apis_new.to_csv('../data/apis_new.csv', index=False)

        except Exception as e:
            # 异常处理，将生成失败的api保存到记录错误的csv文件中
            print(f"Error processing row {row['api_name']}: {e}")
            df_error = pd.read_csv(Config.error_apis_new)
            df_error = pd.concat([df_error, row.to_frame().T], ignore_index=True)
            df_error.to_csv(Config.error_apis_new, index=False)

# TODO 加上异常处理，保存下生成失败的Tool
def tool_expan_to_csv():
    """
    对tool的文档信息进行改写,生成从全局考虑的tool_description
    :return:
    """
    df_original_tools = pd.read_csv(Config.tool_original_path)

    for _, row in tqdm(iterable=df_original_tools.iterrows(), total=len(df_original_tools), desc="Tool expan"):
        try:
            df_tools_new = pd.read_csv(Config.tool_expan_path)
            tool_name = row['tool_name']
            df_apis = pd.read_csv(Config.api_second_expan_path)

            # 获取当前tool下的所有的API
            df_selected_apis = df_apis.loc[df_apis['tool_name'] == tool_name]
            api_doc = ''
            for _, row_api in df_selected_apis.iterrows():
                api_doc = api_doc + f'''\
    API_name: {row_api['api_name']}
    API_description: {row_api['api_description']}
    API_use_scenario: {row_api['scenario']}
    API_response_summary: {row_api['response_summary']}
        
'''

            tool_doc = f'''\
tool_name: {row['tool_name']}
tool_description: {row['tool_description']}
APIs:
{api_doc}
    '''
            expan_tool_doc = ToolExpan.tool_doc_generation(tool_doc)
            # expan_tool_doc = CodeUtil.json_string_extract(expan_tool_doc)
            expan_tool_doc = json.loads(expan_tool_doc)
            # API_calling_dependency = expan_tool_doc.get("API_calling_dependency")
            # # 将生成出来的每个API的调用依赖关系保存到csv文件中  ../data/apis_with_dependency.csv
            # for name, dependency in API_calling_dependency.items():
            #     df_selected_api = df_apis.loc[(df_apis['tool_name'] == tool_name) & (df_apis['api_name'] == name)]
            #     for _,select_api in df_selected_api.iterrows():
            #         select_api['calling_dependency'] = dependency
            #         df_apis_depen = pd.read_csv(Config.api_last_expan_path)
            #         df_apis_depen = pd.concat([df_apis_depen, select_api.to_frame().T], ignore_index=True)
            #         df_apis_depen.to_csv(Config.api_last_expan_path, index=False)

            row['tool_description'] = expan_tool_doc.get("tool_description")
            # row['api_call_logical'] = expan_tool_doc.get("API_call_logical")

            df_tools_new = pd.concat([df_tools_new, row.to_frame().T], ignore_index=True)

            df_tools_new.to_csv(Config.tool_expan_path, index=False)
        except Exception as e:
            print(f"Error processing row {row['tool_name']}: {e}")
            df_error = pd.read_csv(Config.error_tools_new)
            df_error = pd.concat([df_error, row.to_frame().T], ignore_index=True)
            df_error.to_csv(Config.error_tools_new, index=False)



def merge_two_df(path1, path2, save_path):
    """
    将两个dataframe合并为一个dataframe
    :param path1: 第一个csv文件的地址
    :param path2: 第二个csv文件的地址
    :param save_path: 合并之后的文件，保存的地址
    :return:
    """
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    df = pd.concat([df1, df2], ignore_index=True)

    df.to_csv(save_path, index=False)

def API_dependency_to_csv():
    """
    生成API的调用关系，并将API的调用依赖关系保存到csv文件中
    :return:
    """
    df_tools = pd.read_csv(Config.tool_expan_path)
    df_apis = pd.read_csv(Config.api_second_expan_path)
    for _, row_tools in tqdm(df_tools.iterrows(), total=len(df_tools), desc="API_dependency"):
        tool_name = row_tools['tool_name']
        # 获取当前tool下的所有的API
        df_selected_apis = df_apis.loc[df_apis['tool_name'] == tool_name]
        api_doc = ''
        for _, row_api in df_selected_apis.iterrows():
            api_doc = api_doc + f'''\
            API_name: {row_api['api_name']}
            API_description: {row_api['api_description']}
            API_use_scenario: {row_api['scenario']}
            API_response_summary: {row_api['response_summary']}
            API_required_parameters:
            {row_api['required_parameters']}

'''
        API_dependency = ToolExpan.API_dependency_generation(api_doc)
        API_dependency = json.loads(API_dependency)
        for name, dependency in API_dependency.items():
            df_selected_api = df_apis.loc[(df_apis['tool_name'] == tool_name) & (df_apis['api_name'] == name)]
            for _,select_api in df_selected_api.iterrows():
                select_api['calling_dependency'] = dependency
                df_apis_dependency = pd.read_csv(Config.api_last_expan_path)
                df_apis_dependency = pd.concat([df_apis_dependency, select_api.to_frame().T], ignore_index=True)
                df_apis_dependency.to_csv(Config.api_last_expan_path, index=False)


if __name__ == '__main__':

    # 将爬取的信息merge到original_apis.csv文件中
    # merge_two_df(Config.api_original_path, '../doc_gen/apis_data.csv', Config.api_original_path)

    # 第零步，在进行生成之前先需要将original_tools.csv与original_apis.csv分别合并到original_data中
    # merge_two_df(Config.tool_original_base_path, Config.tool_original_path, Config.tool_original_base_path)
    # merge_two_df(Config.api_original_base_path, '../doc_gen/apis_data_v3.csv', Config.api_original_base_path)

    # 第一步：生成API的response schema
    response_schema_to_csv()
    # # 第二步：生成每个API的详细描述
    # api_expan_to_csv()
    # # WARN: 第三步不是merge，需要等到tool生成的时候将calling_dependency 生成出来之后再进行merge
    #
    # # 第三步：生成Tool的描述
    # tool_expan_to_csv()
    #
    # # 第四步：根据Tool进行遍历，生成每个API的调用依赖关系y
    # API_dependency_to_csv()
    #
    # # 第五步：将生成好的API详细描述的csv合并到最终的API的csv中
    # merge_two_df(Config.api_path, Config.api_last_expan_path, Config.api_path)
    # # 第六步：将生成好的Tool的描述的csv合并到最终的Tool的csv中
    # merge_two_df(Config.tool_path, Config.tool_expan_path, Config.tool_path)
    # # 第七步: 对tools的文档信息进行embedding
    Embedding.get_embedding()
    # pass