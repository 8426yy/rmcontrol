const prompt = require('@system.prompt')
const router = require('@system.router')
const storage = require('@system.storage')

/**
 * @desc 显示菜单
 */
function showMenu() {
  const page = router.getState()
  const itemList =
    page.path === '/pages/main' ? ['保存桌面', '取消'] : ['保存桌面', '返回首页', '取消']
  const itemFuncMapping =
    page.path === '/pages/main' ? [createShortcut, null] : [createShortcut, gotoMain, null]
  prompt.showContextMenu({
    itemList,
    success: function (ret) {
      if (itemFuncMapping[ret.index]) {
        itemFuncMapping[ret.index]()
      }
    }
  })
}

/**
 * @desc 创建桌面图标
 * 注意：使用加载器测试`创建桌面快捷方式`功能时，请先在`系统设置`中打开`应用加载器`的`桌面快捷方式`权限
 */
function createShortcut() {
  const shortcut = require('@system.shortcut')
  shortcut.hasInstalled({
    success: function (ret) {
      if (ret) {
        prompt.showToast({
          message: '已创建桌面图标'
        })
      } else {
        shortcut.install({
          success: function () {
            prompt.showToast({
              message: '成功创建桌面图标'
            })
          },
          fail: function (errmsg, errcode) {
            prompt.showToast({
              message: `${errcode}: ${errmsg}`
            })
          }
        })
      }
    }
  })
}

function gotoMain() {
  let page = router.getState()
  console.log(page)
  if (page.path !== '/pages/main') {
    router.push({
      uri: '/pages/main'
    })
  }
}

function queryString(url, query) {
  let str = []
  for (let key in query) {
    str.push(key + '=' + query[key])
  }
  let paramStr = str.join('&')
  return paramStr ? `${url}?${paramStr}` : url
}

function setStorage(key, value) {
  // 设置storage
  storage.set({
    key,
    value: value,
    fail(data, code) {
      console.log(`setStorage fail, code = ${code}`)
    }
  })
}

function clearStorage() {
  storage.clear({
    success: function (data) {
      console.log('handling success')
    },
    fail: function (data, code) {
      console.log(`handling fail, code = ${code}`)
    }
  })
}

function getStorage(key) {
  return new Promise((resolve, reject) => {
    // 获取storage
    storage.get({
      key,
      default: '',
      success(data) {
        if (data) {
          resolve(data)
        }
        else
          reject()
      },
      fail(data, code) {
        console.log(`getStorage fail, code = ${code}`)
        reject({ data, code })
      }
    })
  })
}

function ascii2native(strAscii) {
  var output = "";
  var posFrom = 0;
  var posTo = strAscii.indexOf("\\u", posFrom);
  while (posTo >= 0) {
    output += strAscii.substring(posFrom, posTo);
    output += toChar(strAscii.substr(posTo, 6));
    posFrom = posTo + 6;
    posTo = strAscii.indexOf("\\u", posFrom);
  }
  output += strAscii.substr(posFrom);
  return output;
}

function toChar(str) {
  if (str.substr(0, 2) != "\\u") return str;
  var code = 0;
  for (var i = 2; i < str.length; i++) {
    var cc = str.charCodeAt(i);
    if (cc >= 0x30 && cc <= 0x39)
      cc = cc - 0x30;
    else if (cc >= 0x41 && cc <= 0x5A)
      cc = cc - 0x41 + 10;
    else if (cc >= 0x61 && cc <= 0x7A)
      cc = cc - 0x61 + 10;

    code <<= 4;
    code += cc;
  }
  if (code < 0xff) return str;

  return String.fromCharCode(code);
}
function isarray(a) {
  if (a && Array.isArray(a))
    return true
  return false
}

function isEmpty(obj) {
  if (typeof obj == "undefined" || obj == null || obj == "") {
    return true;
  } else {
    return false;
  }
}

function inArray(arr, key, val) {
  for (let i = 0; i < arr.length; i++) {
      if (arr[i][key] === val) {
          return i;
      }
  }
  return -1;
}

export default {
  showMenu,
  createShortcut,
  queryString,
  setStorage,
  getStorage,
  clearStorage,
  ascii2native,
  toChar,
  isEmpty,
  inArray,
  showToast(message = '', duration = 0) {
    if (!message) return
    prompt.showToast({
      message: message,
      duration
    })
  },
  route2theUrl(url, params, clear = false) {
    router.push({
      uri: url,
      params: params
    })
    if (clear) {
      router.clear()
    }
  }
}
