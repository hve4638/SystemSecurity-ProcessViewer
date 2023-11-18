from typing import Final
import subprocess, os
import winreg

cand_encoding = [ "EUC-KR", "UTF-16", "UTF-8" ]

def pw(command):
    return cmd(f"powershell {command}")

def cmd(command):
    for encoding in cand_encoding:
        try:
            return subprocess.check_output(command, shell=True, text=True, encoding=encoding)
        except UnicodeError:
            continue
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError()

def scmd(command):
    return subprocess.check_output(command, shell=True, text=True)

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
