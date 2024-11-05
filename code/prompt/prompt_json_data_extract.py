
def prompt_json_data_extract(json_data):
    '''
    从json数据中提取出需要的数据
    :param json_data: 包含其他字符的json数据
    :return: 不包含其他字符的json数据
    '''

    prompt = f'''\
Please Extract the json data from the following text:
{json_data}
Please note that the generate json string should be a valid json string, and the json string should not contain any other characters except for json data.
And you should not output anything other natural language text.'''
    return prompt