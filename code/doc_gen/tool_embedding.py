from util.llm_util import LLM_util
import pandas as pd
from config import Config
from tqdm import tqdm

class Embedding:

    @staticmethod
    def get_embedding():
        """
        将tools.csv文件中的tool_description 字段进行embedding，并保存到一个新的列中
        :return:
        """
        df_tools = pd.read_csv(Config.tool_expan_path)
        df_final_tools = pd.read_csv(Config.tool_path)

        llm_util = LLM_util()
        # df_tools["embedding"] = df_tools.tool_description.apply(lambda x: llm_util.model_embedding(x))
        df_tools["embedding"] = [llm_util.model_embedding(x) for x in tqdm(df_tools.tool_description, desc="Embedding")]
        df_final_tools = pd.concat([df_final_tools,df_tools])

        df_final_tools.to_csv(Config.tool_path, index=False)

if __name__ == '__main__':
    Embedding.get_embedding()