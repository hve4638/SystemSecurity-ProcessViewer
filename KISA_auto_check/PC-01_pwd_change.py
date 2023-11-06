import subprocess
import re

# CMD result capture
cmd_output = subprocess.check_output('net accounts', shell=True, encoding='cp949')

lines = cmd_output.splitlines()

min_password_age = None
max_password_age = None
password_hist_len = None


# Data parshing
for line in lines:
    if "최소 암호 사용 기간" in line:
        min_password_age = int(re.search(r'\d+', line).group())
    elif "최대 암호 사용 기간" in line:
        max_password_age = int(re.search(r'\d+', line).group())
    elif "암호 기억" in line:
        password_hist_len = int(re.search(r'\d+', line).group())

"""
check the value
print(f"Minimum password age: {min_password_age}")
print(f"Maximum password age: {max_password_age}")
print(f"Password history length: {password_hist_len}")
"""

if min_password_age==1:
    print("최소 암호 사용기간 정상")
else:
    print("최소 암호 사용기간 취약")

if max_password_age<90:
    print("최대 암호 사용기간 정상")
else:
    print("최대 암호 사용기간 취약")

if password_hist_len==24:
    print("최근 암호 기억 설정 정상")
else:
    print("최근 암호 기억 설정 취약")    
