import pyautogui
import pyperclip
import time
import asyncio
word_dict = {
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', 'Back': 'backspace',
    'q': 'q', 'w': 'w', 'e': 'e', 'r': 'r', 't': 't', 'y': 'y', 'u': 'u', 'i': 'i', 'o': 'o', 'p': 'p', 'a': 'a', 's': 's', 'd': 'd', 'f': 'f', 'g': 'g',
    'h': 'h', 'j': 'j', 'k': 'k', 'l': 'l', 'z': 'z', 'x': 'x', 'c': 'c', 'v': 'v', 'b': 'b', 'n': 'n', 'm': 'm', 'Esc': 'esc', 'Tab': 'tab', 'Caps': 'capslock',
    'Shift': 'shiftleft', 'Ctrl': 'ctrlleft', 'Alt': 'altleft', 'Win': 'winleft', 'Space': 'space', 'Enter': 'enter', 'ins': 'insert', 'del': 'delete', '←': 'left', '↓': 'down', '→': 'right', '↑': 'up',
    'Esc': 'esc', 'F1': 'f1', 'F2': 'f2', 'F3': 'f3', 'F4': 'f4', 'F5': 'f5', 'F6': 'f6', 'F7': 'f7', 'F8': 'f8', 'F9': 'f9', 'F10': 'f10', 'F11': 'f11', 'F12': 'f12'
}
keylist=['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright'],
key = set()

pyautogui.FAILSAFE = False
pyautogui.PAUSE=0

screenWidth, screenHeight = pyautogui.size()

def keyPress(word):
    pyautogui.keyDown(word)
    key.add(word)

def hotkey(data):
    pyautogui.hotkey(*[i.lower() for i in data])

def keyReserve(word):
    pyautogui.keyUp(word)
    key.remove(word)

def keyClick(word):
    pyautogui.press(word)


def default(word):
    print('knowless operate',word)


def refresh():
    for i in key:
        pyautogui.keyUp(i)
        key.remove(i)

def mouseReset(word):
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(x=1/2*screenWidth,y=1/2*screenHeight)
    pyautogui.mouseUp('left')
    pyautogui.mouseUp('middle')
    pyautogui.mouseUp('left')
    print(word)

def mousePress(word):
    pyautogui.mouseDown(button=word)

def mouseClick(word):
    pyautogui.click(button=word)

def mouseReserve(word):
    pyautogui.mouseUp(button=word)

def mouseScroll(word):
    pyautogui.scroll(word)

key_operate = {
    "press": keyPress,
    "click": keyClick,
    "reserve": keyReserve,
}

mouse_operate={
    "press": mousePress,
    "click": mouseClick,
    "reserve":mouseReserve,
    "scroll":mouseScroll,
    "reset":mouseReset
}


def textInput(text):
    pyperclip.copy(text)  # 先复制
    pyautogui.hotkey('ctrl', 'v')


def wordInput(data):
    op = data.get('operate')
    word = word_dict.get(data.get('word'), data.get('word').lower())
    key_operate.get(op, default)(word)

    
def keyDrive(data):
    pass


def mouseMove(data):
    pyautogui.moveRel(xOffset=data.get('x'), yOffset=data.get('y'), duration=data.get('time',0)/1000)
    print(data)

def mouseMoveto(data):
    pyautogui.moveTo(x=(float(data.get('x'))*screenWidth), y=(float(data.get('y'))*screenHeight), duration=data.get('time',0)/1000,tween=pyautogui.easeInOutQuad)
    print(data)


def mousePress(data):
    op = data.get('operate')
    word =data.get('button')
    mouse_operate.get(op, default)(word)