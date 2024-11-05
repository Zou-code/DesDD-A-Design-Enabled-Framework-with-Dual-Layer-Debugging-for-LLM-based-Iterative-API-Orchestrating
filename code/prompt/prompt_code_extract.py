def prompt_code_extract(original_string):
    """
    从一个给定的字符串中提取出代码的部分
    :param prompt:
    :return:
    """
    prompt = f'''\
Please extract the Python code portion from a string that contains Python code, and save the extracted code in JSON format as follows:

{{
    "Python_code": "Extracted Python code"
}}

For example, if the input string is:

"This is a string containing Python code:\n\n```python\ndef hello_world():\n    print('Hello, World!')\n```\n\nOther text content"

Then the output should be:

{{
    "Python_code": "def hello_world():\n    print('Hello, World!')"
}}

Ensure that the extracted code is complete.

Input string:
{original_string}
'''
    return prompt
