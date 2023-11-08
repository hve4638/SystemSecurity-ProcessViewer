#PC-19
import winreg

def get_LMregistry_value(registry_path, value_name):
    try:
        # registry key open
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ)
        
        # read specific vale
        value_data, _ = winreg.QueryValueEx(registry_key, value_name)
        
        # registry key close
        winreg.CloseKey(registry_key)
        
        return value_data

    # Error
    except FileNotFoundError:
        print("The registry key or value does not exist.")
        return None
    except Exception as e:
        print("An error occurred: ", e)
        return None
      
# path of registry
registry_path = r'SYSTEM\CurrentControlSet\Control\Terminal Server'

# name of specific value
value_name = 'fDenyTSConnections'

Connection_value = get_LMregistry_value(registry_path, value_name)
print(f"fDenyTSConnections 값: {Connection_value}")
if Connection_value is not None:
    if Connection_value == 1:
        print("정상: 외부 데스크톱 연결이 차단되어 있습니다.")
    elif Connection_value == 0:
        print("취약점 발견: 외부 데스크톱 연결이 차단되어 있지 않습니다.")
    else:
        print("취약점 발견: 예상치 못한 레지스트리 값")
else:
    print("취약점 발견: fDenyTSConnections 레지스트리 값을 읽을 수 없습니다.")
