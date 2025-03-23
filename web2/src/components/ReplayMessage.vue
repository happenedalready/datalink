<script setup lang="ts">
import { message, message as messageTip } from 'ant-design-vue';
import useMessages from '@/composables/messages';
import { CopyOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import { useClipboard } from '@vueuse/core';
import { TMessage } from '@/types';
import { BulbOutlined,CloseOutlined,CloseSquareOutlined,} from '@ant-design/icons-vue';

// 消息管理和剪贴板功能
const messages = useMessages();
const { copy } = useClipboard({});

// 定义传入的 Props
const props = defineProps<{
  propMessage: TMessage;
}>();


  const text = props.propMessage.msg
  console.log("传入"+text)
  const mms = JSON.parse(text);
  console.log("转json"+mms)

// 方法：复制消息
const copyIt = (msg: string) => {
  copy(msg);
  messageTip.success('已复制');
};

// 方法：删除消息
const deleteIt = (message: TMessage) => {
  messages.messages.value = messages.messages.value.filter((item) => item !== message);
  messageTip.success('已删除');
};

let errorlist: string[] = [];

const clickcheckbox = (msg: string) => {
  if (errorlist.includes(msg)) {
    // 存在则过滤掉该消息
    errorlist = errorlist.filter(item => item !== msg);
  } else {
    // 不存在则添加
    errorlist.push(msg);
  }
  console.log(msg);
};

const submit=()=>{

  if (errorlist.length==0){
    messageTip.success("全部无误，验证通过")
  }

  else{
    console.log(errorlist)
    isClickRefresh(errorlist);
  }
}

const emits = defineEmits(['isClickRefresh'])
const isClickRefresh = (param:any) => {
		emits('isClickRefresh', param) // 根据需求参数，可带可不带
    console.log("点按钮了")
    messageTip.success("已发送错误信息")
	}
</script>

<template>
  <div class="my-2 self-start flex items-center">
    <div class="class1">
      <BulbOutlined class="class2" />
    </div>
    <div class="board">
      <div>
        <div class="overflow-x-auto rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 w-full">
      <table class="w-full divide-y divide-gray-200">
        <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
          <tr>
            <th class="px-6 py-3 text-center text-base" style="width: 15%">消息类型</th>
            <th class="px-6 py-3 text-left text-base" style="width: 75%">结构</th> <!-- 增加结构列宽度 -->
            <th class="px-6 py-3 text-center text-base" style="width: 10%">验证</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(message, index) in mms" :key="index" class="hover:bg-gray-50 transition-colors">
            <!-- 消息类型列 -->
            <td class="px-6 py-4 whitespace-nowrap text-center align-middle">
              <span class="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {{ message.类型 }}
              </span>
            </td>
        
            <!-- //嵌套表格 -->
            <td class="px-6 py-4 align-top">
  <div class="overflow-x-auto rounded-lg border border-gray-100 shadow-xs">
    <table class="min-w-max"> <!-- 改为基于内容的最小宽度 -->
      <thead class="bg-gray-50">
        <tr>
          <th 
            v-for="(value, key) in message.结构" 
            :key="key"
            class="px-3 py-2 text-left text-sm font-medium text-gray-500 uppercase tracking-wider min-w-[50px]"
          >
            {{ key }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 bg-white">
        <tr>
          <td 
            v-for="(value, i) in message.结构"
            :key="i"
            class="px-3 py-2 text-sm text-gray-600"
          >
            <span class="font-mono break-all">{{ value }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</td>
<!-- 验证状态 -->
        <td class="px-6 py-4 align-middle">
          <div class="flex items-center justify-center">
            <label class="error-switch">
              <input 
                type="checkbox" 
                hidden 
                :checked="message.isError"
                @change="clickcheckbox(message.类型)"
              >
              <span class="slider"></span>
            </label>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</div>
<div class="button-container">
  <a-button type="primary" @click="submit">提交</a-button>
</div>

</div>
    <CopyOutlined
      class="pl-2 cursor-pointer self-end !text-gray-400"
      @click="copyIt(propMessage.msg)"
    />
    <DeleteOutlined
      class="pl-1 cursor-pointer self-end !text-gray-400"
      @click="deleteIt(propMessage)"
    />
  </div>
</template>

<style scoped>

/* 新增全局表格样式重置 */
.message-table :deep(table) {
  border-collapse: collapse;
  border-spacing: 0;
}

.button-container {
  margin-top:  10px;
  text-align: right; /* 让按钮向右对齐 */
}
.class1{
  padding: 2%;
}
.class2{
  padding: 2%;
  display: flex;
  align-items: flex-start; /* 子元素顶部对齐 */
  font-size: 25px;
}


.board{
  background-color: #f7f7f7;
  padding: 5%;
}

.message-table :deep(.ant-table-row-expand-icon-cell) {
  display: none;
}

.message-table :deep(.ant-table-expand-icon-th) {
  display: none;
}

.pretty {
  font-size: 20px; /* 基础尺寸 */
  --icon-size: 1em; /* 图标继承字体尺寸 */
}

.message-table :deep(td[data-index="structure"].ant-table-cell) {
  padding: 0 !important; /* 移除该列单元格内边距 */
  position: relative; /* 为子元素定位提供基准 */


}

/* 固定表格列宽 */
table {
  table-layout: fixed;
}

/* 消息类型标签自适应 */
.message-type-tag {
  white-space: normal;
  word-break: break-word;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

/* Ensure nested table cells allow wrapping */
.nested-table th,
.nested-table td {
  width: auto; /* 允许列宽自动调整 */
  padding: 8px 12px;
  /* 修改单元格换行策略 */
  white-space: normal !important;
  word-break: break-all;
  min-width: 120px; /* 根据内容设置最小宽度 */
}


/* 响应式调整 */
@media (max-width: 768px) {
  .nested-table th,
  .nested-table td {
    font-size: 0.875rem;
  }
  
  .message-type-tag {
    font-size: 0.75rem;
    padding: 2px 8px;
  }
}

.error-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #afe3a1;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  content: "✓";
  position: absolute;
  left: 2px;
  bottom: 2px;
  background-color: white;
  color: #22c55e;
  transition: .4s;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

input:checked + .slider {
  background-color: #fbd4d4;
}

input:checked + .slider:before {
  content: "×";
  transform: translateX(20px);
  color: #ef4444;
}
</style>