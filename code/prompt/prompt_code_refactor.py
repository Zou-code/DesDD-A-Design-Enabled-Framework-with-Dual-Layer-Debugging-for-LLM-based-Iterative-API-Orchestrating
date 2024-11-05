


def prompt_code_refactor(code, function_name, response_schema, new_API_description):
    """
    对代码进行重构，将函数名换为给定的函数名，将注释中的response_schema替换为给定的response_schema
    :param code:
    :param function_name:
    :param response_schema:
    :return:
    """

    prompt = '''\
@Persona{
    You are an experienced software developer skilled in refactoring Python code;
    Your primary task is to refactor a given Python function by changing its function name and updating the response_schema ane API_description in the function's docstring;
}
@ContextControl{
    Refactoring code to match specific naming conventions and documentation standards is crucial for maintaining code consistency and readability;
    The integration of specific function names, API_description and response schemas into the main codebase ensures that the code adheres to project standards;
}
@Terminology{
    new_function_name: The desired name for the Python function;
    new_API_description: The desired API_description to replace the original one;
    new_response_schema: The desired response schema to replace the original one;
    function_code: The original Python function code that needs to be refactored;
}
@Instruction{
    @Command According to the refactoring template defined below, refactor the given Python function code by changing the function name to the new_function_name and updating the response_schema API_description in the docstring to the new_response_schema and API_description respectively;
    @Rule1 The function name in the function_code should be replaced with the new_function_name;
    @Rule2 The original response_schema in the docstring should be replaced with the new_response_schema;
    @Rule3 The original API_description in the docstring should be replaced with the new_API_description;
    @Rule4 You can only change the function name, the response_schema and API_description in the docstring, and do not change any other part of the function code;
    @Rule5 In addition to the refactored function code and the associated comments, do not generate additional unrelated natural language or symbols;
}
@Input{
    new_function_name: 
    {new_function_name}
    new_API_description:
    {new_API_description}
    new_response_schema: 
    {new_response_schema}
    function_code:
    ```
{function_code}
    ```
}
@Output Format{
    ```
    {refactored_function_code}
    ```
}'''
    prompt = prompt.replace('{new_function_name}', function_name).replace('{new_response_schema}', response_schema).replace('{function_code}', code)
    prompt = prompt.replace('{new_API_description}', new_API_description)
    return prompt
