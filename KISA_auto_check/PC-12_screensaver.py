import winreg

#PC-12
def get_CUSERregistry_value(registry_path, value_name):
    try:
        # registry key open
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
        
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

#화면보호기 레지스트리: ScreenSaveActive, ScreenSaverIsSecure, ScreenSaveTimeout
# 각 값들은 REG_SZ: str 이므로 변환 필요


if __name__ == "__main__":
    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaveActive'
    SaveActive_value = int(get_CUSERregistry_value(registry_path, value_name))
    print(f"ScreenSaveActive 값: {SaveActive_value}")

    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaverIsSecure'
    SaverIsSecure_value = int(get_CUSERregistry_value(registry_path, value_name))
    print(f"ScreenSaverIsSecure 값: {SaverIsSecure_value}")

    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaveTimeout'
    SaveTimeout_value = int(get_CUSERregistry_value(registry_path, value_name))
    print(f"ScreenSaveTimeout 값: {SaveTimeout_value}")

    if SaveActive_value is not None: 
        if SaveActive_value == 1:
            print("정상: 화면 보호기가 설정되어 있습니다.")
        elif SaveActive_value == 0:
            print("취약점 발견: 화면 보호기가 설정되어 있지 않습니다.")
        else:
            print("취약점 발견: 예상치 못한 레지스트리 값")
    else:
        print("취약점 발견: SaveActive_value 레지스트리 값을 읽을 수 없습니다.")
    
    if SaverIsSecure_value is not None:
        if SaverIsSecure_value == 1:
            print("정상: 화면 보호기가 암호로 보호받고 있습니다.")
        elif SaverIsSecure_value == 0:
            print("취약점 발견: 화면 보호기가 암호로 보호받고 있지 않습니다.")
        else:
            print("취약점 발견: 예상치 못한 레지스트리 값")
    else:
        print("취약점 발견: SaverIsSecure_value 레지스트리 값을 읽을 수 없습니다.")
    
    if SaveTimeout_value is not None:
        if SaveTimeout_value <= 600:
            print("정상: 화면 보호기 호출에 걸리는 시간이 충분히 짧습니다.")
        elif SaveTimeout_value > 600:
            print("취약점 발견: 화면 보호기 호출에 걸리는 시간이 너무 깁니다.")
        else:
            print("취약점 발견: 예상치 못한 레지스트리 값")
    else:
        print("취약점 발견: SaveTimeout_value 레지스트리 값을 읽을 수 없습니다.")
