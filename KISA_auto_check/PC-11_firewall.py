import winreg

def get_registry_value(registry_path, value_name):
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
registry_path = r'SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile'

# name of specific value
value_name = 'EnableFirewall'

firewall_value = get_registry_value(registry_path, value_name)

print(f"EnableFirewall 값: {firewall_value}")

if firewall_value is not None:
    if firewall_value == 1:
        print("정상")
    elif firewall_value == 0:
        print("취약점 발견")
else:
    print("EnableFirewall 레지스트리 값을 읽을 수 없습니다.")
