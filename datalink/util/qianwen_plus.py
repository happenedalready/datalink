from dashscope import Generation


def qianwen(system_prompt, user_prompt, api_key="sk-582a75608e534738a82f8078220826ba", model="qwen-plus"):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
        ]
    response = Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=api_key,
        model=model,
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        # print(response.output.choices[0].message.content)
        return response.output.choices[0].message.content
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return response.message