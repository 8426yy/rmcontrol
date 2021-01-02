"""
author: lixk
description: 本工具包用于执行子进程，实时获取子进程执行过程中输出的数据并打印到控制台，然后返回状态码和执行结果
"""
import subprocess
import sys
import asyncio
import threading

def run(cmd, shell=False) -> (int, str):
    """
    开启子进程，执行对应指令，控制台打印执行过程，然后返回子进程执行的状态码和执行返回的数据
    :param cmd: 子进程命令
    :param shell: 是否开启shell
    :return: 子进程状态码和执行结果
    """
    print('\033[1;32m************** START **************\033[0m')
    p = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p)
    result = []
    while p.poll() is None:
        line = p.stdout.readline().strip()
        if line:
            line = _decode_data(line)
            result.append(line)
            print('\033[1;35m{0}\033[0m'.format(line))
        # 清空缓存
        sys.stdout.flush()
        sys.stderr.flush()
    # 判断返回码状态
    if p.returncode == 0:
        print('\033[1;32m************** SUCCESS **************\033[0m')
    else:
        print('\033[1;31m************** FAILED **************\033[0m')
    
    return p.returncode, '\r\n'.join(result)


def _decode_data(byte_data: bytes):
    """
    解码数据
    :param byte_data: 待解码数据
    :return: 解码字符串
    """
    try:
        return byte_data.decode('UTF-8')
    except UnicodeDecodeError:
        return byte_data.decode('GB18030')



if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # coroutine1=run('ping www.baidu.com')
    # coroutine2=pr()
    # loop.run_until_complete(asyncio.wait([coroutine1,coroutine2]) )
     t=threading.Thread(target=run,args=['ping www.baidu.com'])
     t.start()
     print(1)
    # run('ping www.baidu.com')
    # print(1)


