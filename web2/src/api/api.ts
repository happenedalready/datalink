import axios from 'axios'

const api = axios.create({
  baseURL: '/api',  // 修改这里，使用相对路径
})


api.interceptors.response.use(
  response => {
    return Promise.resolve(response.data)
  },
)

export function getRequest(config: any): Promise<any> {
  return api.request({ ...config, method: 'GET' })
}

export function postRequest(config: any): Promise<any> {
  return api.request({ ...config, method: 'POST' })
}

export default api
