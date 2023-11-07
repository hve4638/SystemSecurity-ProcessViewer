# 브라우저 옵션의 "브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기" 기능이 활성화 되어있는지 점검

import winreg

# registry key path
key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\Cache"
# registry key name
value_name = "Persistent"

try:
    # open registry key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
    # get registry value
    value, regtype = winreg.QueryValueEx(key, value_name)
    winreg.CloseKey(key)
    
    # 0이면 "사용 안 함", 1이면 "사용"
    if value == 0:
        print("양호: '브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기'가 사용으로 설정되어 있습니다.")
    else:
        print("취약: '브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기'가 설정되어 있지 않습니다.")
        
except FileNotFoundError:
    print("레지스트리 키를 찾을 수 없습니다.")
except OSError as e:
    print(f"OS 에러가 발생하였습니다: {e}")

