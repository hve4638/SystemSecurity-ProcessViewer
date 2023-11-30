import re, os
from queue import Queue
import subprocess
import sys
import ctypes

user32 = ctypes.WinDLL('user32')
hWnd = None

if __name__ == "__main__":
    from reg import *
else:
    from .reg import *


"""
PC01 조치 함수
type : link
"""
def solve_pc01():
    try:
        subprocess.run(['lusmgr.msc'], shell=True, check=True)
    except subprocess.CalledProcessError:
        user32.MessageBoxW(None, '관리 창을 띄울 수 없습니다', 'Error!', 0)

"""
PC02 조치 함수
type : solve
"""
def solve_pc02():
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    file = "./.tmp/__newpolicy"

    with open(file, "w", encoding="UTF-16") as f:
        f.write("[Unicode]")
        f.write("PasswordComplexity = 0\n")

    try:
        scmd("net accounts /MINPWLEN:8")
        
        scmd("chcp 65001")
        scmd(f"secedit /import /CFG {file}")
    except subprocess.CalledProcessError:
        sys.stderr.write("error")

def solve_pc03():
    pass

if __name__ == "__main__":
    #subprocess.run(['lusmgr.msc'], shell=True, check=True)
    #subprocess.run(['net accounts','/MINPWLEN:0'], shell=True, check=True)
    solve_pc02()
