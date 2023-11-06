#본 문서는 멀티 부팅 구성 감지까지만 작성하였음.
#후에 OS를 삭제하는 부분은 각별한 주의가 필요하기 때문에 구현하지 않았음을 알림. 
#창을 열어주는 것까지만 구현하는 것을 제안함.

import subprocess

def check_multi_boot():
    # Command to get boot configuration data
    command = "bcdedit"

    # Running the command
    process = subprocess.Popen(["cmd.exe", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()

    # Handle potential errors
    if error:
        print("Error retrieving boot configuration:", error.decode('cp949'))
    else:
        # Decode with 'cp949' to handle Korean characters
        bcd_output = result.decode('cp949')

        # Count how many Windows Boot Loaders are present
        boot_loaders = bcd_output.count("Windows Boot Loader")

        if boot_loaders > 1:
            print("취약점 존재: 멀티 부팅 구성이 감지되었습니다.")
            #open "시스템구성" tap
            subprocess.Popen(["msconfig"])
        else:
            print("정상: 멀티 부팅 구성이 감지되지 않았습니다.")
            
# Call the function to check for multi-boot configuration
check_multi_boot()
