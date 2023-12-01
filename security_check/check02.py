import winreg
import re, os
from queue import Queue

def check_registry_key_recursive(root_key, subkey, target_name):
    path_list = []
    try:
        # 현재 폴더의 모든 하위 키를 열고 검사합니다.
        with winreg.OpenKey(root_key, subkey) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                # 각 하위 키에 대해 재귀적으로 검사합니다.
                next_subkey = winreg.EnumKey(key, i)
                next_subkey_path = f"{subkey}\\{next_subkey}"
                if len(check_registry_key_recursive(root_key, next_subkey_path, target_name)) != 0:
                    path_list.extend(check_registry_key_recursive(root_key, next_subkey_path, target_name))

                # 현재 키의 값을 검사합니다.
                try:
                    registry_key = winreg.OpenKey(root_key, next_subkey_path, 0, winreg.KEY_READ)
                    value, _ = winreg.QueryValueEx(registry_key, target_name)
                    winreg.CloseKey(registry_key)
                    path_list.append(next_subkey_path)
                except FileNotFoundError:
                    pass  # 해당 키에 값이 없는 경우 무시합니다.
        return path_list
        
    except FileNotFoundError:
        return path_list
    
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
        return None
    except Exception as e:
        return None

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
        return None
    except Exception as e:
        return None








def get_solve(info):
    results = Queue()
    if info["id"] == "PC-10": # 백신 프로그램의 실시간 감지 
        if info["sub-id"] == "unknown":
            results.put({
                "type" : "link",
            })
            
    elif info["id"] == "PC-11": 
        if info["sub-id"] == "PC-11-NOTFIREWALL":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "unknown":
            results.put({
                "type" : "link",
            })

    elif info["id"] == "PC-12":
        solve_pc12()
        if info["sub-id"] == "PC-12-NOT_SCREENSAVERACTIVE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "PC-12-UNEXPECTED_SCREENSAVERACTIVE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "unknown_SCREENSAVERACTIVE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "PC-12-NOT_SCREENSAVESECURE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "PC-12-UNEXPECTED_SCREENSAVESECURE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "unknown_SCREENSAVESECURE":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "PC-12-TOOLONG_SCREENSAVETIMEOUT":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "PC-12-UNEXPECTED_SCREENSAVETIMEOUT":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "unknown_SCREENSAVETIMEOUT":
            results.put({
                "type" : "link",
            })

    elif info["id"] == "PC-13": 
        solve_pc13()
        if info["sub-id"] == "PC-13-NOTDRIVEDENY":
            results.put({
                "type" : "link",
            })
        elif info["sub-id"] == "unknown":
            results.put({
                "type" : "link",
            })

    elif info["id"] == "PC-19": 
        if info["sub-id"] == "PC-19-NOT_DENYREMOTECONN":
            results.put({
                "type" : "link"
            })
        elif info["sub-id"] == "PC-19-UNEXPECTED_DENYREMOTECONN":
            results.put({
                "type" : "link"
            })
        elif info["sub-id"] == "unknown":
            results.put({
                "type" : "link"
            })
    else: # 알 수 없는 id 값
        pass
    return results

























def test_check(results:Queue):
    while not results.empty():
        # print(results.get())
        get_solve(results.get())
        


"""
PC10에 대한 검사를 수행
"""
def check_pc10():
    results = Queue()

    # window defenders
    registry_path = r'SOFTWARE\Policies\Microsoft\Windows Defender'
    # name of specific value
    value_name = 'DisableRealTimeMonitering'
    wd_vaccine_value = get_LMregistry_value(registry_path, value_name)
    
    # 알약
    # 최상위 폴더 탐색
    registry_path = r'SOFTWARE\ESTsoft'
    # name of specific value
    value_name = 'realtimeMonitorUse'
    al_vaccine_value = get_LMregistry_value(registry_path, value_name)
    # 하위 폴더 탐색
    if al_vaccine_value == None:
        registry_paths = check_registry_key_recursive(winreg.HKEY_LOCAL_MACHINE, registry_path, value_name)
        if len(registry_paths) > 1:
            pass
        elif len(registry_paths) < 1:
            pass
        else:
            registry_path = registry_paths[0]
            # name of specific value
            al_vaccine_value = get_LMregistry_value(registry_path, value_name)

    # v3
    registry_path = r'SOFTWARE\AhnLab\V3Lite4'
    # name of specific value
    value_name = 'sysmonuse'
    v3_vaccine_value = get_LMregistry_value(registry_path, value_name)
    # 하위 폴더 탐색
    if v3_vaccine_value == None:
        registry_paths = check_registry_key_recursive(winreg.HKEY_LOCAL_MACHINE, registry_path, value_name)
        if len(registry_paths) > 1:
            pass
        elif len(registry_paths) < 1:
            pass
        else:
            registry_path = registry_paths[0]
            # name of specific value
            v3_vaccine_value = get_LMregistry_value(registry_path, value_name)
            
    wd_val = 0
    al_val = 0
    v3_val = 0
    if wd_vaccine_value is not None:
        if wd_vaccine_value == 0:
            wd_val = 1
        elif wd_vaccine_value == 1:
            wd_val = 0
        else:
            wd_val = -1
    else:
        wd_val = -1
    if al_vaccine_value is not None:
        if al_vaccine_value == 0:
            al_val = 1
        elif al_vaccine_value == 1:
            al_val = 0
        else:
            al_val = -1
    else:
        al_val = -1
    if v3_vaccine_value is not None:
        if v3_vaccine_value == 0:
            v3_val = 1
        elif v3_vaccine_value == 1:
            v3_val = 0
        else:
            v3_val = -1
    else:
        v3_val = -1

    if wd_val == -1 and al_val == -1 and v3_val == -1:
        results.put({
            "id" : "PC-10",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "백신의 실시간 감시가 감지되지 않습니다."
        })
    return results




"""
PC11에 대한 검사를 수행
"""
def check_pc11():
    results = Queue()

    # path of registry
    registry_path = r'SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile'
    # name of specific value
    value_name = 'EnableFirewall'
    firewall_value = get_LMregistry_value(registry_path, value_name)
    if firewall_value is not None:
        if firewall_value == 1:
            pass
        elif firewall_value == 0:
            results.put({
                "id" : "PC-11",
                "sub-id" : "PC-11-NOTFIREWALL",
                "type" : "error",
                "reason" : "방화벽이 설정되어 있지 않습니다."
            })
    else:
        results.put({
            "id" : "PC-11",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "방화벽 관련 레지스트리가 존재하지 않습니다."
        })
    return results



"""
PC12에 대한 검사를 수행
"""
def check_pc12():
    results = Queue()
    # 화면보호기 레지스트리: ScreenSaveActive, ScreenSaverIsSecure, ScreenSaveTimeout
    # 각 값들은 REG_SZ: str 이므로 변환 필요

    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaveActive'
    SaveActive_value = int(get_CUSERregistry_value(registry_path, value_name))

    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaverIsSecure'
    SaverIsSecure_value = int(get_CUSERregistry_value(registry_path, value_name))

    # path of registry
    registry_path = r'Control Panel\Desktop'
    # name of specific value
    value_name = 'ScreenSaveTimeout'
    SaveTimeout_value = int(get_CUSERregistry_value(registry_path, value_name))

    if SaveActive_value is not None:
        if SaveActive_value == 1:
            pass
        elif SaveActive_value == 0:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-NOT_SCREENSAVERACTIVE",
                "type" : "error",
                "reason" : "화면 보호기가 활성화되어있지 않습니다."
            })
        else:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-UNEXPECTED_SCREENSAVERACTIVE",
                "type" : "error",
                "reason" : "알 수 없는 레지스트리 값이 설정되어 있습니다."
            })
    else:
        results.put({
            "id" : "PC-12",
            "sub-id" : "unknown_SCREENSAVERACTIVE",
            "type" : "error",
            "reason" : "화면 보호기 활성화 관련 레지스트리 값이 존재하지 않습니다."
        })
    if SaverIsSecure_value is not None:
        if SaverIsSecure_value == 1:
            pass
        elif SaverIsSecure_value == 0:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-NOT_SCREENSAVESECURE",
                "type" : "error",
                "reason" : "화면 보호기가 암호로 보호받고 있지 않습니다."
            })
        else:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-UNEXPECTED_SCREENSAVESECURE",
                "type" : "error",
                "reason" : "알 수 없는 레지스트리 값이 설정되어 있습니다."
            })
    else:
        results.put({
                "id" : "PC-12",
                "sub-id" : "unknown_SCREENSAVESECURE",
                "type" : "error",
                "reason" : "화면 보호기 암호 설정 관련 레지스트리 값이 존재하지 않습니다."
        })
    if SaveTimeout_value is not None:
        if SaveTimeout_value <= 600:
            pass
        elif SaveTimeout_value > 600:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-TOOLONG_SCREENSAVETIMEOUT",
                "type" : "error",
                "reason" : "화면 보호기 동작에 걸리는 시간이 너무 깁니다."
            })
        else:
            results.put({
                "id" : "PC-12",
                "sub-id" : "PC-12-UNEXPECTED_SCREENSAVETIMEOUT",
                "type" : "error",
                "reason" : "알 수 없는 레지스트리 값이 설정되어 있습니다."
            })
    else:
        results.put({
            "id" : "PC-12",
            "sub-id" : "unknown_SCREENSAVETIMEOUT",
            "type" : "error",
            "reason" : "화면 보호기 타임아웃 설정 관련 레지스트리 값이 존재하지 않습니다."
        })
    return results



"""
PC13에 대한 검사를 수행
"""
def check_pc13():
    results = Queue()
    # path of registry
    registry_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer'
    # name of specific value
    value_name = 'NoDriveTypeAutoRun'

    AutoRun_value = get_LMregistry_value(registry_path, value_name)

    if AutoRun_value is not None:
        if AutoRun_value == 255:
            pass
        else:
            results.put({
                "id" : "PC-13",
                "sub-id" : "PC-13-NOTDRIVEDENY",
                "type" : "error",
                "reason" : "모든 이동식 미디어에 대한 자동실행 방지가 수행되고 있지 않습니다."
            })
    else:
        results.put({
            "id" : "PC-13",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "관련 레지스트리 값이 존재하지 않습니다."
        })
    return results




"""
PC19에 대한 검사를 수행
"""
def check_pc19():
    results = Queue()
    # path of registry
    registry_path = r'SYSTEM\CurrentControlSet\Control\Remote Assistance'
    # name of specific value
    value_name = 'fAllowToGetHelp'
    Connection_value = get_LMregistry_value(registry_path, value_name)

    if Connection_value is not None:
        if Connection_value == 0:
            pass
        elif Connection_value == 1:
            results.put({
                "id" : "PC-19",
                "sub-id" : "PC-19-NOT_DENYREMOTECONN",
                "type" : "error",
                "reason" : "원격 지원이 차단되어 있지 않습니다."
            })
        else:
            results.put({
                "id" : "PC-19",
                "sub-id" : "PC-19-UNEXPECTED_DENYREMOTECONN",
                "type" : "error",
                "reason" : "알 수 없는 레지스트리 값이 설정되어 있습니다."
            })
    else:
        results.put({
            "id" : "PC-19",
            "sub-id" : "unknown",
            "type" : "error",
            "reason" : "관련 레지스트리 값이 존재하지 않습니다."
        })
    return results



if __name__ == "__main__":
    test_check(check_pc10())
    test_check(check_pc11())
    test_check(check_pc12())
    test_check(check_pc13())
    test_check(check_pc19())
    
