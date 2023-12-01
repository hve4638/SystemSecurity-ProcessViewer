import hashlib
import random
import time
import queue
import requests
import os
from threading import Thread

my_apikey = "0fda8296874342cb2311f553a9afdb3cf4ac97b021ca6d263695e2f053825112"
url_scan = 'https://www.virustotal.com/vtapi/v2/file/scan'         # # 바이러스토탈 파일 스캔 주소
url_report = 'https://www.virustotal.com/vtapi/v2/file/report'

container = {}
q = queue.Queue()

def get_file_path(filename):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory + "/" + filename)

    if os.path.exists(file_path):
        return file_path
    else:
        return None
    
def maketoken():
    rawid = random.randint(-2147483648, 2147483647) + int(time.time())
    return hashlib.sha256(str(rawid).encode()).hexdigest()

def virustotal_upload(filename:str):
    
    files = get_file_path(filename)
    token = maketoken()
    
    while token in container:
        token = maketoken()                                                     # 토큰 생성 

    container[token] = {"File_Path":files, "status":"ready", "detected":False, "detail":[] }          # 토큰과 결합된 상태정보 생성

    q.put((token, filename))                                                    # q에 token과 filename 결합한 것을 넣음

    return token


def virustotal_progress():
    while True:
        print("progress: enter")
        token, filename = q.get(block=True, timeout=None)  # q가 빌 때까지 token과 filename 가져옴
        print(f"progress: get")
        
        info = container[token]  # token과 결합된 상태 정보
        info["status"] = "progress"  # 상태를 progress로 변경

        try:
            file = get_file_path(filename)
            file_obj = open(file, 'rb')  # 파일 열기
            files = {'file': (file, file_obj)}

            url_scan_params = {'apikey': my_apikey}
            response_scan = requests.post(url_scan, files=files, params=url_scan_params)  # 바이러스토탈 파일 스캔 시작
            result_scan = response_scan.json()
            scan_resource = result_scan['resource']

            url_report_params = {'apikey': my_apikey, 'resource': scan_resource}
            response_report = requests.get(url_report, params=url_report_params)

            report = response_report.json()  # 점검 결과 데이터 추출
            report_scan_result = report.get('scans')
            report_scan_vendors = list(report['scans'].keys())

            num = 0
            
            for vendor in report_scan_vendors:  # 바이러스 스캔 엔진사별 데이터 정리
                outputs = report_scan_result[vendor]                                        #{'detected': False, 'version': '2.0.0.1', 'result': None, 'update': '20231201'}
                outputs_detected = report_scan_result[vendor].get('detected')               #bool 값
                
                
                
                if outputs_detected == True:  # 악성이 감지됐다면 container[token] 상태 변경
                    info["detected"] = True  # 상태를 감지됐다로 변경
                    VENDORNAME = {"Vendor Name": vendor, 'detected': outputs_detected, 'version': outputs.get('version', ''), 'result': outputs.get('result', ''), 'update': outputs.get('update', '')}
                    info["detail"].append(VENDORNAME)
                    
                    
                num = num + 1

            info["status"] = "done"
            file_obj.close()  # 파일 닫기
            time.sleep(20)
        except Exception:
            pass
        finally:
            if info["status"] != "done":
                info["status"] = "error"
                
                file_obj.close()  # 파일 닫기

def virustotal_get_result(token:str, remove_when_done:bool=False)->dict:
     result = container[token]
     if remove_when_done and (result["status"] == "done" or result["status"] == "error"):
        del container[token]
     return result

if __name__ == "__main__":
    progress = Thread(target=virustotal_progress)
    progress.start()
    token = virustotal_upload("example.txt")
    token1 = virustotal_upload("Malicious.hwp")
    token2 = virustotal_upload("Malicious2")
    token3 = virustotal_upload("Malicious1.hwp_")

    
    result = virustotal_get_result(token, remove_when_done=True)
    result1 = virustotal_get_result(token1, remove_when_done=True)
    result2 = virustotal_get_result(token2, remove_when_done=True)
    result3 = virustotal_get_result(token3, remove_when_done=True)
    
    while True:
        print(result)
        print(result1)
        print(result2)
        print(result3) 
        
        match result3["status"]:
            case "error" | "done":
                break
            case _:
                pass
        time.sleep(15)
    time.sleep(15)
    raise Exception()
    pass
    

