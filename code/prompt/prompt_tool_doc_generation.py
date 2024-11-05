import os


def prompt_tool_doc_gen(tool_doc):
    prompt = '''\
Tool Documentation Generation {
    @Persona {
        @Description {
            You are a technical writer specializing in creating detailed tool usage description \
based on tool documentation;
            You excel in translating technical specification into clear, actionable instructions for users;
        }
    }
    @ContextControl {
        @Description {
            Tool documentation includes a description of the tool, its name, and a list of endpoints;
            The task involves describing the use of the tool, functions of each API, parameters for API invocation, \
scenarios for endpoint use, and the logic of API invocation;
        }
    }
    @Terminology {
        tool_documentation: The complete set of documents that outline the tool's features, usage, and technical specifications;
        tool_name: The official name of the tool as specified in the documentation;
        tool_description: A brief summary of the tool's purpose and main functionalities;
        api_name: The name of each API endpoint provided by the tool;
        api_description: A detailed explanation of what each API does and its role within the tool;
        scenario: A hypothetical situation or use case where the API would be utilized;
        parameters: The input values required by each API for its operation;
        api_call_logical: The sequence and logic of how APIs are invoked within the tool, including dependencies and interactions;
    }
    @Instruction {
        @Command Extract the tool description, tool name, and endpoints from the provided documentations;
        @Command Describe the usage of the tool and the function of each API;
        
        @Rule1 The description of the tool should not only describe the main function of the tool, but also show \
         the function of all the apis under the tool;
        
        @Command Detail the parameters required for each API invocation;
        @Command Create scenarios that will use the endpoints and describe the logic of the API invocation in the tool;
        @Rule2 The generated result should be in JSON format;
        @Rule3 You can only generate the JSON data, do not generate other unrelated natural language;
    }
    @Input {
        tool_documentation:
        {tool_documentation}
        
    }
    @Output example format{
        ```
        {
            "tool_name":"",
            "tool_description":"",
            "api_list":[
                {
                    "api_name":"",
                    "api_description":"",
                    "scenario":"",
                    "parameters":""
                },
                {
                    "api_name":"",
                    "api_description":"",
                    "scenario":"",
                    "parameters":""
                },
                ....
            ],
            "api_call_logical":""
        }
        ```
    }
}'''
    prompt = prompt.replace('{tool_documentation}', tool_doc, 1)
    return prompt
