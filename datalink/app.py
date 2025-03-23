import time
import os
import json
from flask import Flask, request, jsonify, session, g
from flask_cors import CORS
from flask_socketio import SocketIO
from openai import OpenAI
# from util.new_research import research
from util.type_select import type_select
from util.extract import extract_key

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # 启用 WebSocket

# 配置密钥和模型
app.secret_key = "Jxing121"
app.config['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY", "sk-c31303420bd24975b0287cfce6af2271")
app.config['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
app.config['OPENAI_MODEL'] = "qwen-plus"


# 初始化 OpenAI 客户端
def init_openai_client():
    return OpenAI(
        api_key=app.config['OPENAI_API_KEY'],
        base_url=app.config['OPENAI_BASE_URL']
    )


@app.before_request
def before_request():
    g.openai_client = init_openai_client()


@app.route('/completions', methods=['POST'])
def completions():
    """
    处理聊天补全请求，并保存多轮对话历史
    """

    # -------------------  初始化 + 读取 + 匹配  -----------------
    data = request.json
    instruction = data['messages']

    # 每次请求清空 session['chat_history']
    session['chat_history'] = []

    socketio.emit('loadingMessage', {'message': '请稍候，正在匹配元语言...'})  # 匹配元语言(还没搞好)
    time.sleep(2)

    keys = type_select(instruction)
    # keys = ['卫星预报']
    # keys.append('空域变更')

    # ---------- 优化prompt进行测试 -------------------
    socketio.emit('loadingMessage', {'message': '正在调用大模型处理数据...'})  # 传输给大模型
    time.sleep(2)

    out_list = extract_key(keys)
    print(out_list)
    num = len(out_list)
    prompt = f"请将上面这段文字转为{num}段结构信息，要求标准的json格式(不加其他赘余,不加其他任何描述):类型+结构，"
    for i in range(num):
        prompt += f"其中的{keys[i]}的key包括:{out_list[i]}"

    user_message = f"{instruction} {prompt}"

    # 重新初始化对话历史
    session['chat_history'].append({'role': 'user', 'content': user_message})

    client = g.openai_client
    completion = client.chat.completions.create(
        model=app.config['OPENAI_MODEL'],
        messages=session['chat_history'],
    )

    content = completion.choices[0].message.content
    content = content.replace("```json", "").replace("```", "")  # 获取最终输出

    session['chat_history'].append({'role': 'assistant', 'content': content})

    # -----------  自我反思 -----------------------------
    socketio.emit('loadingMessage', {'message': '自我反思中...'})

    reflection_prompt = f"""
        你需要检查以下 JSON 数据是否符合要求：

        【提取出的 JSON 数据】：
        {content}

        【要求】：
        1. JSON 必须严格按照标准格式，不能有额外的文本。
        2. 其中的类型必须是：{keys}
        3. 每个类型的 key 必须包含：{out_list}
        4. 确保 JSON 的层级结构与预期一致，不能缺少字段或错误嵌套

        如果 JSON 完全符合要求，返回 `true`；
        如果有问题，返回 `false` 并给出错误原因。

        返回格式(仅包含下面的信息)：
        ```json
        {{
          "is_valid": true 或 false,
          "reason": "错误原因（如果有）"
        }}
        ```
        
        """

    session['chat_history'].append({'role': 'user', 'content': reflection_prompt})

    reflection_completion = client.chat.completions.create(
        model=app.config['OPENAI_MODEL'],
        messages=session['chat_history'],
    )

    reflection_result = reflection_completion.choices[0].message.content
    reflection_result = reflection_result.replace("```json", "").replace("```", "")
    print(reflection_result)

    try:
        reflection_data = json.loads(reflection_result)
        is_valid = reflection_data.get("is_valid", False)
        reason = reflection_data.get("reason", "未知错误")
    except json.JSONDecodeError:
        is_valid = False
        reason = "大模型返回的格式错误，无法解析"

    # -------------------------------------------------------

    if is_valid:
        print('自我反思完成，数据符合预期！')
    else:
        print(f'自我反思发现问题：{reason}')
        # 自动修正 JSON
        fix_prompt = f"""
            你的 JSON 存在以下问题：
            {reason}

            请基于原 JSON 数据修正错误，确保符合要求。仅返回修正后的 JSON，不要任何额外文本。
            """

        session['chat_history'].append({'role': 'user', 'content': fix_prompt})

        fix_completion = client.chat.completions.create(
            model=app.config['OPENAI_MODEL'],
            messages=session['chat_history'],
        )

        fixed_content = fix_completion.choices[0].message.content
        fixed_content = fixed_content.replace("```json", "").replace("```", "")

        session['chat_history'].append({'role': 'assistant', 'content': fixed_content})

        # socketio.emit('loadingMessage', {'message': '错误已修正！'})
        content = fixed_content  # 替换原始 JSON

    # ------------  output ----------------------------
    socketio.emit('loadingMessage', {'message': '数据处理完成！'})
    time.sleep(2)

    return content


@app.route('/finderror', methods=['POST'])
def findError():
    """
    处理错误信息
    """
    data = request.json
    key = data['messages']

    socketio.emit('loadingMessage', {'message': '正在分析研究关键词...'})


    # print(content)
    # session.pop('chat_history', None)

    socketio.emit('loadingMessage', {'message': '正在提取关键词...'})

    print(key)
    # 这里书写修正的逻辑
    err_prompt = f"""
            之前抽取的信息当中出现了错误信息，请根据错误的消息类型类型对文本重新进行抽取，如果认为错误信息已经解决，请返回原有抽取的结构化信息。
            错误类型：{key}

            仅返回修正后的 JSON，不要任何额外文本。
            """
    session['chat_history'].append({'role': 'user', 'content': err_prompt})
    # time.sleep(2)

    socketio.emit('loadingMessage', {'message': '正在调用大模型处理数据...'})

    client = g.openai_client
    err_completion = client.chat.completions.create(
        model=app.config['OPENAI_MODEL'],
        messages=session['chat_history'],
    )

    err_content = err_completion.choices[0].message.content
    err_content = err_content.replace("```json", "").replace("```", "")

    socketio.emit('loadingMessage', {'message': '数据处理完成！'})

    return err_content


@app.route('/reset', methods=['POST'])
def reset_history():
    """
    重置对话历史
    """
    session.pop('chat_history', None)
    return jsonify({"message": "Chat history reset."})


# @app.after_request
# def clear_session(response):
#     """
#     确保每次请求后清空 session，防止数据残留影响下次请求
#     """
#     session.pop('chat_history', None)
#     return response


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
