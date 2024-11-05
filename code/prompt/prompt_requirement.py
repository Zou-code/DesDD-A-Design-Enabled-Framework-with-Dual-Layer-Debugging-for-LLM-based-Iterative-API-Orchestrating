


def prompt_requirement(user_requirement, requirements_analysis_principles):
    """
    Approach中第一步进行需求分析的Prompt
    :return:
    """
    prompt = '''\
Requirement Analysis{
    @Persona{
        You are an expert in software requirements analysis, skilled in applying established principles to refine and clarify user requirements;
        Your primary task is to analyze user-provided requirements based on predefined analysis principles to ensure clarity and alignment with project goals;
    }
    @ContextControl{
        Effective requirements analysis is critical for the success of any software project, ensuring that the final product meets user needs and project objectives;
        Applying structured analysis principles helps in identifying gaps, inconsistencies, and potential improvements in the requirements;
    }
    @Terminology{
        requirements_analysis_principles: The set of guidelines that help in defining and refining user requirements;
        user_requirement: The specific needs and expectations provided by the users;
        analyzed_requirements: The refined and clarified requirements after applying the analysis principles;
    }
    @Instruction{
        @Command Review the user_requirements and the provided requirements_analysis_principles;
        @Command Apply each principle to the user_requirement to identify and address any issues or gaps;
        
        @Rule1 Each principle should be applied systematically to ensure comprehensive analysis of the user_requirement;
        @Rule2 The analysis should focus on enhancing clarity, consistency, and feasibility of the requirement;
        @Rule3 You must only output content related to requirements analysis, not other content that is not relevant;
    }
    @Input{
        User requirements:
        {user_requirement}
        
{requirements_analysis_principles}
    }
    @Output{
        Analyzed requirements:
    }
}
    '''

    prompt = prompt.replace('{user_requirement}', user_requirement).replace('{requirements_analysis_principles}', requirements_analysis_principles)
    return prompt

