import os


class Config:
    # model_embedding = "text-embedding-3-small"
    model_embedding = "text-embedding-ada-002"

    react_model = 'gpt-4'
    react_max_turn = 20

    encoding_name = "cl100k_base"

    tool_nums = 3

    # 最后一次扩展，生成了API调用依赖的API文件路径
    api_last_expan_path = "../data/apis_with_dependency.csv"
    # 第一次扩展，即只生成json schema的API的文件路径
    api_first_expan_path = "../data/new_apis_with_schema.csv"
    # 进行了第二次扩展，但还没合并到总api库中的文件路径
    api_second_expan_path = "../data/apis_new.csv"
    # 总api库的文件路径
    api_path = "../data/apis.csv"
    # 新加入的，还没有进行任何扩展的API的文件路径
    api_original_path = "../data/original_apis.csv"
    # 原始的API库，每次新加入的APIs，都要merge到这里
    api_original_base_path = "../data/original_data/original_apis_base.csv"


    # 已经进行了扩展，扩展完毕，但还没合并到总tool库的文件路径
    tool_expan_path = "../data/tools_new.csv"
    # 总tool库的文件路径
    tool_path = "../data/tools.csv"
    # 新加入的，还没有进行任何扩展的tool的文件路径
    tool_original_path = "../data/original_tools.csv"
    # 原始的Tool库，每次新加入的tools，都要merge到这里
    tool_original_base_path = "../data/original_data/original_tools_base.csv"

    # 出错文件管理
    # API的response schema生成报错记录
    error_apis_schema = "../logs/error_log/error_apis_schema.csv"
    # API 第一次扩展生成报错记录
    error_apis_new = "../logs/error_log/error_apis_new.csv"
    # Tool 扩展生成报错记录
    error_tools_new = "../logs/error_log/error_tools_new.csv"

    # 可运行代码的临时保存路径
    runnable_code_temp_path = "./temp_output/executable_code.py"