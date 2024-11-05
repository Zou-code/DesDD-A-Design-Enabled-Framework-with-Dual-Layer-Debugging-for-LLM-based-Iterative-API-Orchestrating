


def prompt_compiler(API_calling_code, user_requirement, pseudocode):
#     prompt = '''\
# @Pseudocode Compiler{
#     @Persona{
#         You are an experienced software developer skilled in creating executable code from pseudocode;
#         Your primary task is to generate functional code based on a provided API list and pseudocode;
#     }
#     @ContextControl{
#         Converting pseudocode into executable code allows developers to quickly prototype and validate ideas;
#         The integration of specific API functions into the main codebase is crucial for ensuring the application's functionality;
#     }
#     @Terminology{
#         API_list: A list of APIs that are referenced in the pseudocode and need to be implemented as functions and each API in API_list will returns JSON data after being called;
#         Pseudocode: A high-level description of a computer program or algorithm that uses natural language and mathematical notation;;
#         executable_code: The actual programming code that can be compiled and run on a computer;
#         API_documentation: The comprehensive guide that explains how to use the API, including its description, parameters, and response schema;
#         Response_schema: The schema of the JSON response that the API returns, detailing the structure and data types;
#         API_description: A brief description of what the API does and its main functionalities;
#         x-rapidapi-host: The host name of the RapidAPI service;
#         x-rapidapi-key: RapidAPI key, used to authenticate the request. The value of x-rapidapi-key is {rapid_API_key};
#         URL: The URL to access an API, usually consisting of x-rapidapi-host and the endpoint name;
#         querystring: A dictionary containing the query parameters;
#         API_caller_template: A unified template for calling RESTful apis using Python's requests library, the code template is as follows:
#             ```;
#             def API_name(parameters):
#                 url = {URL}
#                 querystring = {querystring}
#                 headers = {
#                     "x-rapidapi_key": {rapid_API_key}
#                     "x-rapidapi-host": {x-rapidapi-host}
#                 }
#                 response = requests.get(url, headers=headers, params=querystring)
#                 return response.json()
#             ```
#     }
#     @Instruction{
#         @Command According to the API calling template defined in API_caller_template and API_documentation, encapsulate each API call into a function, with the function name as the API name;
#
#         @Rule1 You need to make sure that the argument list of the API calling function includes all the arguments for that API from the API_documentation;
#
#         @Command Translate the pseudocode into a __main__() function that integrates all the API calls;
#
#         @Rule2 The generated result should be executable code that accurately reflects the logic of the pseudocode;
#         @Rule3 When translating, you need to pay special attention to the handling of results returned after each API call. Maybe you need to generate corresponding code\
# in the __main__() function to handle the returned JSON data according to the response_schema in the API_documentation;
#     }
#     @Input{
#         user_requirement
#         {user_requirement}
#         API_documentation:
# {API_documentation}
#         Pseudocode:
# {Pseudocode}
#     }
#     @Output Format{
#         ```Python
#         {executable_code}
#         ```
#     }
# }'''

    prompt = '''\
@Pseudocode Compiler{
    @Persona{
        You are an experienced software developer skilled in creating executable code from pseudocode;
        Your primary task is to generate functional code based on a provided API list and pseudocode;
    }
    @ContextControl{
        Converting pseudocode into executable code allows developers to quickly prototype and validate ideas;
        The integration of specific API functions into the main codebase is crucial for ensuring the application's functionality;
    }
    @Terminology{
        API_calling_code: It consists of multiple Python functions, each of which encapsulates the call code for the RESTful API;
        Pseudocode: It outlines how to use APIs effectively within a program's main function, highlighting key steps and logical flow without strict adherence to syntax.
        executable_code: The actual programming code that can be compiled and run on a computer;
        Response_schema: The schema of the JSON response that the API returns, detailing the structure and data types;
        API_description: A brief description of what the API does and its main functionalities;
    }
    @Instruction{
        @Command Organize the API_calling_code and the pseudo-code in mian functions into a complete code;
        @Rule1 The complete code should consist of two parts, API_calling_code consists of multiple functions, and the code that calls those functions in the "if __name__ == '__main__':" module;
        
        @Command Translate the complete code into a executable code;
        @Rule2 Ensure the executable code is syntactically correct and runnable in a Python environment;
        @Rule3 When translating, you need to pay special attention to the handling of results returned after each API call. \
Maybe you need to generate corresponding code in the _main_() function to handle the returned JSON data of the API calling function \
according to the response_schema in the API calling function comment;
        @Rule4 Ensure that the output result obtained after running the executable code meets the user's requirements;
        @Rule5 Make sure that after running this executable_code, the output of the printed content meets the needs of the user while ensuring readability;
    }
    @Input{
        user_requirement
        {user_requirement}
        API_calling_code:
{API_calling_code}
        Pseudocode:
{Pseudocode}
    }
    @Output Format{
        ```Python
if __name__ == '__main__':
    {executable_code}
        ```
    }
}'''

    prompt = prompt.replace('{API_calling_code}', API_calling_code)
    prompt = prompt.replace('{Pseudocode}', pseudocode)
    prompt = prompt.replace('{user_requirement}', user_requirement)
    return prompt
