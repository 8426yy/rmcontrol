# 古木遥控
## 1 Server
windows端,python版本3.6，安装库flask，flask-sockets，pyautogui，pywin32，更改main中地址为局域网地址或公网地址，启动pysockets.py  
## 2 Client
安装QuickappIDE,可在https://www.quickapp.cn/docCenter/IDEPublicity进行下载，安装后设置client为工作目录，打开工程，等待npm安装即可修改。
## 3 部署
电脑端启动server/pysocket.py,移动端安装resources/quickapp_debugger_v1080.apk与
resources/quickapp_platform_preview_release_v1080.apk
将resources/com.gm.yaokong.debug.rpk移动至存储目录，启动快应用调试器，点击本地安装，选择rpk即可启动。
