from flask import Flask, request, jsonify, session, g
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# 配置密钥和模型
app.secret_key = "Jxing121"  # 用于 session 加密
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
    # 在每次请求时初始化 OpenAI 客户端
    g.openai_client = init_openai_client()


@app.route('/completions', methods=['POST'])
def completions():
    """
    处理聊天补全请求，并保存多轮对话历史
    """
    data = request.json
    instruction = data.get('message', '')
    prompt = ("请将上面这段文字转为两段结构信息，要求字典格式(不加其他赘余):类型+结构，"
              "其中的空域变更信息的key包括:空域起始坐标、空域结束坐标、生效时间、空域类型、通信频率。"
              "卫星预报信息的key包括:卫星预报、阵地位置、离开时间、目标类型、目标任务、目标型号、所属方、"
              "过顶日期、进入时间、阵地坐标位置、卫星离开时间、空中目标类型、空中目标任务、空中目标型号、航迹所属国家/联盟/地区、卫星过顶日期、卫星进入时间.")
    user_message = instruction.join(prompt)
    print(user_message)

    # 初始化对话历史（如果 session 中不存在历史）
    if 'chat_history' not in session:
        session['chat_history'] = []

    # 添加用户消息到历史记录
    session['chat_history'].append({'role': 'user', 'content': user_message})

    # 获取 OpenAI 客户端
    client = g.openai_client

    # 将对话历史传递给大模型
    completion = client.chat.completions.create(
        model=app.config['OPENAI_MODEL'],
        messages=session['chat_history'],  # 多轮对话历史
    )

    # 提取模型生成的消息
    assistant_message = completion.choices[0].message.content

    # 添加助手消息到历史记录
    session['chat_history'].append({'role': 'assistant', 'content': assistant_message})

    # 返回响应
    return jsonify({
        "assistant_message": assistant_message,
        "chat_history": session['chat_history']  # 返回完整对话历史（可选）
    })


@app.route('/reset', methods=['POST'])
def reset_history():
    """
    重置对话历史
    """
    session.pop('chat_history', None)  # 清空会话
    return jsonify({"message": "Chat history reset."})


if __name__ == '__main__':
    app.run(debug=True)
