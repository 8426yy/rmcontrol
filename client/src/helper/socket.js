import prompt from '@system.prompt'
import websocketfactory from '@system.websocketfactory'
const channel = new BroadcastChannel('statechannel')

var ws = null
var isOpen = false

function create(address) {
    //创建websocket实例
    channel.postMessage({ kind: 'open', data: `create start connect with ${address}` })
    try{
        ws = websocketfactory.create({
            url: address,
            header: {
                'content-type': 'application/json'
            },
            protocols: ['protocol']
        })
    }
    catch(err)
    {
        channel.postMessage({ kind: 'open', data: `create connect fail check with address` })
    }
  
    //连接打开事件的监听
    ws.onopen = function () {
        isOpen = true
        channel.postMessage({ kind: 'open', data: `create connect with ${address} success` })
    }

    //消息事件的监听
    ws.onmessage = function (data) {
        channel.postMessage({ kind: 'rec', data: `receive data from pc`,value:data.data })

    }

    //错误事件的监听
    ws.onerror = function (e) {
        channel.postMessage({ kind: 'err', data: `socket error occured ` })
    }

    //关闭连接事件的监听
    ws.onclose = function (data) {
        isOpen = false
        channel.postMessage({ kind: 'close', data: `close connect with ${address} code=${data.code}` })
    }
}

function send(message) {
    if (isOpen) {
        ws.send({
            data: message,
            success: function () {
                channel.postMessage({ kind: 'send', data: `send ${message} success` })
            },
            fail: function () {
                channel.postMessage({ kind: 'send', data: `send ${message} fail` })
            }
        })
    }
    else {
        prompt.showToast({ message: '没有一个有效的连接' })
    }

}
function close() {
    if (isOpen) {
        ws.close({
            success: function () {
                isOpen = false
                channel.postMessage({ kind: 'close', data: `close connect success` })
            },
            fail: function () {
                prompt.showToast({ message: '没有正在运行的链接' })
                channel.postMessage({ kind: 'close', data: `close connect fail` })
            }
        })
    }
}

var keep=setInterval(() => {
    if(isOpen)
    {
        send({kind:'c',data:'keep alive'})
    }
  }, 5000)


export default {
    ws,isOpen, create, send, close
}
