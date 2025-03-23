<script setup lang="ts">
import { message as messageTip } from 'ant-design-vue'
import { Viewer } from '@bytemd/vue-next'
import useMessages from '@/composables/messages'
import { CopyOutlined, DeleteOutlined,UserOutlined } from '@ant-design/icons-vue'
import { useClipboard } from '@vueuse/core'
import { TMessage } from '@/types'

const messages = useMessages()
const { copy } = useClipboard({})
defineProps<{
  message: TMessage;
}>()

const copyIt = (msg: string) => {
  copy(msg)
  messageTip.success('Copied')
}

const deleteIt = (meseage: TMessage) => {
  messages.messages.value = messages.messages.value.filter((item) => item !== meseage)
  messageTip.success('Deleted')
}
</script>

<template>
  <div class="my-2 self-end flex items-center flex-row" >
    <DeleteOutlined class="pr-1 cursor-pointer self-end !text-gray-400" @click="deleteIt(message)" />
    <div class="p-1 rounded-t-lg rounded-l-lg bg-blue-300 shadow text-sm min-w-10 max-w-500">
      <!-- <pre class="max-w-80 !mb-0 m-2">{{ message.msg }}</pre> -->
      <Viewer class="max-w-120 m-2" :value="message.msg" />
    </div>
    <div class="class1"><UserOutlined class = "class2"/></div>
  </div>
</template>

<style scoped>
.ant-card-body {
  padding: 5px !important;
}

.a {
  color: black;
  background-color: white;
}

.b {
  color: white;
  background-color: rgba(96, 165, 250, var(--un-bg-opacity));
}

p {
  margin-bottom: 0 !important;
}

.class1{
  padding: 5%;

}

.class2{
  padding: 5%;
  display: flex;
  align-items: flex-start; /* 子元素顶部对齐 */
  font-size: 25px;
}

</style>