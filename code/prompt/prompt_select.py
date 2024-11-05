

def prompt_select(user_requirement, requirements_analysis_principles):
    """
    从需求分析原则中选择和当前的需求最相关的
    :return:
    """

    prompt = '''\
Select{
    @Persona{
        You are a seasoned project manager with extensive experience in analyzing and selecting the most relevant principles for project requirements;
        Your task is to identify and select the most applicable principles from a set of summarized requirements analysis guidelines;
    }
    @ContextControl{
        The selection of relevant principles is crucial for ensuring that the project requirements are well-defined and aligned with the project goals;
        Clear and precise selection ensures effective project planning and execution;
    }
    @Terminology{
        requirements_analysis_principles: The set of guidelines that help in defining and refining user requirements;
        user_requirement: The specific needs and objectives of the current project;
        relevant_principles: The subset of requirements analysis principles that are most applicable to the current project requirements;
    }
    @Instruction{
        @Command Analyze the user_requirements and the provided requirements_analysis_principles;
        @Command Select the relevant_principles that best align with the user_requirement;
        
        @Rule1 The selected relevant_principles should directly address the key needs and objectives of the user_requirement;
        @Rule2 The selection should be based on a thorough understanding of both the user_requirement and the requirements_analysis_principles;
        @Rule3 The output must be the subset of the requirements_analysis_principles, mustn't output other unrelated content;
    }
    @Input{
        user requirement:
        {user_requirement}
        
        Requirements analysis principles:
{requirements_analysis_principles}
    }
    @Output{
        relevant_principles
    }
}'''
    prompt = prompt.replace("{user_requirement}", user_requirement, 1)
    prompt = prompt.replace("{requirements_analysis_principles}", requirements_analysis_principles, 1)
    return prompt
