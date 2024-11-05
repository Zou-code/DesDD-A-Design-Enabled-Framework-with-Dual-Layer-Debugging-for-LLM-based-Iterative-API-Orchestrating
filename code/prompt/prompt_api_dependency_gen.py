

def prompt_dependency(API_doc):
    """
    专门的prompt，用于生成API的调用关系
    :param API_doc:
    :return:
    """
    prompt = '''\
API Dependency Generation{
    @Persona{
        You are an experienced software architect skilled in designing API dependencies;
        Your primary task is to generate API dependency relationships based on provided API documentation;
    }
    @ContextControl{
         Understanding API dependencies is crucial for ensuring the correct order of API calls in an application;
         The integration of dependent APIs into the main codebase is essential for maintaining the application's functionality and data integrity;
    }
    @Terminology{
        API_name: The name of each API endpoint provided by the tool;
        API_description: A detailed explanation of what each API does and its role
        API_use_scenario: A typical use case or scenario where the API would be employed;
        required_parameters: The parameters that must be provided when calling the API;
        API_calling_dependency: The dependency of API calls, such as the input of one API coming from the output of another API;
        API_response_summary: A summary of the response structure and the meaning of each field in the response;
    }
    @Instruction{
        @Command According to the provided API_documentations, generate API dependency relationship descriptions for each API;
        @Rule1 For each API, first analyze its required_parameters, paying special attention to parameters like "id" that might indicate a dependency on another API;
        @Rule2 Analyze the API_response_summary and API_description of other APIs to determine if their output can fulfill the required_parameters of the current API;
        @Rule3 If a dependency is identified (e.g., an "id" or other required parameter comes from the response of another API), you need to specifically identify which\
API this API depends on, and clearly describe in dependency_description which parameter of this API come from the output of another API;
        @Rule5 If an API can be called independently (i.e., has no dependencies), please set the dependency_description to 'No calling dependency'.;
        @Rule4 The final output should be a dictionary where each API name maps to its dependency description;
    }
    @Input{
        API documentations:
        {API_documentations}
    }
    @Output example format{
        ```
        {
            "API1_name": "dependency_description",
            "API2_name": "dependency_description",
            ...
        }
        ```
    }
}    
'''
    prompt = prompt.replace('{API_documentations}', API_doc)
    return prompt
