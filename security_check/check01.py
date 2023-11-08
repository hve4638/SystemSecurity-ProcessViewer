import re, os
from queue import Queue
from reg import *

MAXIMUM_PASSWD_AGE = "Maximum password age (days):"
MINIMUM_PASSWD_AGE = "Minimum password age (days)"
PASSWD_HISTORY_COUNT = "Length of password history maintained"
MINIMUM_PASSWD_LENGTH = "Minimum password length"
PASSWD_COMPLEXITY = "PasswordComplexity"

r = re.compile(r"^.+[:]\s*([^\s]+).*$")
re_split_colon = re.compile(r"^(.+)\s*[:]\s*([^\s]+).*$")
re_split_equalsign = re.compile(r"^(.+)\s*[=]\s*([^\s]+).*$")

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
    
    check_pc02_sec(results)

    return results

def check_pc02_sec(results):
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    file = "./.tmp/__policy"

    cmd("chcp 65001")
    cmd(f"secedit /export /CFG {file}")

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