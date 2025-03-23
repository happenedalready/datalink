import chromadb
from text2vec import SentenceModel
from chromadb import Documents, EmbeddingFunction, Embeddings
import json
import time  # 导入 time 模块

from util.extract import extract_key


def extract_values(obj):
    values = []
    if isinstance(obj, dict):
        for value in obj.values():
            if isinstance(value, (dict, list)):
                values.extend(extract_values(value))
            else:
                values.append(value)
    elif isinstance(obj, list):
        for item in obj:
            values.extend(extract_values(item))
    return values


def instruction_combination(instruction):
    sentences = instruction.split('，')

    result = []
    ids = []

    for sentence in sentences:
        result.append(sentence)
        ids.append(f"id{len(result)}")  # 为每个句子生成唯一的标识符

    for i in range(len(sentences) - 1):
        combined_sentence = sentences[i] + '，' + sentences[i + 1]
        result.append(combined_sentence)
        ids.append(f"id{len(result)}")  # 为每个句子生成唯一的标识符
    return result, ids


class Text2VecEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceModel('shibing624/text2vec-base-chinese')

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = [self.model.encode(text).tolist() for text in texts]
        return embeddings


def research(instruction):
    with open('../data1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    keys = []

    chroma_client = chromadb.Client()

    collection = chroma_client.create_collection(
        name="my_collection",
        embedding_function=Text2VecEmbeddingFunction()
    )

    myDocuments, myIds = instruction_combination(instruction)

    collection.add(
        documents=myDocuments,
        ids=myIds
    )

    for key, value in data.items():
        values = extract_values(value)
        count = len(values)
        score = 0
        for sentence in values:
            results = collection.query(
                query_texts=[sentence],
                n_results=1
            )
            score += results["distances"][0][0]
        if 275 > (score / count):
            keys.append(key)

    return keys


if __name__ == "__main__":
    start_time = time.time()  # 记录开始时间
    ins = ("前方发现潜在威胁目标，正快速向我方空域靠近，现已启动二级威胁警报，各机进入战斗准备状态，随时准备应对可能的空中冲突。空域将进行变更：空域起始坐标为东经115°20′，北纬30°10′；空域结束坐标为东经116"
           "°30′，北纬31°45′；该变更空域自北京时间14时00分起正式生效；空域类型为临时作战管制区；通信频率调整为127.500 MHz。")
    # ins = ("2025年1月20日08:00 UTC起，位于北纬30.000度、东经120.000度至北纬35.000度、东经125.000度的空域将进行变更, 划定为禁飞区与限制区。"
    #        "指挥频率为132.000 MHz，应急频率为121.500 MHz。与此同时，2025年1月21日03:00 UTC, 侦察卫星GX-12将从北纬40.000度、东经116.000度上空进入，"
    #        "并于06:00 UTC离开。该卫星执行空中侦察任务, 主要用于情报收集，隶属于北约国防联盟，过顶日期为2025年1月21日。")
    # keys = research(ins)
    # end_time = time.time()  # 记录结束时间
    # print(keys)
    # print(f"运行时间：{end_time - start_time:.2f} 秒")  # 输出运行时间
    ins1 = ("我方预警机编队正受到不明国籍战斗机编队的威胁，目标数量2架，型号未知，当前位于东经116°30′、北纬32°15′，高度8000米，速度1200公里/小时，航向270°（正西），"
            "威胁等级一级（极高），各单位立即进入一级战备状态，拦截编队做好拦截准备，预警机编队调整航向至090°，高度降至7000米，避开威胁方向，"
            "保持通信畅通并随时报告威胁动态，观测区域位于东经116°00′、北纬32°00′，当前气象状况为局部小雨，能见度10公里，西南风，风速15米/秒，"
            "云量8成，云底高2000米，云顶高6000米，场压1010百帕，请各单位根据气象条件调整飞行姿态，避免进入云层，确保飞行安全，拦截编队注意利用气象条件隐蔽接近，预警机编队加强空中监视。")

    ins2 = ("敌方所属的侦察卫星（目标型号：XX型）将于今日15时进入我方阵地（坐标位置：东经116°30′，北纬32°15′）上空，过顶日期为2025年1月23日，"
            "预计进入时间为14时45分，离开时间为15时15分，目标类型为侦察卫星，任务为对我方阵地进行情报收集，各单位做好隐蔽措施，严格控制电磁信号，避免暴露阵地信息。")

    keys = research(ins2)
    out_list = extract_key(keys)

    num = len(out_list)
    prompt = f"请将上面这段文字转为{num}段结构信息，要求字典格式(不加其他赘余):类型+结构，"
    for i in range(num):
        prompt += f"其中的{keys[i]}的key包括:{out_list[i]}"

    user_message = f"{ins} {prompt}"
    print(user_message)