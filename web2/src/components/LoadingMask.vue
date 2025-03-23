<template> 
  <div v-if="visible" class="loading-mask">
    <div class="loading-content">
      <div class="spinner"></div>
      <br>
      <!-- <p>{{ message }}</p> -->
       <div style="padding-right: 5%;">
      <a-steps :current="changeCount-1">
        <a-step
          v-for="(item, index) in items"
          :key="index"
          :title="item.title"
        />
      </a-steps>
      </div>
<!-- 修改这里，添加一个包裹容器 -->
<div class="text-container">
  <div class="text-block">
  <template v-for="(char, index) in textArray1" :key="index">
    <span 
      v-if="char !== '\n'"
      class="char" 
      :style="{ opacity: index < currentIndex1 ? '1' : '0' }"
    >{{ char }}</span>
    <br v-else-if="index < currentIndex1" />
  </template>
</div>

<div class="text-block">
  <template v-for="(char, index) in textArray2" :key="index">
    <span 
      v-if="char !== '\n'"
      class="char" 
      :style="{ opacity: index < currentIndex2 ? '1' : '0' }"
    >{{ char }}</span>
    <br v-else-if="index < currentIndex2" />
  </template>
</div>

<div class="text-block">
  <template v-for="(char, index) in textArray3" :key="index">
    <span 
      v-if="char !== '\n'"
      class="char" 
      :style="{ opacity: index < currentIndex3 ? '1' : '0' }"
    >{{ char }}</span>
    <br v-else-if="index < currentIndex3" />
  </template>
</div>

<div class="text-block">
  <template v-for="(char, index) in textArray4" :key="index">
    <span 
      v-if="char !== '\n'"
      class="char" 
      :style="{ opacity: index < currentIndex4 ? '1' : '0' }"
    >{{ char }}</span>
    <br v-else-if="index < currentIndex4" />
  </template>
</div>
      </div>

    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, defineProps, watch,computed } from 'vue'; // 添加watch导入
import {Steps } from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

// 确保Steps组件被正确使用，Ant Design Vue通常自动处理组件名为a-steps
const ASteps = Steps;
const props = defineProps({
  visible: Boolean,
  message: {
    type: String,
    default: '请稍候，正在处理数据...',
  },
});

const description = computed(() => props.message);
const flag1 = ref(0);
const flag2 = ref(0);
const flag3 = ref(0);
const flag4 = ref(0);


const items = computed(() => [
{ title: '匹配元语言数据库', description: "请稍候，正在预处理..." },
  { title: '大模型结构化解析', description: "正在匹配元语言..." },
  { title: '自我反思中', description: "正在调用大模型处理数据..." },
  { title: '数据处理完成', description: "自我反思中..." },
]);

const changeCount = ref(0);

watch(
  () => [props.message, props.visible],
  ([newMessage, newVisible], [oldMessage, oldVisible]) => {
    if (newMessage !== oldMessage) {
      changeCount.value += 1;
      console.log(description.value)
      if(changeCount.value === 1){
        flag1.value = 1;
        showText1(); // 调用动画函数
      }
      if(changeCount.value === 2){
        flag2.value = 1;
        currentIndex1.value = textArray1.length;
        flag1.value = 0;
        showText2();
      }
      if(changeCount.value === 3){
        flag3.value = 1;
        currentIndex2.value = textArray2.length;
        flag2.value = 0;
        showText3();
      }
      if(changeCount.value === 4){
        flag4.value = 1;
        currentIndex3.value = textArray3.length;
        flag3.value = 0;
        showText4();
      }
    }
    if (!newVisible) {
      changeCount.value = 0;
      flag1.value = 0;
      flag2.value = 0;
      flag3.value = 0;
      flag4.value = 0;
      currentIndex1.value = 0;
      currentIndex2.value = 0;
      currentIndex3.value = 0;
      currentIndex4.value = 0;

    }
  }
);

//每个步骤的内容
const content1 = ref(`· 接收自然语言指令输入
· 进行基础文本清洗（去除噪声、标准化表述）
· 提取关键语义要素（实体识别/关键词抽取）`);
const textArray1 = content1.value.split("");
const currentIndex1 = ref(0);

const showText1 = () => {
  if (currentIndex1.value < textArray1.length && flag1.value) {
    setTimeout(() => {
      currentIndex1.value++;
      showText1();
    }, 50); // 逐字间隔 200ms
  }
};

const content2 = ref(`· 加载元语言知识库索引
· 基于语义相似度进行向量检索（建议用颜色突出该关键步骤）
· 生成Top-K候选指令模板集（K值可动态调整）`);
const textArray2 = content2.value.split("");
const currentIndex2 = ref(0);

const showText2 = () => {
  if (currentIndex2.value < textArray2.length && flag2.value) {
    setTimeout(() => {
      currentIndex2.value++;
      showText2();
    }, 50); // 逐字间隔 200ms
  }
};

const content3 = ref(`· 指令类型匹配（从候选集中识别最适模板）
· 要素提取（填充模板参数槽位）
· 歧义消解（处理多义性表述）`);
const textArray3 = content3.value.split("");
const currentIndex3 = ref(0);

const showText3 = () => {
  if (currentIndex3.value < textArray3.length && flag3.value) {
    setTimeout(() => {
      currentIndex3.value++;
      showText3();
    }, 100); // 逐字间隔 200ms
  }
};

const content4 = ref("");
const textArray4 = content4.value.split("");
const currentIndex4 = ref(0);

const showText4 = () => {
  if (currentIndex4.value < textArray4.length && flag4.value) {
    setTimeout(() => {
      currentIndex4.value++;
      showText4();
    }, 50); // 逐字间隔 200ms
  }
};

</script>

<style scoped>
/* 蒙版样式 */
.loading-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

/* 加载内容 */
.loading-content {
    background: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    width: 70%;
    height: 50%;
}

/* 旋转动画 */
.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid rgba(0, 0, 0, 0.2);
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.text-container {
  display: flex;
  flex-direction: row;  /* 横向排列 */
  justify-content: space-around;  /* 平均分配空间 */
  gap: 20px;  /* 设置间距 */
  margin-top: 20px;
}

.text-block {
  /* 每个文本块的样式 */
  padding: 10px;
  /* 可选：添加背景色或边框使分隔更明显 */
  /* background-color: #f5f5f5; */
  /* border: 1px solid #eee; */
  /* border-radius: 4px; */
  width: 20%;
  text-align: left; /* 让文本整体右对齐 */
  color: rgb(113, 113, 113);

}

.char {
  display: inline-block;
  transition: opacity 0.05s ease;
}
</style>