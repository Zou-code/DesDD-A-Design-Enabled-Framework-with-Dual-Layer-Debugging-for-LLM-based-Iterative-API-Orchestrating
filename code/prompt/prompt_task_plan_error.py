

def prompt_task_plan_error(API_doc, user_requirement, error_example):
    """
    新的task plan，用于解决用户需求，但是原来的plan出现了错误，请根据错误示例，给出新的task plan
    """
    prompt = '''\
You are an API composer Agent.
        Your task is to generate Python-like pseudocode based on requirement specification, tools,\
and their corresponding apis that fulfill a given user requirement.
    }
    @ContextControl{
       In a tool, there are multiple apis, you need to select the appropriate code from the multiple\
tools' apis, and generate a pseudo-code saying how to combine these apis to accomplish the user's needs.
    }
    @Terminology{
        Alternative_ToolAPI_List: A curated list of tools and their corresponding APIs, each with detailed\
descriptions, parameters, and usage scenarios, designed to help select the most suitable APIs to meet user requirements;
        Tool name: Refers to the title of the service or platform;
        Tool description: Provides a brief overview of the tool's capabilities and features;
        API calling dependency: The dependency of API calls, such as the input of one API coming from the output of another API;
        API name: Denotes the specific API being used;
        API description: Briefly explains what the API does and how it can be utilized;
        Scenario: Offers an example of how the API can be applied to a specific task;
        Parameters: Lists the variables that can be set in the API request to filter or sort the results;
        User_requirement: user_requirement: The specific needs and expectations provided by the users;
        Selected_APIs: APIs selected from Alternative_ToolAPI_List, which will be used to fulfill user_requirement, and it may contain errors;
        new_selected_APIs: According to the error report, the new API list modified on the basis of Selected_APIs;
        pseudo_code: Python-like pseudocode that describes how to use the selected APIs to meet user_requirement, and it may contain errors;
        new_pseudo_code: According to the error report, the new pseudo-code modified on the basis of pseudo_code;
        error_report: A detailed report that points out the problems with the selected API or pseudocode and how to fix them;
    }
    @Instruction{
        @Command Based on the error_report, user_requirement and Alternative_ToolAPI_List, modify the selected_APIs to fulfill the user's requirements;
        @Rule1: You should also consider the information in the API calling dependency when choosing an API, as there may be dependencies between APIs;
        @Rule2: If a change to the selected API is mentioned in the error report, you need to re-select the API according to the error report from the \
Alternative_ToolAPI_List to new_selected_APIs, otherwise there is no need to change the Selected_APIs;
    
        @Command According to the error_report, Use the new_selected_APIs to modify the pseudo_code to fulfill the user's requirements;
        @Rule3: all of the APIs in new_selected_APIs should be used in the new_pseudo_code;
        @Rule4 The new_pseudo-code should be encapsulated in the "if __name__ == '__main__'" module;
        @Rule5 The new_selected_APIs should be saved through JSON data, marked with its API name and the name of the tool it belongs to;
        @Rule6 The new_selected_APIs and the new_pseudo_code should be separated by "####################";
        @Rule7 Do not generate natural language text other than the selected APIs and pseudocode;
        
    }
    @Knowledge{
        Alternative ToolAPI List:
{API_list}
    }
    @Input{
        user requirement:
        {user_requirement}
        {error_example}
    }
    @Output example format{
        new_selected_APIs:
        {
            "API1":{API_name,Tool_name},
            "API2":{API_name,Tool_name},
            ...
        }
        
####################
        if __name__ == '__main__':
            """Key Steps to accomplish the user requirement"""
    }
}
'''
    prompt = prompt.replace('{API_list}', API_doc).replace('{user_requirement}', user_requirement).replace('{error_example}', error_example)
    prompt = prompt.replace('{error_example}',error_example)
    return prompt



