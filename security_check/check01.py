import re, os
from queue import Queue
from .reg import *

# 이후 파일로 분리해 저장 필요
SERVICES_UNUSED = ["CryptSvc", "Dhcp", "Dnscache", "WerSvc", "hidserv", "Spooler", "RemoteRegistry"]
UNAUTHORIZED_MASSENGER = [
    "C:\\Program Files (x86)\\Kakao\\KakaoTalk"
]

MAXIMUM_PASSWD_AGE = "Maximum password age (days):"
MINIMUM_PASSWD_AGE = "Minimum password age (days)"
PASSWD_HISTORY_COUNT = "Length of password history maintained"
MINIMUM_PASSWD_LENGTH = "Minimum password length"
PASSWD_COMPLEXITY = "PasswordComplexity"

r = re.compile(r"^.+[:]\s*([^\s]+).*$")
re_split_colon = re.compile(r"^(.+)\s*[:]\s*([^\s]+).*$")
re_split_equalsign = re.compile(r"^(.+)\s*[=]\s*([^\s]+).*$")

def test_check(results:Queue):
    while not results.empty():
        print(results.get())

def check_pc01():
    results = Queue()
    cmd("chcp 65001")

    lines = cmd("net accounts").split("\n")
    maximum_pass_age = None
    minimum_pass_age = None
    history_count = None
    for line in lines:
        if MAXIMUM_PASSWD_AGE in line:
            maximum_pass_age = re_split_colon.match(line).group(2)
        if MINIMUM_PASSWD_AGE in line:
            minimum_pass_age = re_split_colon.match(line).group(2)
        if PASSWD_HISTORY_COUNT in line:
            history_count = re_split_colon.match(line).group(2)
    
    if maximum_pass_age is None or minimum_pass_age is None or history_count is None:
        results.put({
            "id" : "PC-01",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "점검에 실패했습니다"
        })

    if int(maximum_pass_age) < 90:
        results.put({
            "id" : "PC-01",
            "sub-id" : "PC-01-MINPWAGE",
            "type" : "error",
            "reason" : "최대 암호 사용 기간이 90일보다 적습니다"
        })
    if int(minimum_pass_age) == 0:
        results.put({
            "id" : "PC-01",
            "sub-id" : "PC-01-MAXPWAGE",
            "type" : "error",
            "reason" : "최소 암호 사용 기간이 지정되지 않았습니다"
        })
    if history_count == "None":
        results.put({
            "id" : "PC-01",
            "sub-id" : "PC-01-PWHISTORY",
            "type" : "error",
            "reason" : "최근 암호 기억이 설정되지 않았습니다"
        })
    elif int(history_count) < 24:
        results.put({
            "id" : "PC-01",
            "sub-id" : "PC-01-PWHISTORY",
            "type" : "error",
            "reason" : "최근 암호 기억이 24일보다 적습니다"
        })

    return results

def check_pc02():
    results = Queue()
    cmd("chcp 65001")
    
    lines = cmd("net accounts").split("\n")
    passwd_length = None
    for line in lines:
        if MINIMUM_PASSWD_LENGTH in line:
            passwd_length = re_split_colon.match(line).group(2)
    
    if passwd_length is None:
        results.put({
            "id" : "PC-02",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "점검에 실패했습니다"
        })

    if int(passwd_length) < 8:
        results.put({
            "id" : "PC-02",
            "sub-id" : "PC-02-PWLEN",
            "type" : "error",
            "reason" : "최소 암호 길이가 8자보다 적습니다"
        })
    
    try:
        check_pc02_sec(results)
    except subprocess.CalledProcessError:
        results.put({
            "id" : "PC-02",
            "sub-id" : "PC-02-PERMISSION-ERROR",
            "type" : "warning",
            "reason" : "세부 정보를 확인할수 없습니다"
        })

    return results

def check_pc02_sec(results:Queue):
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    file = "./.tmp/__policy"

    scmd("chcp 65001")
    scmd(f"secedit /export /CFG {file}")

    with open(file, "r", encoding="UTF-16") as f:
        for line in f.readlines():
            if PASSWD_COMPLEXITY in line:
                if int(re_split_equalsign.match(line).group(2)):
                    pass
                else:
                    results.put({
                        "id" : "PC-02",
                        "sub-id" : "PC-02-PWCOMPLEXITY",
                        "type" : "error",
                        "reason" : "암호 복잡성 정책이 충족하지 않습니다"
                    })
        
    if os.path.isfile(file):
        os.remove(file)

re_share = re.compile(r"^(\w+[$])\s*([\w:\\]+)\s*([^\s]+).*$")
def check_pc03():
    results = Queue()
    cmd("chcp 65001")
    shared = []

    lines = cmd("net share").split("\n")
    for line in lines:
        if m := re_share.match(line):
            shared.append(m.group(1))

    if shared:
        results.put({
            "id" : "PC-03",
            "sub-id" : "PC-03-SHARED",
            "type" : "error",
            "reason" : "공유 폴더가 설정되어 있습니다",
            "addition" : {
                "share" : shared
            }
        }) 
    return results

re_service = re.compile(r"^(Running)\s+([^\s]+)\s*([^\s].+[^\s]).*$")
def check_pc04():
    results = Queue()
    cmd("chcp 65001")
    lines = pw("Get-Service").split("\n")
    services = []
    unused = []

    for line in lines:
        if m := re_service.match(line):
            services.append(m.group(2))
            #print(m.group(2))
    for sv in SERVICES_UNUSED:
        if sv in services:
            unused.append(sv)
    
    if unused:
        results.put({
            "id" : "PC-04",
            "sub-id" : "PC-04-SERVICE-UNNECESSARY",
            "type" : "error",
            "reason" : "불필요한 서비스가 실행중입니다",
            "addition" : {
                "unnecessary" : unused
            }
        }) 
    return results

def check_pc05():
    results = Queue()
    unauth = []

    for directory in UNAUTHORIZED_MASSENGER:
        if os.path.exists(directory):
            unauth.append(directory)
    
    if unauth:
        results.put({
            "id" : "PC-05",
            "sub-id" : "PC-05-SERVICE-UNAUTHORIZE",
            "type" : "error",
            "reason" : "허가되지 않은 상용 메신저가 설치되어 있습니다",
            "addition" : {
                "unnecessary" : unauth
            }
        }) 

    return results

re_volume = re.compile(r"^([A-Z])\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+.*$")
def check_pc16():
    results = Queue()
    cmd("chcp 65001")
    lines = pw("get-volume").split("\n")
    drives = []

    for line in lines:
        if m := re_volume.match(line):
            if m.group(3) == "NTFS":
                drives.append(m.group(1))

    if drives:
        results.put({
            "id" : "PC-16",
            "sub-id" : "PC-16-SERVICE-INVALIDFS",
            "type" : "error",
            "reason" : "드라이브가 NTFS 포맷이 아닙니다",
            "addition" : {
                "unnecessary" : drives
            }
        }) 
    return results

if __name__ == "__main__":
    test_check(check_pc04())
    test_check(check_pc01())
    test_check(check_pc02())
    test_check(check_pc03())
    test_check(check_pc05())
    test_check(check_pc16())

    #"Get-Service"