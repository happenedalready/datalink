import { getRequest, postRequest } from "./api";
import useSetting from "@/composables/setting";
import { DataType } from '@/types';

const setting = useSetting()
export const completion = async (text: string) => {
  const res = await postRequest({
    url: '/completions',
    data: {
      "messages": text
    },
  })
  return res
}

export const finderror = async (key: any) => {
  const res = await postRequest({
    url: '/finderror',
    data: {
      "messages": key,
    },
  })
  return res
}


