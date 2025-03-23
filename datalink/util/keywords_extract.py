from datalink.util.qianwen_plus import qianwen


def keywords_extract(text):
    system_prompt1 = "你是一个擅长提取结构化信息的助手"
    user_prompt1 = ("这里有一条军事航空领域的自然语言指令，这条指令当中可能会描述几种消息，每条消息会包含不同的消息要素，请从指令中提取与结构化知识项相关的关键要素，例如：“在东经120度、北纬35度、海拔8000"
                    "米处进行空中整合任务，整合单元标识为“INTEGRATOR-001”，整合目标标识为“TARGET-098”。此次整合任务应在14:00完成，并预计于14:10"
                    "报告整合结果。”提取出来的关键要素是[整合单元标识,整合目标,整合位置,整合时间,整合结果]。不提取对应的值，要求只返回标准的列表格式。需要提取的指令如下：“")
    user_prompt1 += text
    user_prompt1 += "”最终要求按照标准的列表格式输出一个列表。"
    keywords_string = qianwen(system_prompt1, user_prompt1)
    system_prompt2 = "你是一个擅长生成文本近义词的助手"
    user_prompt2 = "这里有一个列表，请给这个列表中每个元素生成至多十个的近义词，并将所有元素和生成的近义词都放进一个列表中，要求只返回标准的列表格式并且只返回一个列表，不要包含换行符，采用单引号包括元素。列表如下："
    keywords_string = qianwen(system_prompt2, user_prompt2 + keywords_string)
    keywords = [item for item in keywords_string.strip('[\'\']').replace(' ', '').split('\',\'')]
    return keywords


if __name__ == '__main__':
    text = ("在北纬35度20分，东经45度15分，高度为2000米的位置，修理单元标识为R-123的维修部队将对编号为T-456的目标进行空中修理任务。该任务预计于今天上午10时开始，并将于中午12"
            "时完成，修理结果良好。与此同时，联合单元标识为U-789的联合部队将在同一地点的高度2000米处与编号为J-678的目标进行空中联合行动，此行动也定于上午10时开始，预期将在中午12"
            "时结束，联合结果表明一切顺利。以上两份报告的时间戳均为2023年4月5日13时整。")
    keywords = keywords_extract(text)
    print(keywords)
