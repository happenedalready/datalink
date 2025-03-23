import json


def extract_key(keyword_list):
    # 读取 JSON 文件
    with open("D:\桌面\Project\Project\datalink\data1.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    extract_list = []

    for keyword in keyword_list:
        if keyword in data:
            threat_alert = data[keyword]
            threat_keys = list(threat_alert.keys())
            extract_list.append(threat_keys)
        else:
            print(f"没有找到{keyword}这个key。")

    formatted_list = []

    # 遍历 extract_list 中的每一组 item
    for items in extract_list:
        descr = ""  # 每次处理一个 items 都初始化一个空的 descr
        for idx, item in enumerate(items):
            if idx == len(items) - 1:  # 如果是最后一个 item
                descr += item  # 不加 "、"
            else:
                descr += f"{item}、"  # 在非最后一个 item 后加 "、"
        descr += "。"  # 每一组项结束后加 "。"

        # 将格式化后的字符串添加到 formatted_list 中
        formatted_list.append(descr)

    return formatted_list


if __name__ == '__main__':
    extract_key(['空域变更', '威胁警报'])