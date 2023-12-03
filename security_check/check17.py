import subprocess
import queue

def check_pc17():
    results = Queue()
    cmd("chcp 949")
    
    # 부팅 구성 데이터 가져오기
    try:
        process = subprocess.Popen(["cmd.exe", "/c", "bcdedit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()

        # 에러 확인
        if error:
            raise subprocess.CalledProcessError(1, "bcdedit", error)

        # 멀티 부팅 구성 확인
        boot_loaders = result.decode('cp949').count("Windows Boot Loader")
        if boot_loaders > 1:
            results.put({
                "id": "PC-17",
                "sub-id": "PC-17-MBOOT",
                "type": "warning",
                "reason": "멀티 부팅 구성이 감지되었습니다."
            })
        else:
            results.put({
                "id": "PC-17",
                "sub-id": "PC-17-NO-MBOOT",
                "type": "info",
                "reason": "멀티 부팅 구성이 감지되지 않았습니다."
            })

    except subprocess.CalledProcessError as e:
        # 에러 처리
        results.put({
            "id": "PC-17",
            "sub-id": "PC-17-ERROR",
            "type": "error",
            "reason": "부팅 구성 데이터를 가져오는데 에러가 발생했습니다.",
            "addition": {"error_detail": str(e)}
        })

    return results
