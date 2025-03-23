import time
import os
from openai import OpenAI

from datalink.util.extract import extract_key

# 配置API密钥和模型
OPENAI_API_KEY = "sk-c31303420bd24975b0287cfce6af2271"
OPENAI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
OPENAI_MODEL = "qwen-plus"


def getJson(text, keys):

    # 假定的提取关键字列表
    out_list = extract_key(keys)
    num = len(out_list)
    prompt = f"请将上面这段文字转为{num}段结构信息，要求标准的json格式(不加其他赘余,不加其他任何描述):类型+结构，"
    for i in range(num):
        prompt += f"其中的{keys[i]}的key包括:{out_list[i]}"

    user_message = f"{text} {prompt}"

    print(user_message)

    messages = []
    messages.append({'role': 'user', 'content': user_message})

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-c31303420bd24975b0287cfce6af2271",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
    )

    content = completion.choices[0].message.content
    content = content.replace("```json", "").replace("```", "")

    print(content)

    return content


if __name__ == "__main__":
    text = ("在接下来的演练中，我们将在北纬34度27分、东经118度25分至北纬34度30分、东经118度30分之间的空域设立一个新的禁飞区，"
            "并将其定为限制区和活动区。该空域变更将于明天上午9时生效。所有参与方需使用121.5MHz的指挥频率进行通讯，并在紧急情况下切换到243MHz的应急频率。"
            "同时，我们将启用编号为LCP-007的弹道走廊，该走廊宽度为5海里，将从北纬34度28分、东经118度26分的起点位置延伸至北纬34度29分、东经118度27分的终点位置。"
            "此弹道走廊的上升段将从明天上午9时开始，于下午5时结束。在执行过程中，请注意中间经过点位置北纬34度28分30秒、东经118度26分30秒的安全通过。")
    keys = ['空域变更', '弹道参数']

    content = getJson(text, keys)
