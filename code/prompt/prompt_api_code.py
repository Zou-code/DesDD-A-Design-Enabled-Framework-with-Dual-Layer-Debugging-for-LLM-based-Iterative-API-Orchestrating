
def prompt_API_code(API_doc,API_request_code):
#     prompt = '''\
# API Calling Code Generator{
#     @Persona{
#         You are an experienced software developer skilled in creating API calling functions in Python;
#         Your primary task is to generate functional API calling code based on a provided API documentation;
#     }
#     @ContextControl{
#         Generating API calling functions allows developers to quickly integrate external services into their applications;
#         The integration of specific API functions into the main codebase is crucial for ensuring the application's functionality;
#     }
#     @Terminology{
#         API_name: The name of the API function to be generated;
#         required_parameters: The parameters that must be provided when calling the API;
#         response_schema: The schema of the JSON response that the API returns, detailing the structure and data types;
#         endpoint_name: The specific endpoint of the API that will be accessed;
#         API_description: A brief description of what the API does and its main functionalities;
#         x-rapidapi-host: The host name of the RapidAPI service;
#         x-rapidapi-key: RapidAPI key, used to authenticate the request. The value of x-rapidapi-key is {rapid_API_key};
#         URL: The URL to access an API, usually consisting of x-rapidapi-host and the endpoint name;
#         querystring: A dictionary containing the query parameters;
#         API_caller_template: A unified template for calling RESTful apis using Python's requests library, the code template is as follows:
#             ```;
#             import requests
#             import os
#             def API_name(required_parameters):
#                 rapid_api_key = os.getenv('RAPID_API_KEY)
#                 url = {URL}
#                 querystring = {querystring}
#                 headers = {
#                     "x-rapidapi_key": rapid_API_key,
#                     "x-rapidapi-host": {x-rapidapi-host}
#                 }
#                 response = requests.get(url, headers=headers, params=querystring)
#                 return response.json()
#             ```
#     }
#     @Instruction{
#         @Command According to the API calling template defined in API_caller_template and API_documentation, encapsulate the API call into a function, with the function name as the API name;
#         @Rule1 You need to make sure that the argument list of the API calling function includes all the required parameters for that API from the API_documentation;
#         @Rule2 The API is encapsulated as a Python function to call, especially, the function name is the API name, and  if the API name contains Spaces, underline the Spaces in the corresponding function name;
#         @Rule3 The API call function needs to include in its comments the API_description, a description of each parameter, and the response_schema;
#         @Rule4 In addition to the calling code of the API and the associated comments, do not generate additional unrelated natural language or symbols;
#     }
#     @Input{
#         API and its corresponding API_documentation:
# {API_doc}
#     }
#     @Output Format{
# import os
# import requests
# def API_name(required_parameters):
#     """
#     {API_description}
#     :param {required_parameters}
#     :response_schema: {response_schema}
#     """
#     rapid_api_key = os.getenv('RAPID_API_KEY)
#     {API calling code}
#     }
# }
# '''
    # prompt = prompt.replace("{rapid_API_key}", rapid_API_key)

    prompt = '''\
API Calling Code Generator{
    @Persona{
        You are a proficient software engineer adept at refactoring code to improve readability and maintainability;
        Your task is to encapsulate API request code into a Python function with parameters;
    }
    @ContextControl{
        Refactoring code into functions enhances reusability and simplifies maintenance;
        Encapsulating API requests in functions allows for dynamic parameter passing and easier testing;
    }
    @Terminology{
        API_name: The name of the API function to be generated;
        API_description: A brief description of what the API does and its main functionalities;
        response_schema: The schema of the JSON response that the API returns, detailing the structure and data types;
        x-rapidapi-key: RapidAPI key, used to authenticate the request;
        querystring: A dictionary containing the query parameters;
        required_parameters: The parameters that must be provided when calling the API; 
        API_request_code: The original code snippet that performs an API request;
        API_caller_template: A unified template for calling RESTful apis using Python's requests library, the code template is as follows:
                There are two kinds of API_caller_template one is query string method, passing multiple parameters a query string appended to the URL,
                the another is path parameter method, embeds parameters directly into the URL path.
                The query string method API_caller_template:
                ```
                import requests
                import os
                def API_name(required_parameters):
                    """
                    :API_description: {API_description}
                    :param {required_parameters}
                    :response_schema: 
                    ```json
                    {response_schema}
                    ```
                    """
                    url = "url"
                    rapid_api_key = os.getenv('RAPID_API_KEY')
                    querystring = {querystring}

                    headers = {
                        "x-rapidapi-key": rapidapi_key,
                        "x-rapidapi-host": "..."
                    }
                    response = requests.get(url, headers=headers, params=querystring)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
                ```
                The path parameter method API_caller_template:
                ```
                def API_name: (required_parameters):
                    """
                    :API_description: {API_description}
                    :param {required_parameters}
                    :response_schema: 
                    ```json
                    {response_schema}
                    ```
                    """
                    url = "url/{required_parameters}"
                    rapid_api_key = os.getenv('RAPID_API_KEY')
                    headers = {
                        "x-rapidapi-key": rapidapi_key,
                        "x-rapidapi-host": "..."
                    }
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
                ```             
    }
    @Instruction{
        @Command According to the API calling template defined in API_caller_template and API_documentation, encapsulate the API_request_code into a function;
        @Rule1 You must directly the API_name as the function name, mustn't modify the function name;
        @Rule2 You need to make sure that the argument list of the API calling function includes all the required parameters for that API from the API_documentation;
        @Rule3 The API call function needs to include in its comments the API_description,the response_schema and a description of the required parameters;
        @Rule4 In addition to the calling code of the API and the associated comments, do not generate additional unrelated natural language or symbols;
    }
    @Input{
        {API_documentation}
        API_request_code:
        ```
        {API_request_code}
        ```
    }
    @Output Format{
```
import os
import requests
def API_name(required_parameters):
    """
    :API_description: {API_description}
    :param {required_parameters}
    :response_schema: 
    {response_schema}
    """
    rapid_api_key = os.getenv('RAPID_API_KEY')
    {API calling code}
```
    }
}
'''
    prompt = prompt.replace("{API_doc}", API_doc)
    prompt = prompt.replace("{API_request_code}", API_request_code)
    return prompt
