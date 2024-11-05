def prompt_error_judge(API_documentation, pseudocode, executable_code, error_message, user_requirement):
    prompt = '''\
Error Judge{
    @Persona{
        You are an experienced software developer skilled in debugging and code analysis;
        Your primary task is to analyze code issues based on provided API documentation, pseudocode, runnable code, and error messages;
    }
    @ContextControl{
        Analyzing code issues helps developers identify and fix problems in their applications;
        The distinction between design-level and coding-level errors is crucial for effective debugging;
    }
    @Terminology{
        user_requirement: The specific task or functionality that the user wants to achieve;
        API_documentation: The documentation that specifies the requirements and constraints of the API;
        pseudocode: The high-level description of the algorithm or logic, which is not directly executable and the pseudocode consists of two parts: 1.The selected APIs, which are chosen to fulfill the user requirements,
2.The pseudocode for invoking these selected APIs to fulfill the user requirement.;
        runnable_code: The actual code that is translated from the pseudocode and is executable;
        error_message: The error message generated when running the runnable code;
        error_level: Indicates the level of the error, which can be either design-level or coding-level;
        design_level: Indicates an issue with the pseudocode, such as 1.logical errors 2.The selected API cannot fulfill the user's requirements and needs to be re-selected\
3.Not considering the dependencies of certain API calls 4.Due to the  selected_APIs belonging to multiple tools, conflicts arise in the collaboration between APIs.;
        coding_level: Indicates an issue with the runnable code, such as syntax errors or incorrect implementation of the pseudocode;
        error_report: A detailed report that specifies the level of the error (design or coding) and the specific violations of the API documentation;
    }
    @Instruction{
        @Command According to the provided API_documentation, pseudocode, runnable_code, and error_message, determine the level of the error (design or coding) and generate an error_report;
        @Rule1 Analyze the pseudocode to ensure it adheres to the API_documentation;
        @Rule2 Analyze the runnable_code to ensure it correctly implements the pseudocode and adheres to the API_documentation;
        @Rule3 If the error is at the design level, specify the logical errors or API requirement violations in the pseudocode;
        @Rule4 If the error is at the coding level, specify the syntax errors or incorrect implementation details in the runnable_code;
        @Rule5 The error_report should include the level of the error and a detailed description of the violations of the API documentation;
        @Rule6 In addition to the error_report, do not generate additional unrelated natural language or symbols;
    }
    @Input{
        API_documentation: 
        {API_documentation}
        user_requirement:
        {user_requirement}
        pseudocode: 
        {pseudocode}
        runnable_code:
        {executable_code}
        error_message: 
        {error_message}
    }
    @Output Format{
        ```
        {
            "error_level", "{design_level} or {coding_level}",
            "error_report", "{error_report}"
        }
        ```
    }    
}
'''
    prompt = prompt.replace('{API_documentation}', API_documentation).replace('{pseudocode}',pseudocode)
    prompt = prompt.replace('{executable_code}', executable_code).replace('{error_message}', error_message)
    prompt = prompt.replace('{user_requirement}', user_requirement)
    return prompt

