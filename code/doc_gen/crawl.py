# -*- coding: utf-8 -*-
import json
import re
import time
import sys
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def setup_driver():
    print(2)
    # 设置无头模式
    options = Options()
    options.headless = True  # 无头模式
    driver = webdriver.Chrome(options=options)
    return driver


def wait_for_element(driver, class_name):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )

sys.stdout.reconfigure(encoding='utf-8')

def api_name(driver) -> str:
    code_elements = driver.find_elements(By.CSS_SELECTOR,
                                         ".truncate.text-xs.font-normal.normal-case.text-breadcrumb-text")
    api_names = []
    for element in code_elements:
        api_names.append(element.text)
        # print("API Name:", element.text)
    return ", ".join(api_names)


def tool_name(driver):
    p_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//p[@class="truncate"]'))
    )

    tool_names = []
    for element in p_elements:
        tool_names.append(element.text)
        # print("Tool name:", element.text)
    return ", ".join(tool_names)

def api_desc(page: str, api_id: str): # 获取api_description
    scripts = re.findall(r'<script>[^>]*</script>', page)
    for s in scripts:
        if 'self.__next_f.push([1,"f:' in s:
            # print(s)
            s = s.replace('<script>self.__next_f.push([1,"f:', '"').replace('\\n"])</script>', '"')
            json_data = json.loads(json.loads(s))
            endpoints: list = json_data[3]["state"]["queries"][1]["state"]["data"]["endpoints"]
            # print(endpoints)
            # with open('data.json', 'w', encoding='utf-8') as f:
            #     json.dump(json_data, f, ensure_ascii=False, indent=4)
            for endpoint in endpoints:
                if endpoint["id"] == api_id:
                    # print(endpoint["description"])
                    return endpoint["description"]


def parameters(page) -> dict:
    infos = {}

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(page, 'html.parser')

    # 查找所有的参数 div 标签
    param_divs = soup.find_all('div', class_='css-1qdo00m')

    # 遍历每个参数 div 标签，提取信息
    for param_div in param_divs:
        info = {
            'name': '',
            'option': '',
            'type': '',
            'desc': '...',  # 默认值
        }
        # 提取名称
        name_tag = param_div.find('span', class_='text-ellipsis css-1j2ol27')
        name = name_tag.get_text(strip=True) if name_tag else None
        info["name"] = name

        # 提取可选性
        optional_tag = param_div.find('span', class_='items-baseline italic text-xs text-gray-400')
        optional = optional_tag.get_text(strip=True) if optional_tag else "(required)"
        info["option"] = optional

        # 提取类型
        type_tag = param_div.find('span', class_='text-[10px] text-gray-900')
        param_type = type_tag.get_text(strip=True) if type_tag else None
        info["type"] = param_type

        # 提取描述
        description_tag = param_div.find('div', class_='markdown w-full break-normal text-xs leading-normal')
        description = description_tag.get_text(strip=True) if description_tag else None
        if description:
            info["desc"] = description

        infos[info["name"]] = info["type"] + ' - ' + info['desc'] + info['option']
    return infos

def parameter_info(page) -> list:
    infos = []

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(page, 'html.parser')

    # 查找所有的参数 div 标签
    param_divs = soup.find_all('div', class_='css-1qdo00m')

    # if not param_divs:
    #     time.sleep(15) # 等待加载？

    # 遍历每个参数 div 标签，提取信息
    for param_div in param_divs:
        info = {
            'name': '',
            'option': '',
            'type': '',
            'desc': '...', # 默认值
        }
        # 提取名称
        name_tag = param_div.find('span', class_='text-ellipsis css-1j2ol27')
        name = name_tag.get_text(strip=True) if name_tag else None
        info["name"] = name

        # 提取可选性
        optional_tag = param_div.find('span', class_='items-baseline italic text-xs text-gray-400')
        optional = optional_tag.get_text(strip=True) if optional_tag else "(required)"
        info["option"] = optional

        # 提取类型
        type_tag = param_div.find('span', class_='text-[10px] text-gray-900')
        param_type = type_tag.get_text(strip=True) if type_tag else None
        info["type"] = param_type

        # 提取描述
        description_tag = param_div.find('div', class_='markdown w-full break-normal text-xs leading-normal')
        description = description_tag.get_text(strip=True) if description_tag else None
        if description:
            info["desc"] = description

        infos.append(info)
    return infos

def one_api(url: str, driver): # 获取一个页面的api info：tool_name, api_name, api_description, parameters
    # 找到该api的id
    idx = url.find('apiendpoint')
    api_id = url[idx::]

    driver.get(url)
    # 在访问页面后等待页面完全加载
    WebDriverWait(driver, 60).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    page = ''
    try: # 没有参数的page加载的不一样
        # 等待加载出参数相关页面
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-1qdo00m'))
        )
        page = driver.page_source
        # param = parameter_info(page)
        param = parameters(page)
    except Exception: # 没有params
        page = driver.page_source
        param = "No additional params"
    finally:
        desc = api_desc(page, api_id)

        tool = tool_name(driver)

        name = api_name(driver)
    # page = driver.page_source
    # print(page)

    # if 'No additional params' in page: # 可能没有参数
    #     param = "No additional params"
    # else:
    #     param = parameter_info(page)

    return tool, name, desc, param


def main(df):
    # driver = webdriver.Chrome()  # 确保ChromeDriver已安装并在路径中
    driver = setup_driver()
    print(1)
    # api_data = []
    # for url in tqdm(url_list, total=len(url_list)):
    for _,row in tqdm(df.iterrows(),total = len(df)):
        df_apis = pd.read_csv('./apis_data.csv')
        url = row['url']
        tool, name, desc, params = one_api(url, driver)
        print("Tool Name:", tool)
        print("API Name:", name)
        print("API Description:", desc)

        # 打印API参数信息
        print("API Parameters:", end=' ')
        if isinstance(params, str): # 没有参数
            print(params)
        elif isinstance(params, dict):
            # print(params)
            for p_name, p_info in params.items():
                # 输出结果
                # print("名称:", p["name"])
                # print("可选性:", p["option"])
                # print("类型:", p["type"])
                # print("描述:", p["desc"])
                print(p_name, ":", p_info)
                # print("-" * 40)
            params = json.dumps(params)
        print('=' * 50)

        new_data = {
            "tool_name": row['tool_name'],
            "api_name": name,
            "api_description": desc,
            "query_string": url,
            "required_parameters": params
        }

        # api_data.append({
        #     "tool_name": tool,
        #     "api_name": name,
        #     "api_description": desc,
        #     "parameters": params,
        # })
        # api_df = pd.DataFrame(api_data)
        df_apis.loc[len(df_apis)] = new_data
        df_apis.to_csv('./apis_data.csv', index=False)
    driver.quit()
if __name__ == '__main__':
    df_crawl_tools = pd.read_csv('./crawl_tools.csv')

    main(df_crawl_tools)
