import subprocess
from queue import Queue

def check_pc17():
    results = Queue()
    cmd("chcp 949")
    
    try:
        # 시스템 구성(msconfig) 실행
        subprocess.Popen('msconfig')

        # 실행 결과를 Queue에 추가
        results.put({
            "id": "PC-17",  .
            "sub-id": "PC-17-MSCONFIG",
            "type": "info",
            "reason": "시스템 구성 도구(msconfig)가 실행되었습니다."
        })

    except subprocess.CalledProcessError as e:
        # 실행 중 에러 발생 시
        results.put({
            "id": "PC-17",
            "sub-id": "PC-17-ERROR",
            "type": "error",
            "reason": f"시스템 구성 도구 실행 중 오류 발생: {e}"
        })

    return results
