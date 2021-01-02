import bluetooth from '@system.bluetooth'
import prompt from '@system.prompt'
function bluetoothinit() {
    bluetooth.onadapterstatechange = function (data) {
        if (!data.available) {
            setKeyValue('devdata','vaild',false)
        }
        console.log("adapterState changed, now is", data.available);
    };
    //注册设备连接状态监听
    bluetooth.onbleconnectionstatechange = function (data) {
        console.log(`handling device state change: deviceId = ${data.deviceId}, connected = ${data.connected}`)
        if (!data.connected) {
            bluetooth.onblecharacteristicvaluechange = null
            prompt.showToast({
                message: "蓝牙已经断开"
            })
        }
    },
        blueopenadpter()
}
function blueopenadpter() {
    //初始化蓝牙模块
    bluetooth.openAdapter({
        operateAdapter: true,
        success: function () {
            console.log("open bluetooth adpter success");
        },
        fail: function (data, code) {
            console.log(`open bluetooth adpter fail, code = ${code}`);
            if (code === 10001) {
                //蓝牙未打开，提示用户打开蓝牙
            }
        },
        complete: function () {
            console.log("complete");
        }
    });
}
function createBLEConnection(data) {
    return new Promise((resolve, reject) => {
        let deviceId = data.deviceId
        let name = data.name
        bluetooth.createBLEConnection({
            deviceId,
            success(res) {
                setKeyValue('devdata','id',deviceId)
                setKeyValue('devdata','name',name)
                getBLEDeviceServices(deviceId).then(() => {
                    console.log('getservice success')
                    resolve(deviceId)
                }).
                    catch((data, code) => {
                        console.log('getservice inter fail')
                        reject(data, code)
                    })
            },
            fail: function (data, code) {
                console.log('getservice fail')
                reject(data, code)
            }
        })
    })
}

function getBLEDeviceServices(deviceId) {
    console.log(deviceId)
    return new Promise((resolve, reject) => {
        bluetooth.getBLEDeviceServices({
            deviceId,
            success(res) {
                for (let i = 0; i < res.services.length; i++) {
                    if (res.services[i].uuid == '0000FFE0-0000-1000-8000-00805F9B34FB') {
                        getBLEDeviceCharacteristics(deviceId, res.services[i].uuid).then(() => {
                            console.log('getcharcat success')
                            resolve()
                        }).catch((data, code) => {
                            console.log('getcharcat inter fail')
                            reject(data, code)
                        })
                    }
                }
            },
            fail: function (data, code) {
                console.log('getcharcat  fail')
                reject(data, code)
            }
        })
    })
}

function getBLEDeviceCharacteristics(deviceId, serviceId) {
    return new Promise((resolve, reject) => {
        bluetooth.getBLEDeviceCharacteristics({
            deviceId,
            serviceId,
            success(res) {
                for (let i = 0; i < res.characteristics.length; i++) {
                    let item = res.characteristics[i]
                    if (item.properties.notify || item.properties.indicate) {
                        if (item.uuid == "0000FFE1-0000-1000-8000-00805F9B34FB") {
                            bluetooth.onblecharacteristicvaluechange = function (data) {
                                let list = $operate.dataparse(data.value)
                                datalist.push(...list)
                            }
                            bluetooth.notifyBLECharacteristicValueChange({
                                deviceId,
                                serviceId,
                                characteristicId: item.uuid,
                                state: true,
                                success() {
                                    console.log('notify success')
                                    setKeyValue('devdata','id',deviceId)
                                    setKeyValue('devdata','service',serviceId)
                                    setKeyValue('devdata','character',item.uuid)
                                    setKeyValue('devdata','vaild',true)
                                    prompt.showToast({
                                        message: '订阅成功'
                                    })
                                    resolve()
                                },
                                fail(data, code) {
                                    console.log('notify fail')
                                    reject(data, code)
                                }
                            })
                        }
                    }
                }

            },
            fail(data, code) {
                console.log('notify failed')
                reject(data, code)
            }
        })
    })
}

function bluecloseconnect() 
{
    let vaild=getGlobalData('devdata').vaild
    if (vaild==false) {
        prompt.showToast({ message: "当前没有有效的连接" })
        return
    }
    bluetooth.onblecharacteristicvaluechange = null
    bluetooth.closeBLEConnection({
        deviceId: getKeyValue('devdata','id'),
        success: function () {
            prompt.showToast({
                "message": "解除完成"
            })
            console.log("close bluetooth connect success")
        },
        fail: function (data, code) {
            console.log(`close bluetooth connect fail, code = ${code}`)
        },
        complete: function () {
            console.log("close bluetooth connect complete")
            setKeyValue('devdata','vaild',false)
        }
    })
}

function bluetoothexit() {
    bluetooth.onadapterstatechange = null
    bluetooth.onbleconnectionstatechange = null
    bluetooth.onblecharacteristicvaluechange = null
    bluetooth.ondevicefound = null
    //注销蓝牙模块
    bluetooth.closeAdapter({
        //是否关闭系统蓝牙开关，默认false，此操作会直接关闭系统蓝牙，为了不影响用户其他蓝牙设备的体验，不建议设置为true
        operateAdapter: false,
    });
}

function bluestopdiscover() {
    bluetooth.getAdapterState({
        success: function (data) {
            if (data.discovering) {
                bluetooth.ondevicefound = null
                bluetooth.stopDevicesDiscovery({})
            }
        }
    })
}

function bluetoothdiscover() {
    return new Promise((resolve, reject) => {
        bluetooth.ondevicefound = function (data) {
            console.log("new device list has founded");
            data.devices.forEach(device => {
                if (!device.name && !device.localName) {
                    return
                }
                const foundDevices = devices
                const idx = $utils.inArray(foundDevices, 'deviceId', device.deviceId)
                if (idx === -1) {
                    resolve(device)
                    devices.push(device)
                } else {
                    devices.splice(idx, 1, device)
                }

            });
        }
        bluetooth.startDevicesDiscovery({
            //     services: ['0000FFE0-0000-1000-8000-00805F9B34FB', '0000FEE7-0000-1000-8000-00805F9B34FB'],
            allowDuplicatesKey: false,
            success: function () {
                console.log("success find");
            }
        })
    })
}


export default
    {


    }

