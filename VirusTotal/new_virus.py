import requests, time, os

Status =  /Users/jeonil_ji/Desktop/Virustotal/status/  # status 디렉토리의 경로



def get_file_path(filename):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory + "/filename/", filename)
    if os.path.exists(file_path):
        return file_path
    else:
        return None

def virustotal_upload(filename):
    file_path = get_file_path(filename) 
    if file_path == None:		# get_file_path의 반환값이 None이면 토큰값 반환 x.
	return None


    else:
	run_virustotal(file_path)		# virus total 실행
	
        status_path = Status + os.path.splitext(filename)[0] + '.txt'		#status 디렉토리에 만들 txt파일의 경로 
	if not os.path.exists(status_path):	#status 디렉토리에 filename에 대한 파일이 존재하지 않을경우
            with open(file_path, 'w') as file:		#파일 쓰기 모드로 생성
             
              
            




        return file_path		# 토큰값 반환




	

def virustotal_get_result(token:str)->dict:
    pass

def run_virustotal(file):
    my_apikey = '0fda8296874342cb2311f553a9afdb3cf4ac97b021ca6d263695e2f053825112'
    # 바이러스 의심 파일 설정

    files = {'file': (file, open(file, 'rb'))}

    # 바이러스토탈 파일 스캔 주소
    url_scan = 'https://www.virustotal.com/vtapi/v2/file/scan'
    url_scan_params = {'apikey': my_apikey}

    # 바이러스토탈 파일 스캔 시작
    response_scan = requests.post(url_scan, files=files, params=url_scan_params)
    result_scan = response_scan.json()
    scan_resource = result_scan['resource']

    # URL 스캔 시작 안내
    #print('Virustotal FILE SCAN START (60 Seconds Later) : ', file, '\n')

    # URL 스캔 후 1분 대기 : 결과가 바로 나오지 않기 때문에 1분 정도 대기
    #time.sleep(60)

    # 바이러스토탈 파일 스캔 결과 주소
    url_report = 'https://www.virustotal.com/vtapi/v2/file/report'
    url_report_params = {'apikey': my_apikey, 'resource': scan_resource}

    # 바이러스토탈 파일 스캔 결과 리포트 조회
    response_report = requests.get(url_report, params=url_report_params)

    # 점검 결과 데이터 추출
    report = response_report.json()
    report_scan_date = report.get('scan_date')
    report_scan_sha256 = report.get('sha256')
    report_scan_md5 = report.get('md5')
    report_scan_result = report.get('scans')
    report_scan_vendors = list(report['scans'].keys())
    report_scan_vendors_cnt = len(report_scan_vendors)

    num = 1

    #  점검 완료 메시지
    #print(report.get('verbose_msg'), '\n')
    #time.sleep(1)

    # 파일 스캔 결과 리포트 데이터 보기
    print('Scan Date (UTC) : ', report_scan_date)
    print('Scan File SHA256 : ', report_scan_sha256)
    print('Scan File MD5 : ', report_scan_md5)
    print('Scan File Vendor CNT : ', report_scan_vendors_cnt, '\n')

    #time.sleep(2)

    # 바이러스 스캔 엔진사별 데이터 정리
    for vendor in report_scan_vendors:
        outputs = report_scan_result[vendor]
        outputs_result = report_scan_result[vendor].get('result')
        outputs_version = report_scan_result[vendor].get('version')
        outputs_detected = report_scan_result[vendor].get('detected')
        outputs_update = report_scan_result[vendor].get('update')

        print('No', num,
              'Vendor Name :', vendor,
              ', Vendor Version :', outputs_version,
              ', Scan Detected :', outputs_detected,
              ', Scan Result :', outputs_result)
        num = num + 1
