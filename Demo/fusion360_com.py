# encoding: utf-8

from pywinauto.application import Application
import pywinauto
# from pywinauto_recorder.player import *

# fusion360 실행 / 오류없이 실행
# app = Application(backend="uia").start(r"C:\Users\break\AppData\Local\Autodesk\webdeploy\production\6a0c9611291d45bb9226980209917c3d\FusionLauncher.exe",wait_for_idle=False)
# 프로그램 실행 될 동안 기다리기
# time.sleep(90)

# 실행중 프로세스 받아오기
procs = pywinauto.findwindows.find_elements()

# 실행 중 프로세스에서 fusion360 찾기
for proc in procs:
    if proc.name == 'Autodesk Fusion 360 (Personal - Not for Commercial Use)':
        print("찾았다!")
        break

# 프로세스로 fusion360 연결
app = Application(backend="uia").connect(process=proc.process_id)

# dialog 연결
dig = app['{}'.format(proc.name)]

# 사용 가능한 매소드 출력
# dig.print_control_identifiers()


def makeblock(dig):
    # shift + s 로 .f3d 파일 생성
    dig.set_focus()
    pywinauto.keyboard.send_keys("{VK_SHIFT down}S""{VK_SHIFT up}")
    # pywinauto.keyboard.send_keys("{VK_CONTROL down}Z""{VK_CONTROL up}")
