import re, os
from queue import Queue
import subprocess
import sys
import ctypes
if __name__ == "__main__":
    from reg import *
else:
    from .reg import *

user32 = ctypes.WinDLL('user32')
hWnd = None

if __name__ == "__main__":
    from reg import *
else:
    from .reg import *

SERVICES_UNUSED = ["CryptSvc", "Dhcp", "Dnscache", "WerSvc", "hidserv", "Spooler", "RemoteRegistry"]

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

    try:
        scmd("net accounts /MINPWLEN:8")
        
        # scmd("chcp 65001")
        # scmd(f"secedit /import /CFG {file}")
    except subprocess.CalledProcessError:
        sys.stderr.write("error")

re_share = re.compile(r"^(\w+[$])\s*([\w:\\]+)\s*([^\s]+).*$")
"""
PC03 조치 함수
type : solve
"""
def solve_pc03():
    results = Queue()
    cmd("chcp 65001")
    shared = []

    lines = cmd("net share").split("\n")
    for line in lines:
        if m := re_share.match(line):
            shared.append(m.group(1))
    
    if shared:
        try:
            for d in shared:
                cmd(f"net share {d} /delete")
        except subprocess.CalledProcessError:
            sys.stderr.write("Permisson error")


"""
PC04 조치 함수
type : link
"""
def solve_pc04():
    pw("services.msc")

"""
PC05 조치 함수 : 프로그램 제거창을 띄워 상용 메신저 제거
type : link
"""
def solve_pc05():
    try:
        cmd("control appwiz.cpl")
    except subprocess.CalledProcessError:
        pass

"""
PC06 조치 함수 : 디스크 관리 창을 띄워 NTFS포맷 수동 조치
type : link
"""
def solve_pc06():
    cmd("diskmgmt.msc")

def solve_pc15():
    rpath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SetUp\recoveryconsole"
    rname = r"securitylevel"
    set_registry_value(rpath, rname, 0)


def solve_pc16():
    pass

if __name__ == "__main__":
    #subprocess.run(['lusmgr.msc'], shell=True, check=True)
    #subprocess.run(['net accounts','/MINPWLEN:0'], shell=True, check=True)
    #solve_pc05()
    rpath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SetUp\recoveryconsole"
    rname = r"securitylevel"
    print(get_registry_value(rpath, rname))
    print("hello")
    set_registry_value(rpath, rname, 1)
    print("set")
    print(get_registry_value(rpath, rname))
    
