import pandas as pd
from config import Config

def merge_two_df(path1, path2, save_path):
    """
    将两个dataframe合并为一个dataframe
    :param path1: 第一个csv文件的地址
    :param path2: 第二个csv文件的地址
    :param save_path: 合并之后的文件，保存的地址
    :return:
    """
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    df = pd.concat([df1, df2], ignore_index=True)

    df.to_csv(save_path, index=False)

if __name__ == '__main__':
    # path1 = Config.api_original_base_path
    # path2 = Config.api_original_path
    # dest_path = "../data/original_data/apis.csv"
    #
    # merge_two_df(path1, path2, path1)
    path1 = '../data/requirement/requirements.csv'
    path2 = '../data/requirement/requirements_4.csv'
    dest_path = '../data/requirement/requirements.csv'
    merge_two_df(path1, path2, dest_path)