#!/user/bin/env pyhton解释器路径
# -*-coding:utf-8-*- 脚本编码
import os, time, msvcrt, platform
from configparser import ConfigParser
from datetime import datetime
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from playwright.sync_api import Playwright, sync_playwright

file100 = 'config.ini'

def file1():  # 文件读写
    #global answer
    if os.path.exists(file100):  # 文件存在检测
        # printer('file existed')
        cf = ConfigParser()
        cf.read(file100)
        username = cf.get('main', 'uid')
        password = cf.get('main', 'pwd')
        testurl = cf.get('main', 'url')
        mode = cf.get('main', 'mode')
        wifi = cf.get('main', 'wifi')
        local = cf.get('main','local')

        '''
        if local != '0':
            lpath = cf.get('main','lpath')
            return username, password, testurl, mode, local, lpath
        else:'''
        return username, password, testurl, mode, local, wifi

    else:
        #printer('config file not fund')
        printer('input username')
        username = input()
        printer('input password')
        password = pwd_input()
        print(' ')
        printer('choose mode  0 | 1')
        printer('1 for headless')
        mode = input()
        printer('choose local 0 | 1')
        printer('chromium | chrome')
        local = input()
        printer('1 for wifi on')
        wifi = input()
        '''
        if local == '1':
            answer = search()
            if answer == -1:
                printer('chrome not found')
                answer = None
            else:
                printer('chrome existed')
                printer(answer)'''

        testurl = 'http://so.cn'
        t0 = '\n'

        with open(file100, "w") as file:
            file.write(
                '[main]' + t0 +
                'uid = ' + str(username) + t0 +
                'pwd = ' + str(password) + t0 +
                'mode = ' + str(mode) + t0 +
                'local = ' + str(local) + t0 +
                'url = ' + str(testurl) + t0 +
                'wifi = ' + str(wifi) + t0)
            file.close()
        for step in track(range(100), description="Writing..."):
            time.sleep(0.01)
        printer('config is generated')


        '''
        if local != '0':
            lpath = str(answer)
            return username, password, testurl, mode, local, lpath
        else:'''
        return username, password, testurl, mode, local, wifi

def search():#chrome查找
    path = 'c:\\'
    name = 'chrome.exe'
    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)+ str('\chrome.exe')
            return root
    return -1

def printer(content):#彩色输出
    console = Console()
    time1 = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    console.print(time1, end='')
    console.print(content, style="yellow")

def pwd_input():#密码
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n': # 如果是换行，则输入结束
             break
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号
             if chars:
                 del chars[-1]
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
                 msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
    return (''.join(chars) )

def password1():
    console = Console()
    if input() == '00':
        return 0
    else:
        with console.screen(style="bold white on red") as screen:
            text = Align.center("[blink]error[/blink]", vertical="middle")
            screen.update(Panel(text))
            time.sleep(2)
    password1()

def os_checker():
    os_version = platform.platform()
    os.system('mode con cols=45 lines=10')
    if 'Windows-10' in os_version:
        printer('script started')
        #printer('haha windows10')
    if 'Windows-11' in os_version:
        printer('script started' + ':pile_of_poo:')

def run(playwright: Playwright) -> None:
    global browser, channel1, lpath,wifi
    result1 = file1()
    username = result1[0]
    password = result1[1]
    testurl = result1[2]
    mode = result1[3]
    local = result1[4]
    wifi = result1[5] #lpath

    if mode == '0':
        mode = False
    else:
        mode = True

    if local == '0':
        channel1 = None #Chromium
        #lpath = None
    if local == '1':
        channel1 = 'chrome'
        #lpath = result1[5]

    browser = playwright.chromium.launch(
            headless=mode,channel=channel1)
    #,executable_path=lpath)
    context = browser.new_context()
    page = context.new_page()
    printer('url:' + testurl)
    page.goto(testurl)
    
    time.sleep(1)
    printer('username: ' + username)
    page.fill('//*[@id="userId"]', username)
    printer('password: ******')
    page.fill('//*[@id="passwordText"]', password)
    printer('submit')
    page.click('text=登 录')

    if wifi == '1':
        os.system('PowerShell.exe -file wifi.ps1')

    printer('input 00 to log out')
    if password1()==0:
        page.click('//*[@id="userPad"]/ul/li[4]/button')
        printer('success!')
        time.sleep(15)
        exit(1)

    context.close()
    browser.close()


if __name__ == '__main__':
    file1()
    os_checker()
    with sync_playwright() as playwright:
        run(playwright)