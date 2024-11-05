import re

import pandas as pd
import json
import os
from util.llm_util import LLM_util
from util.code_util import CodeUtil
from prompt.prompt_select import prompt_select
from prompt.prompt_requirement import prompt_requirement
from prompt.prompt_task_plan import prompt_implement
from prompt.prompt_error_judge import prompt_error_judge
from prompt.prompt_task_plan_error import prompt_task_plan_error
from approach.retrieval import Retrieval
from prompt.prompt_compiler import prompt_compiler
from prompt.prompt_code_repair import prompt_repair
from config import Config
import time
import logging
import subprocess

# 获取当前时间并格式化
current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

# 定义日志文件名
log_filename = f"../logs/log_SE_code_gen/log_{current_time}.log"

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),  # 文件处理器
        logging.StreamHandler()  # 控制台处理器
    ]
)

class SEFramework:
    def __init__(self):
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model = LLM_util()
        self.retrieval = Retrieval()
        # self.requirement_principles = [
        #     "        1. What are the key assumptions underlying this problem?",
        #     "2. How can I simplify the problem so that it is easier to solve?",
        #     "3. How can I break down this problem into smaller, more manageable parts?",
        #     "4. What are the potential obstacles or challenges that might arise in solving this problem? ",
        #     "5. Are there any stakeholders or individuals who are directly affected by the problem? What are their perspectives and needs?",
        #     "6. How can progress or success in solving the problem be measured or evaluated?",
        #     "7. Does the problem involve decision-making or planning, where choices need to be made under uncertainty or with competing objectives?",
        #     "8. Develop detailed use cases that outline how users will interact with the system to achieve their goals.",
        #     "9. Write user stories and scenarios that describe the actions and motivations of users. This can aid in understanding the context in which the system will be used.",
        #     "10. Ensure each functional and non-functional requirement has a clearly defined objective that aligns with the overall project goals. ",
        #     "11. For each task, assign responsibilities clearly to team members based on their skills and the needs of the task.",
        #     "12. Plan tasks with an eye on the future, ensuring that solutions are sustainable and scalable. Consider how the tasks will fit into the long-term goals of the organization and prepare for possible expansions or upgrades. ",
        #     "13. Plan tasks with a focus on user-centric design principles, ensuring that the end product meets the usability and experience expectations of the end-users.",
        #     "14. Plan for tasks that ensure the system is compatible and can integrate smoothly with existing or external systems.",
        #     "15. Prioritize tasks based on the critical path for functional requirements, ensuring that core functionalities are developed and tested first."
        # ]

        self.requirement_principles = [
            "1.Establish clear, measurable objectives to guide the development process and evaluate success.",
            "2.Involve all relevant stakeholders early in the analysis to gather diverse inputs and maintain alignment throughout the project lifecycle.",
            "3.Prioritize the needs and experiences of end-users to ensure the solution is user-centric and practical.",
            "4.Maintain traceability of requirements from inception through to implementation to ensure all needs are met and changes are managed effectively.",
            "5.Use an iterative approach to refine requirements through continuous feedback and validation.",
            "6.Evaluate the technical feasibility and risks associated with each requirement to ensure realistic planning and execution.",
            "7.Analyze and prioritize requirements based on their potential value to the business or project goals.",
            "8.Design requirements to accommodate changes and future expansions without significant reworks.",
            "9.Detailed use cases are provided, such as a user inputting a theme and receiving a list of movies fitting that theme available on selected streaming platforms.",
            "10.The requirement is broken down into specific functionalities, such as identifying movies based on themes and checking their availability on streaming platforms.",
            "11.User stories are created to capture the perspective of end-users and their interactions with the system, such as planning a movie night.",
            "12.Requirements should be expressed clearly and simply to ensure they are understood by all stakeholders.",
            "13.Ensure all requirements are in alignment with the overarching business strategy to support organizational objectives.",
            "14.Consider the broader system and operational environment when analyzing requirements to understand interdependencies and impacts.",
            "15.Design requirements to accommodate future growth and changes in technology without substantial alterations.",
            "16.Adopt an agile mindset to allow for flexibility in changing requirements as projects evolve and new insights are gained.",
            "17.Each requirement should have a clearly defined purpose that contributes directly to the project goals.",
            "18.Write requirements in a language that is easy to understand for all project stakeholders, avoiding technical jargon where possible.",
            "19.Aim for consensus among all key stakeholders on the importance and interpretation of each requirement.",
            "20.Formulate requirements in a way that their fulfillment can be objectively tested and verified.",
            "21.Each requirement should be unique and avoid overlap with others to prevent duplication and conflicts.",
            "22.Requirements should be concise, providing enough detail without unnecessary verbosity."
        ]


    def select_requirement_principles(self, user_requirement) -> str:
        """
        第一步：从需求分析的原则中选择适合当前需求的
        :param user_requirement: 用户需求
        :return: 选择了的需求分析原则
        """

        principles_str = "\n        ".join(self.requirement_principles)
        prompt = prompt_select(user_requirement, principles_str)

        logging.info("选择需求分析原则的prompt\n" + prompt)
        # selected_principles = self.model.model_deepseek_chat(prompt)
        selected_principles = self.model.model_gpt4o(prompt)
        return selected_principles

    def requirement_analysis(self, selected_principles, user_requirement) -> str:
        """
        第二步：调整选择的推理模块，使其更具体地适用于任务
        :param selected_principles: 选择了的需求分析原则
        :param user_requirement: 用户需求
        :return:
        """
        requirement_principles = selected_principles.split("\n")
        requirement_principles = "        \n".join(requirement_principles)
        prompt = prompt_requirement(user_requirement, requirement_principles)

        # analyzed_requirements = self.model.model_deepseek_chat(prompt)
        analyzed_requirements = self.model.model_gpt4o(prompt)
        return analyzed_requirements

    def task_plan(self, requirement_specification, user_requirement, tool_API_doc ,error_example=None):
        """
        第三步
        :param requirement_specification:
        :param user_requirement:
        :param tool_API_doc:
        :param error_example:
        :return:
        """
        if error_example is None:
            prompt = prompt_implement(requirement_specification, tool_API_doc, user_requirement)
        else:
            prompt = prompt_task_plan_error(requirement_specification, tool_API_doc, user_requirement, error_example)
        logging.info("进行任务规划，生成伪代码的prompt\n" + prompt)
        # plan_pseudocode = self.model.model_deepseek_coder(prompt)
        plan_pseudocode = self.model.model_gpt4o(prompt)
        return plan_pseudocode

    def pseudocode_compiler(self, user_requirement, API_calling_code, pseudocode: str):
        """
        第四步：将伪代码转化为可执行的代码
        :param API_calling_code: API调用代码，其实就是多个Python函数
        :param user_requirement: 用户需求
        :param pseudocode: 伪代码
        :return: 可执行的代码
        """
        prompt = prompt_compiler(API_calling_code, user_requirement, pseudocode)
        runnable_code = self.model.model_gpt4o(prompt)
        # TODO 生成出来的代码可能会包含一些其他的字符，需要进一步处理
        return runnable_code

    def error_judge(self, error_message, pseudocode, runnable_code, API_documentation, user_requirement):
        """
        第五步：判断代码是否正确
        :param pseudocode: 伪代码
        :param error_message: 错误信息
        :param runnable_code: 可执行的代码
        :param API_documentation: 选中了的API的文档
        :return: 包含error_level 和 error_report 的json数据
        """
        prompt = prompt_error_judge(API_documentation, pseudocode, runnable_code, error_message,user_requirement)
        error_result = self.model.model_gpt4o(prompt)
        error_result = CodeUtil.json_string_extract(error_result)
        return error_result

    def code_repair(self, runnable_code, error_message, error_documentation, API_documentation):
        """
        第六步：修复代码
        :param API_documentation:
        :param runnable_code: 可执行的代码
        :param error_message: 错误信息
        :param error_documentation: 错误文档
        :return: 修复后的代码
        """
        prompt = prompt_repair(runnable_code, error_message, error_documentation, API_documentation)
        repaired_code = self.model.model_gpt4o(prompt)
        return repaired_code


    @staticmethod
    def get_API_calling_code(APIs:dict):
        """
        根据选中的APIs打开对应的文件，获取API的调用代码
        :param APIs:  JSON格式的选中的API的及API对应的tool  {"API1":["API_name", "tool_name"], ...}
        :return: 多个函数，API的调用代码
        """
        # APIs = json.loads(APIs)
        API_calling_code = ''
        for value in APIs.values():
            tool_name = value[1].strip().replace(' ', '_')
            API_name = value[0].strip().replace(' ', '_')

            API_code_path = f'../Tools/{tool_name}/{API_name}.py'
            try:
                API_calling_code = API_calling_code + open(API_code_path, 'r', encoding='utf-8').read()
            except Exception as e:
                logging.error(e, exc_info=True)
        return API_calling_code

    @staticmethod
    def code_run(runnable_code):
        """
        将模型生成的可运行代码保存到文件中，并执行
        :param runnable_code:
        :return:
        """
        # 将可运行的代码保存到文件中 ./temp_output/executable_code.py
        with open(Config.runnable_code_temp_path, 'w', encoding='utf-8') as f:
            f.write(runnable_code)
            f.flush()
            f.close()

        result = subprocess.run(
            ["python", "./temp_output/executable_code.py"],
            stdout=subprocess.PIPE,  # 捕获标准输出
            stderr=subprocess.PIPE,  # 捕获标准错误
            text=True,  # 以文本模式读取输出
            encoding='utf-8'  # 指定编码方式为 UTF-8
        )
        return result

    # 如人饮水，冷暖自知吧
    def SE_framework(self, user_requirement):
        # Note：Step1选择合适的推理模块
        selected_principles = self.select_requirement_principles(user_requirement)
        logging.info('Step1: 选择需求分析的原则\n%s',selected_principles)

        # Note：Step2：调整选择的推理模块，使其更具体地适用于任务
        analyzed_requirement = self.requirement_analysis(selected_principles, user_requirement)
        logging.info('Step2:根据选择的需求分析原则进行分析\n%s', analyzed_requirement)

        ERROR = True  # 标识是否有错误发生，如果有错误发生，第一次执行时，默认有错
        FIRST_RUN = True # 第一次运行，即在task plan阶段不必传入error_report
        error_report = ''

        # 调用方法获取最相似的top k个API
        df_possible_tools = self.retrieval.tool_retrieval(user_requirement, Config.tool_nums)
        tool_API_doc = CodeUtil.get_api_doc(df_possible_tools)

        while ERROR:
            # plan_pseudocode = ''
            if FIRST_RUN:
                # Note：Step3：根据调整后的需求规约，生成伪代码
                plan_pseudocode = self.task_plan(analyzed_requirement, user_requirement, tool_API_doc)
                logging.info('第一次进行task plan，生成伪代码\n%s', plan_pseudocode)
                FIRST_RUN = False
            else:
                error_example = CodeUtil.get_error_example(pseudocode, error_report, tool_API_doc)
                plan_pseudocode = self.task_plan(analyzed_requirement, user_requirement, tool_API_doc, error_example)
                logging.info('在design层面上进行修改，生成新的伪代码\n%s', plan_pseudocode)

            selected_APIs = plan_pseudocode.split("####################")[0].strip()
            selected_APIs = CodeUtil.string_clean(selected_APIs)
            logging.info('selected_APIs:\n%s', selected_APIs)
            APIs = json.loads(selected_APIs)
            # APIs = json.loads(plan_pseudocode.split("####################")[0].strip())
            pseudocode = plan_pseudocode.split("####################")[-1].strip()
            pseudocode = CodeUtil.string_clean(pseudocode)
            logging.info('pseudocode:\n%s', pseudocode)


            # TODO 这里的prompt可能需要改一下，在调用util的时候的prompt，需要再加一个动作，将API_description 也进行替换
            API_calling_code = self.get_API_calling_code(APIs)

            # NOTE Step4：将伪代码转化为可执行的代码
            runnable_code = self.pseudocode_compiler(user_requirement, API_calling_code, pseudocode)
            logging.info('Step4:将伪代码转化为可执行的代码\n%s', runnable_code)
            # pattern = r'```Python(.*?)```'
            # match = re.search(pattern, runnable_code, re.DOTALL)
            # if match:
            #     runnable_code = match.group(1).strip()
            runnable_code = CodeUtil.get_code_from_string(runnable_code)

            # NOTE Step5：运行可运行的代码
            # TODO 目前只是将代码保存到一个临时文件中，后面要考虑将每次生成的可运行代码都保存下来
            result = self.code_run(runnable_code)

            if result.stdout:
                # Note 执行成功，直接输出结果
                logging.info('代码执行成功，程序结束:\n%s', result.stdout)
                return result.stdout
            if result.stderr:
                # Note Step6：执行失败，调用错误处理函数
                logging.warning('代码执行报错\n%s', result.stdout)
                error_message = result.stderr
                logging.error('error_message:\n%s', error_message)
                API_doc = CodeUtil.get_API_doc_for_error_judge(APIs)
                error_result = self.error_judge(error_message, plan_pseudocode, runnable_code, API_doc, user_requirement)
                logging.info('进行错误判断，确定错误的level和错误报告\n%s', error_result)
                error_result = json.loads(error_result)
                error_level = error_result['error_level']
                error_report = error_result['error_report']
                # Note Step7：根据判断的error_level 和 error_report，调用对应的错误处理函数
                if error_level == 'design_level':
                    continue
                else:
                    while True:
                        API_documentation = CodeUtil.get_API_doc_foe_code_repair(APIs)
                        runnable_code = self.code_repair(runnable_code, error_message, error_report, API_documentation)
                        runnable_code = CodeUtil.get_code_from_string(runnable_code)
                        logging.info('在coding层面上对代码进行修复\n%s', runnable_code)

                        run_result = self.code_run(runnable_code)
                        if result.stdout:
                            logging.info('代码执行成功，程序结束:\n%s', result.stdout)
                            return run_result.stdout
                        else:
                            logging.warning('代码执行报错\n%s', result.stdout)
                            error_result = self.error_judge(error_message, pseudocode, runnable_code, API_doc, user_requirement)
                            error_result = json.loads(error_result)
                            logging.info('进行错误判断，确定错误的level和错误报告\n%s', error_result)
                            error_level = error_result['error_level']
                            error_report = error_result['error_report']
                            if error_level == 'design_level':
                                break
                            else:
                                continue

# 嗯，勇敢的人先享受世界！！！
if __name__ == '__main__':
    SE = SEFramework()
    # self_framework.self_discovery_framework('My family is planning a movie night, and we need some family-friendly movies to watch. Can you recommend some movies suitable for children that are available on streaming services like Netflix, Prime Video, and Disney+? It would be great if you could provide the streaming links for these movies.')
    user_requirement = '''A group of friends is organizing a themed movie night and needs a selection\
of movies that fit params like "Adventure" or "Animation." They are looking\
for three films and they would like to know the cast details, user reviews, and plot summaries for the chosen movies. '''
    # print(user_requirement)
 #    SE_framework.SE_framework(user_requirement)

    requirement_specification = '''\
 {
    "analyzed_requirements": [
        {
            "requirement": "A selection of movies that fit th into: 1) Identifying movies based on themes, 2) Checking availability of these movies on popular streaming platforms.",
                "stakeholders": "The group of friends organizing the movie night, and potentially the streaming platforms if their APIs are used.",
                "use_cases": "A user inputs a theme, the system returns a list of movies fitting that theme available on selected streaming platforms.",
                "user_stories": "As a movie night organizer, I want to find movies fitting a specific theme available on my streaming platforms, so I can plan the movie night.",
                "objective": "To provide users with a selection of movies fitting their chosen theme available on their streaming platforms.",
                "user_centric_design": "The system should be easy to use, with intuitive theme selection and clear presentation of results.",
                "integration": "The system should integrate with APIs of popular streaming platforms to check movie availability.",
                "priority": "This is a core functionality and should be developed and testeemes like 'Space Exploration' or 'Classic Literature Adaptations.'",
            "analysis": {
                "assumptions": "The system should have access to a comprehensive database of movies, including their themes, availability on streaming platforms, and other details.",
                "breakdown": "This requirement can be broken downd first."
            }
        },
        {
            "requirement": "Provide cast details, user reviews, and plot summaries for the chosen movies.",
            "analysis": {
                "assumptions": "The system should have access to detailed information about movies, including cast, reviews, and plot summaries.",
                "breakdown": "This requirement can be broken down into: 1) Retrieving movie details, 2) Presenting these details to the user.",
                "stakeholders": "The movie night organizers who need this information to make their selection, and potentially movie databases for data retrieval.",
                "use_cases": "A user selects a movie, the system returns detailed information about the movie.",
                "user_stories": "As a movie night organizer, I want to see detailed information about a movie, so I can decide if it fits our movie night.",
                "objective": "To provide users with detailed information about selected movies.",
                "user_centric_design": "The system should present movie details in a clear, easy-to-read format.",
                "integration": "The system should integrate with movie databases to retrieve movie details.",
                "priority": "This is a core functionality and should be developed and tested after the movie selection functionality."
            }
        }
    ]
}'''
    # 调用方法获取最相似的top k个API


    SE.SE_framework(user_requirement)
    # code = SE_framework.task_plan(requirement_specification, user_requirement, 3)
    # print(code)
#     APIs = '''{
#     "API1": ["Advanced Search", "OTT Details"],
#     "API2": ["Title Details", "OTT Details"],
#     "API3": ["Additional Title Details", "OTT Details"]
# }'''

#     APIs = '''{
#     "API1": ["Search By Genre", "Advanced Movie Search"],
#     "API2": ["Get Detailed Response", "Advanced Movie Search"],
#     "API3": ["Title Details", "OTT Details"],
#     "API4": ["Additional Title Details", "OTT Details"]
# }'''
#
#     api_list = json.loads(APIs)
#     API_caller_code = SE_framework.API_call_code_generate(api_list, Config.Rapid_API_key)
#     print(API_caller_code)
#     api_calling_code = open('./temp_output/api_calling_code.py','r').read()
#     pseudocode = open('./temp_output/pseudocode.py','r').read()
#
#     executable_code = SE_framework.pseudocode_compiler(user_requirement,api_calling_code,pseudocode)
#     print(executable_code)



