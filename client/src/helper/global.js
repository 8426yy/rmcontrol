/**
 * @file 全局能力的配置与获取
 */

function getGlobalRef() {
  return Object.getPrototypeOf(global) || global
}

const quickappGlobal = getGlobalRef()

/**
 * 设置全局(被APP与Page共享)数据；
 * @param key {string}
 * @param val {*}
 */
function setGlobalData(key, val) {
  quickappGlobal[key] = val
}
function setKeyValue(key1, key2, val) {
  try {
    quickappGlobal[key1][key2] = val
  }
  catch (err) {
    quickappGlobal[key1] = {}
    quickappGlobal[key1][key2] = val
  }

}
function getKeyValue(key1, key2) {
  try {
    return quickappGlobal[key1][key2]
  } catch (err) {
    return ''
  }
}
/**
 * 获取全局(被APP与Page共享)数据；
 * @param key {string}
 * @return {*}
 */
function getGlobalData(key) {
  return quickappGlobal[key]
}

// 两个方法默认定义在全局
setGlobalData('setGlobalData', setGlobalData)
setGlobalData('getGlobalData', getGlobalData)
setGlobalData('setKeyValue', setKeyValue)
setGlobalData('getKeyValue', getKeyValue)
export default { setGlobalData, getGlobalData, setKeyValue , getKeyValue}
