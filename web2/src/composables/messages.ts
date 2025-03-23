import { useStorage } from '@vueuse/core'
import { TMessage } from '@/types'
import dayjs from 'dayjs'


// const text = `[
//   {
//     "类型": "空域变更信息",
//     "结构": {
//       "空域类型": "禁飞区与限制区",
//       "通信频率": "指挥频率为132.000 MHz，应急频率为121.500 MHz"
//     }
//   },
//   {
//     "类型": "卫星预报信息",
//     "结构": {
//       "卫星预报": "侦察卫星GX-12",
//       "阵地位置": "北纬40.000度、东经116.000度",
//       "离开时间": "2025年1月21日06:00 UTC",
//       "空中目标任务": "空中侦察",
//       "空中目标型号": "GX-12",
//       "航迹所属国家/联盟/地区": "北约国防联盟"
//     }
//   }
// ]`;


// // 默认值
// const defaultMessages: TMessage[] = [
//   {
//     username: "chatGPT",
//     msg: text,
//     time: dayjs().format('HH:mm'),
//     type: 0,
//   },
// ]

// // 每次运行时，重置 localStorage 中的 'messages'
// localStorage.setItem('messages', JSON.stringify(defaultMessages))

// 使用 sessionStorage
const messages = useStorage<TMessage[]>('messages', [], sessionStorage)

// 每次加载页面时重置 messages
messages.value = []; // 或者 messages.value.length = 0;

console.log('初始化 messages:', messages.value)

export default function useMessages() {
  const addMessage = (message: TMessage) => {
    messages.value.push({
      username: message.username,
      msg: message.msg,
      time: message.time || dayjs().format('HH:mm'),
      type: message.type,
    })
  }

  const clearMessages = () => {
    messages.value = []
  }

  const getLastMessages = (num: number = 10) => {
    return messages.value.slice(-num)
  }

  const getLastTypeOneMessage = () => {
    // 反向遍历数组查找 type=1 的消息
    for (let i = messages.value.length - 1; i >= 0; i--) {
      if (messages.value[i].type === 1) {
        return messages.value[i]
      }
    }
    // 如果没找到返回 null
    return null
  }
  return {
    messages,
    addMessage,
    clearMessages,
    getLastMessages,
    getLastTypeOneMessage
  }
}
