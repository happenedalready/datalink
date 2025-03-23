from datalink.util.sql import open_connection, execute_query, close_connection
from datalink.util.qianwen_plus import qianwen
from datalink.util.keywords_extract import keywords_extract


def type_select(text):
    keywords = keywords_extract(text)

    type_candidate = []
    connection = None
    try:
        connection = open_connection()
        for keyword in keywords:
            sql = "select 消息类型 from flight_data where 信息要素 like '%" + keyword + "%'"
            result = execute_query(connection, sql)
            if any(result):
                type_candidate.append(result[0][0])

        type_candidate = list(set(type_candidate))
        print(f"sql查询后可能的消息类型有{type_candidate}")

        system_prompt = "用户将会输入一段文本，请评估以下知识项:"
        for i in range(len(type_candidate)):
            system_prompt += type_candidate[i] + ","
        system_prompt += "与用户输入文本的相关性，并筛选出文本所涉及的最相关的一到四个知识项进行保留，要求只返回最标准的列表形式，采用双引号包括元素。"
        # print(system_prompt)

        result = qianwen(system_prompt, text)
        print(f"大模型评估后保留的消息类型有{result}")

        return [item for item in result.strip('[\"\"]').split('\", \"')]
    except Exception as e:
        print(e)
        return []
    finally:
        if connection:
            close_connection(connection)


if __name__ == '__main__':
    text = "目标捕获更新：更新单元标识为Alpha-5，目标标识为Target-789，更新内容包括增强信号强度和目标方位角调整，更新时间为2023年4月12日14时30分，时间戳为2023年4月12日14时35分。空中评估：评估单元标识为Bravo-6，评估目标为Target-123，评估位置位于北纬40.7128度，东经74.0060度，高度为300米，评估时间为2023年4月12日15时00分，评估结果为敌方设施已确认，时间戳为2023年4月12日15时05分。空中跟踪：跟踪单元标识为Charlie-7，跟踪目标为Target-456，跟踪路径从北纬40.7128度，东经74.0060度至北纬40.7138度，东经74.0070度，跟踪时间范围为2023年4月12日16时00分至17时00分，跟踪状态为开始、进行中和结束，时间戳为2023年4月12日17时05分。空中联合：联合单元标识为Delta-8，联合目标为Target-789，联合位置位于北纬40.7128度，东经74.0060度，高度为500米，联合时间为2023年4月12日18时00分，联合结果为协同攻击准备就绪，时间戳为2023年4月12日18时05分。"
    type_list = type_select(text)
    print(type_list)



