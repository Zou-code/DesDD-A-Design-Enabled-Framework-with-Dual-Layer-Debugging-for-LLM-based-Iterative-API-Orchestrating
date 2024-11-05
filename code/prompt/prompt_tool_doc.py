

def prompt_tool_doc(tool_doc):
    """
    This is the doc for prompt_tool.
    """
    prompt = '''\
Tool Doc Generation{
    @Persona{
        You are a technical writer specializing in creating detailed tool usage description \
based on tool documentation;
        You excel in translating technical specification into clear, actionable instructions for users;
    }
    @ContextControl{
        Tool documentation includes a concise description of the tool, its name, and a list of endpoints;
        The task involves describing the use of the tool, functions of each API, parameters for API invocation, \
scenarios for endpoint use, and the logic of API invocation;
    }
    @Terminology{
        tool_documentation: The complete set of documents that outline the tool's features, usage, and technical specifications;
        tool_name: The official name of the tool as specified in the documentation;
        tool_description: A brief summary of the tool's purpose and main functionalities;
        API_name: The name of each API endpoint provided by the tool;
        API_description: A detailed explanation of what each API does and its role
        API_use_scenario: A typical use case or scenario where the API would be employed;
        API_response_summary: A summary of the response structure and the meaning of each field in the response;
    }
    @Instruction{
        @Command Analyze the tool_documentation to extract the tool_name, API_names, and their respective API_descriptions;
        @Command Based on the description of all apis under the tool, generate the main function description of the tool
        
        @Rule1 The description of the tool should not only describe the main function of the tool, but also show \
the function of all the apis under the tool;
        @Rule2 The generated tool_description should be concise, clear, and easy to understand, and should not contain any unnecessary information;
        
        @Rule3 The generated result should be in JSON format;
        @Rule4 You can only generate the JSON data, do not generate other unrelated natural language;
    }
    @Input{
        tool documentation:
        {tool_documentation}
    }
    @Output example format{
        ```
            {
                "tool_name": "",
                "tool_description": "",
            }
        ```
    }
}    
    '''
    return prompt.replace("{tool_documentation}", tool_doc, 1)