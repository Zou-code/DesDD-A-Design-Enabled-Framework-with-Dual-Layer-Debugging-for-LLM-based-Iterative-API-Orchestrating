import time
from openai import OpenAI
import os
from config import Config
import tiktoken

class LLM_util:
    def __init__(self):
        # openai_api_key = os.getenv('OPENAI_API_KEY')
        openai_api_key = Config.openai_api_key
        # print(openai_api_key)
        self.client_gpt = OpenAI(api_key=openai_api_key, base_url="https://openkey.cloud/v1")
        # self.client_gpt = OpenAI(api_key=openai_api_key)
        self.client_deepseek = OpenAI(api_key=Config.deepseek_key, base_url="https://api.deepseek.com")

    def call_LLM(self, prompt, llm_name, client):
        message = [
            {"role": "user", "content": prompt}
        ]
        while True:
            try:
                response = client.chat.completions.create(
                    model=llm_name,
                    messages=message,
                    temperature=0
                )
                # return response.choices[0].message['content']
                # print(response)
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                time.sleep(1)

    def model_gpt35(self, prompt):
        model = "gpt-3.5-turbo"
        return self.call_LLM(prompt, model,self.client_gpt)

    def model_gpt4o(self, prompt):
        model = "gpt-4o"
        return self.call_LLM(prompt, model,self.client_gpt)


    def model_deepseek_chat(self, prompt):
        model = "deepseek-chat"
        return self.call_LLM(prompt, model,self.client_deepseek)

    def model_deepseek_coder(self, prompt):
        model = "deepseek-coder"
        return self.call_LLM(prompt, model,self.client_deepseek)

    def model_gpt4(self,prompt):
        model = "gpt-4"
        return self.call_LLM(prompt, model, self.client_gpt)

    def model_gpt4o_mini(self, prompt):
        model = "gpt-4o-mini"
        return self.call_LLM(prompt, model, self.client_gpt)

    def model_embedding(self, text):
        """
        调用OpenAI的embedding接口，将文本转化为embedding向量
        :param text: 需要生成向量的文本
        :return: 一个1536维的list类型的向量
        """
        model = Config.model_embedding
        text = text.replace("\n", " ")
        return self.client_gpt.embeddings.create(input=[text], model=model).data[0].embedding

    @staticmethod
    def num_tokens_from_prompt(prompt):
        """
        计算prompt的token数量并返回
        :param prompt:
        :return:
        """
        prompt = str(prompt)
        encoding = tiktoken.get_encoding(Config.encoding_name)
        num_tokens = len(encoding.encode(prompt))
        return num_tokens

    @staticmethod
    def get_top_k_tokens(prompt, k:int):
        """
        将字符串的Prompt进行编码，返回前k个tokens
        :param prompt: 输入的字符串类型的Prompt
        :param k:
        :return:
        """
        embedding_encoding = Config.encoding_name
        encoding = tiktoken.get_encoding(embedding_encoding)
        tokens = encoding.encode(prompt, disallowed_special=())
        return tokens[:k]

    @staticmethod
    def tokens_to_text(tokens):
        """
        将tokens转换为字符串类型的文本
        :param tokens: 字符串的编码
        :return:
        """
        embedding_encoding = Config.encoding_name
        encoding = tiktoken.get_encoding(embedding_encoding)
        return encoding.decode(tokens)


if __name__ == '__main__':
    util = LLM_util()
    embedding = util.model_embedding("你好啊")
    print(embedding)
    print(type(embedding))
    print(len(embedding))
