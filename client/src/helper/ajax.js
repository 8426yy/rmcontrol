import $fetch from '@system.fetch'
import $utils from './utils'

function requestHandle(params) {
  console.log(`当前正在发起请求的 Url 是： ${params.url}`)
  return new Promise((resolve, reject) => {
    $fetch.fetch({
      url: params.url,
      method: params.method,
      data: params.data,
      success: data => {
        const serverResponse = JSON.parse(data.data)
        if (serverResponse.success || serverResponse.status === 0) {
          resolve(serverResponse.result || serverResponse.value)
        } else {
          reject(serverResponse.message)
        }
      },
      fail: (data, code) => {
        console.log(`request fail, code = ${code} `, data)
        reject(data)
      },
      complete: data => {
        reject(data)
      }
    })
  })
}

export default {
  post: function(url, params, op) {
    return requestHandle({
      method: 'post',
      url: url,
      data: params
    })
  },
  get: function(url, params, op) {
    return requestHandle({
      method: 'get',
      url: $utils.queryString(url, params)
    })
  }
}
