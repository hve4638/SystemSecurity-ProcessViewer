import os
import winreg
import subprocess

"""
PC-06에 대한 조치 함수
type : link
"""
def solve_06():

    # Run the specified command
    os.system("start ms-settings:windowsupdate")

"""
PC-07에 대한 조치 함수
type : link
"""    
def solve_07():
    # Run the specified command
    os.system("start ms-settings:windowsupdate")    
    
"""
PC-08(한글업데이트)에 대한 조치 함수
type : link
"""
def solve_08_A():
    key_path = r"SOFTWARE\WOW6432Node\HNC\Shared\HncUpdate\HncUtils_2020\HancomStudio"
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
    value, _ = winreg.QueryValueEx(key, "FilePath")

    hancom_studio_path = value
    subprocess.run([hancom_studio_path], check=True)       
