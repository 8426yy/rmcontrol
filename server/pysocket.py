from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
import time
import datetime
import ast
import pyinput as keyin
import pywindow as window
import pycmd as cmd
app = Flask(__name__)
sockets = Sockets(app)

def wordin(data):
    keyin.textInput(data)

def mousein(data):
    keyin.mouseMove(data)

def keyinput(data):
    keyin.wordInput(data)

def mouseMoveto(data):
    keyin.mouseMoveto(data)

def hotkey(data):
    keyin.hotkey(data)

def mousepress(data):
    keyin.mousePress(data)

def windowoperate(data):
    ret = window.operate(data)
    return ret

def conkeep(data):
    pass

def reset():
    keyin.refresh()
    window.windowreset()




switch = {'w': wordin,
          'h': hotkey,
          'k': keyinput,

          'm': mousein,
          'p': mousepress,
          't': mouseMoveto,

          's': windowoperate,

          'c': conkeep,     
          }


def default(data):                          # 默认情况下执行的函数
    print('No such case')


def control(data, ws):
    ret = switch.get(data.get('kind'), default)(data.get('data'))
    if ret is not None:
        ws.send(json.dumps(ret))


@sockets.route('/')
def rec(ws):
    while not ws.closed:
        msg = ws.receive()
        if msg:
            try:
                data = ast.literal_eval(msg)
                print(data)
                control(data, ws)
            except:
                print('something wrong occured')
                now = json.dumps({'kind':'i', 'data':datetime.datetime.now().isoformat()})
                ws.send(now)
                print(f'i sent:{now}')
    reset()
    print('ws is closed now')


if __name__ == "__main__":
    server = pywsgi.WSGIServer(
        ('192.168.43.223', 6811), application=app, handler_class=WebSocketHandler)
    server.serve_forever()
