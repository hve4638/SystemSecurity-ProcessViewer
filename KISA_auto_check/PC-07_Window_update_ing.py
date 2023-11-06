"""
HotFix ID 값들을 얻어내는 것 까지는 성공함.
하지만 해당 값들이 최신인 것을 어떻게 확인할 지 고민중에 있음.
우선 생각하는 방향은 microsoft의 업데이트에 접근하여 최신 HotFix값을 파싱한 후 해당 값을 비교하는 것임.
하지만 해당 방안이 공기관과 같이 추가적 도구를 설치하는 것이 불가능한 환경에서 가능한 것인지는 잘 모르겠음.
"""
import subprocess

def check_windows_update_status():
    # Command to check Windows Update status
    command = "wmic qfe get Hotfixid"

    # Running the command
    process = subprocess.Popen(["cmd.exe", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()

    if error:
        print("Error retrieving Windows Update status:", error.decode('cp949'))
    else:
        # Decode with 'cp949' to handle Korean characters
        updates_installed = result.decode('cp949').strip().split('\r\n')

        # If only 'HotFixID' is returned, no updates are installed
        if len(updates_installed) <= 1:
            print("설치된 업데이트가 없습니다.")
        else:
            print("설치된 업데이트 목록:")
            for update in updates_installed[1:]:  # Skip the title
                print(update)

# Call the function to check Windows Update status
check_windows_update_status()
