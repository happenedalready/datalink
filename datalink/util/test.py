import re
import pprint

# 示例生成内容，替换为 print(content) 查看实际生成的文本
content = """
### 空域变更信息

**类型：空域变更**

- **空域起始坐标**：北纬30.000度、东经120.000度
- **空域结束坐标**：北纬35.000度、东经125.000度
- **生效时间**：2025年1月20日08:00 UTC
- **空域类型**：禁飞区与限制区
- **通信频率**：
  - 指挥频率：132.000 MHz
  - 应急频率：121.500 MHz

### 卫星预报信息

**类型：卫星预报**

- **阵地位置**：北纬40.000度、东经116.000度
- **进入时间**：2025年1月21日03:00 UTC
- **离开时间**：2025年1月21日06:00 UTC
- **目标类型**：空中目标
- **目标任务**：情报收集
- **目标型号**：GX-12
- **所属方**：北约国防联盟
- **过顶日期**：2025年1月21日
- **卫星进入时间**：2025年1月21日03:00 UTC
- **卫星离开时间**：2025年1月21日06:00 UTC
- **空中目标类型**：侦察卫星
- **空中目标任务**：空中侦察
- **空中目标型号**：GX-12
- **航迹所属国家/联盟/地区**：北约国防联盟
- **卫星过顶日期**：2025年1月21日
"""

# 分段匹配
section_pattern = r"### (.*?)\n\n\*\*类型：(.*?)\*\*\n([\s\S]*?)(?=\n###|\Z)"
item_pattern = r"- \*\*(.*?)\*\*：(.*?)(?=\n- \*\*|\n|$)"
sublist_pattern = r"- (.*?)：([\s\S]*?)(?=\n  - |\n- |\Z)"

# 匹配分段
sections = re.findall(section_pattern, content)

# 存储结果的字典
result = {}

for section_title, section_type, section_body in sections:
    structure = {}
    # 匹配字段
    for match in re.finditer(item_pattern, section_body):
        key, value = match.groups()
        key = key.strip()
        value = value.strip()

        # 检测是否是"通信频率"字段，并处理其子项
        if key == "通信频率":
            sublist = {}
            # 匹配子项
            for submatch in re.finditer(r"- (.*?):(.*)", value):
                subkey, subvalue = submatch.groups()
                sublist[subkey.strip()] = subvalue.strip()
            structure[key] = sublist
        else:
            structure[key] = value

    result[section_title] = structure

# 输出结果
pprint.pprint(result)
