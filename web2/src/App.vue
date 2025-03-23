<script setup lang="ts">
import dayjs from 'dayjs'
import { ClearOutlined, LoadingOutlined, SettingOutlined, GithubOutlined } from '@ant-design/icons-vue'
import { completion, finderror } from '@/api'
import ReplayMessage from './components/ReplayMessage.vue'
import SendMessage from './components/SendMessage.vue'
import SettingModal from './components/setting.vue'
import useSetting from '@/composables/setting'
import useMessages from '@/composables/messages'
import { nextTick } from 'vue'

import LoadingMask from "@/components/LoadingMask.vue"; 
import { io } from "socket.io-client";

const loading = ref(false);

const toggleLoading = () => {
  initWebSocket()
  console.log("loading改了")
  loading.value = !loading.value
};
const loadingMessage = ref("请稍候，正在处理数据...");
let socket:any = null;

const initWebSocket = () => {
  if (socket) {
    console.warn("WebSocket 已经初始化");
    return;
  }

  // 连接 Socket.IO 服务器
  socket = io("http://localhost:5000", {
    transports: ["websocket"], // 强制使用 WebSocket
    reconnection: true,        // 开启自动重连
    reconnectionAttempts: 5,   // 失败 5 次后停止重连
    reconnectionDelay: 3000,   // 每次重连间隔 3 秒
  });

  // 监听 WebSocket 连接成功
  socket.on("connect", () => {
    console.log("✅ WebSocket 连接成功");
  });

  // 监听后端消息
  socket.on("loadingMessage", (message:any) => {
    loadingMessage.value = message.message;
  });

  socket.on("loading", (status:any) => {
    loading.value = status;
  });

  // 监听 WebSocket 断开
  socket.on("disconnect", (reason:any) => {
    console.warn("❌ WebSocket 断开:", reason);
  });

  // 监听 WebSocket 错误
  socket.on("connect_error", (error:any) => {
    console.error("❌ WebSocket 连接错误:", error);
  });
};
// ----------------------------

const setting = useSetting()

const state = reactive({
  message: '',
  loadding: false,
  visible: false,
})
const createdAt = dayjs().format('YYYY-MM-DD HH:mm:ss')

const messages = useMessages()

const sendMessage = async (event: { preventDefault: () => void }) => {
  event.preventDefault() // 阻止默认事件
  state.loadding = true
  
  console.log(messages.messages.value)
  
  messages.addMessage({
    username: "user",
    msg: state.message,
    type: 1,
  })
  let question = state.message
  console.log("输入的"+state.message)
  state.message = ""

  const data: string = await completion(question)

  loading.value = false;

  let str = JSON.stringify(data);
  console.log("msg:"+str);
  const replyMessage = str
  messages.addMessage({
    username: "chatGPT",
    msg: replyMessage,
    type: 0,
  })
  state.loadding = false

}

const clearMessages = () => {
  messages.clearMessages()
}

const sendMessage2 = async (key:any) => {
  const data: any = await finderror(key)

  loading.value = false;  // 这里把 loading 设置为了 false
  
  let str = JSON.stringify(data);
  const replyMessage = str
  messages.addMessage({
    username: "chatGPT",
    msg: replyMessage,
    type: 0,
  })
  state.loadding = false
}

let refresh = reactive({ showRefresh: true })
	// isClickRefresh监听子组件事件
const isClickRefresh = (datas:any) => { // 有参数就把()换成参数(自定义)名称，下面调用
    console.log("父组件触发了，发送错误信息"+datas)
		refresh.showRefresh = false
  nextTick(() => {
      sendMessage2(datas)

    refresh.showRefresh = true
    })
    toggleLoading();
  }

</script>

<template>
  <LoadingMask :visible="loading" :message="loadingMessage" />

  <div id="layout">
    <header id="header" class="bg-dark-50 text-white h-10 select-none">
      <LoadingOutlined v-if="state.loadding" class="pl-3 cursor-pointer" />
      <span class="text-size-5 pl-5">航空数据链系统</span>

      <span class="float-right pr-3 pt-2">
        <a-tooltip>
        <template #title>清除聊天记录</template>
        <a-popconfirm title="确定清除本地所有聊天记录吗?" ok-text="是的" cancel-text="再想想" @confirm="clearMessages">
          <ClearOutlined class="pl-3 cursor-pointer" />
        </a-popconfirm>
      </a-tooltip>

      <a-tooltip>
        <template #title>设置</template>
        <SettingOutlined class="pl-3 cursor-pointer" @click="state.visible = true" />
      </a-tooltip>

      </span>
    </header>

    <div id="layout-body">
      <main id="main">
        <div class="flex-1 relative flex flex-col">
          <!-- header -->
          <!-- content -->
          <div class="flex-1 inset-0 overflow-hidden bg-transparent bg-bottom bg-cover flex flex-col">
            <!-- dialog -->
            <div class="flex-1 w-full self-center">
              <div class="relative px-3 py-1 m-auto flex flex-col">
                <div class="mx-0 my-1 self-center text-xs text-gray-400">
                  {{ createdAt }}
                </div>
                  <div v-for="msg in messages.messages.value">
                  <SendMessage v-if="msg.type === 1" :message="msg" class="send" />
                  <ReplayMessage v-else :propMessage="msg" class="replay" @isClickRefresh="isClickRefresh" />
                 </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <footer id="footer">
      <div class="relative p-4 w-full overflow-hidden text-gray-600 focus-within:text-gray-400 flex items-center">
        <a-textarea v-model:value="state.message" :auto-size="{ minRows: 3, maxRows: 5 }" placeholder="请输入消息..."
          @pressEnter="sendMessage($event)"
          class="appearance-none pl-10 py-2 w-full bg-white border border-gray-300 rounded-full text-sm placeholder-gray-800 focus:outline-none focus:border-blue-500 focus:border-blue-500 focus:shadow-outline-blue" />
        <span class="absolute inset-y-0 right-0 bottom-6 pr-6 flex items-end">
          <a-button shape="round" type="primary" @click="toggleLoading(); sendMessage($event)">发送</a-button>
        </span>
      </div>
    </footer>

    <setting-modal v-model:visible="state.visible" />
  </div>
</template>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
}

#layout {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background-color: #f0f2f5;
  margin-left: 0;
  margin-right: 0;
}

#header {
  box-shadow: 2px 5px 5px 0px rgba(102, 102, 102, 0.5);
  flex-shrink: 0;
  height: 6%;
}

#layout-body {
  flex-grow: 2;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding-left: 10%;
  padding-right: 10%;
}

#footer {
  border-top: 1px rgb(228, 228, 228) solid;
  /* height: 100px; */
  flex-shrink: 0;
  padding-left: 15%;
  padding-right: 15%;
}

#main {
  flex-grow: 2;
}

.replay {
  float: left;
  clear: both;
}

.send {
  float: right;
  clear: both;
}
</style>
