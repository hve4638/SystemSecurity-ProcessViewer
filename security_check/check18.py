import winreg
from queue import Queue

def check_pc18():
    results = Queue()

    # registry key path and name
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\Cache"
    value_name = "Persistent"

    try:
        # open registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        # get registry value
        value, regtype = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)

        # 0이면 "사용 안 함", 1이면 "사용"
        if value == 0:
            results.put({
                "id": "PC-18",
                "sub-id": "PC-18-CACHE",
                "type": "info",
                "reason": "'브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기'가 사용으로 설정되어 있습니다."
            })
        else:
            results.put({
                "id": "PC-18",
                "sub-id": "PC-18-NO-CACHE",
                "type": "warning",
                "reason": "'브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기'가 설정되어 있지 않습니다."
            })

    except FileNotFoundError:
        results.put({
            "id": "PC-18",
            "sub-id": "PC-18-NOT-FOUND",
            "type": "error",
            "reason": "레지스트리 키를 찾을 수 없습니다."
        })
    except OSError as e:
        results.put({
            "id": "PC-18",
            "sub-id": "PC-18-OS-ERROR",
            "type": "error",
            "reason": f"OS 에러가 발생하였습니다: {e}"
        })

    return results
