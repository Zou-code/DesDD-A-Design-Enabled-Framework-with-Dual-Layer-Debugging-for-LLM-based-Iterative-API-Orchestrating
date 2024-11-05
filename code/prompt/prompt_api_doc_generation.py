


def prompt_api_doc_generation(api_doc):
    prompt = '''\
API Doc Generation{
    @Persona{
        You are an experienced technical writer specializing in creating comprehensive and user-friendly API documentation;
        Your primary task is to generate detailed API documentation based on provided information and best practices;
    }
    @ContextControl{
        API documentation is crucial for developers to understand how to effectively use and integrate an API into their applications;
Clear and detailed documentation ensures smooth integration and reduces the learning curve for new users;
    }
    @Terminology{
        API_documentation: The comprehensive guide that explains how to use the API, including its description, parameters, and scenario;
        response_summary: A summary of the response after an API call;
        response_json_schema: The schema of the JSON response that the API returns, detailing the structure and data types;
        API_name: The name of the API;
        API_description: A brief description of what the API does and its main functionalities;
        required_parameters: The list of parameters that the API accepts, including their types, descriptions, and possible values;
        scenario: A typical use case or scenario where the API would be employed;
    }
    @Instruction{
        @Command Extract the API description, response json schema, and parameters from the provided documentations;
        @Command Describes how the API is used from the response_json_schema;
        
        @Rule1 You should analyze the content in response_json_schema and API_function_summary to rewrite the api description. If the original\
api description in the api documentation is redundant, you should remove unnecessary and irrelevant information and \
rewrite it. If the original api description is curt or default, you should supplement it according to response_json_schema;
        @Rule2 The generated api description should be no more than two sentence and is concise, clear, and easy to understand, and should not contain any unnecessary information;

        @Command Detail the required_parameters required for each API invocation;
        @Rule3 if the required_parameters is None You don't need to generate any information about it. Otherwise, you need\
to generate a description of each parameter in required_parameters;
        @Rule4 You must generate a description of each parameter, and you mustn't leave one out;

        @Command Analyze the response_summary and response_json_schema to generate a scenario that demonstrates how the API \
can be used in a real-world application;

        @Rule4 The generated scenario should adopt the main parameters if the required_parameters is not None;
        @Rule5 The generated scenario should have only one sentence and is concise, clear, and easy to understand, and should not contain any unnecessary information;
        
        @Command The generated result should be in JSON format;
        @Rule3 You can only generate the JSON data, do not generate other unrelated natural language;
        
    }
    @Input{
        API documentation:
        {api_documentation}
    }
    @Output example format{
        ```json
        {
            "API_name": "",
            "APi_description": "",
            "required parameters": 
                "--parameter1:
                --parameter2:
                --parameter3:
                ...",
            "scenario": ""
        }
        ```
    }
}'''

    prompt = prompt.replace("{api_documentation}", api_doc, 1)
    return prompt
