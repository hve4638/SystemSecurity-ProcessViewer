# VirusTotal

## 파일 업로드 (virustotal_upload)

```python
def virustotal_upload(filename:str)->str:
    pass
```

*인자*

- `filename` : 업로드할 파일의 경로입니다

*리턴*

이후 결과를 확인하기 위한 문자열로 된 토큰를 리턴합니다

토큰 생성에 대한 예시 코드는 맨 아래를 참고하세요

*추가 정보*

실제 이 함수 내에서 실행되어야 하는 것은 `해당 검사에 대한 토큰 생성`, `해당 토큰에 대응되는 상태 정보 딕셔너리 추가`, `비동기로 수행되는 __virustotal_progress() 호출` 입니다

`상태 정보` 딕셔너리의 포맷에 대해선 아래를 참고하세요

이 함수가 호출되면 즉시 토큰을 리턴하며 실제 검사 작업은 `__virustotal_progress()`에서 수행됩니다. 또, 받은 토큰을 이용해 `virustotal_get_result()`에서 현재 검사 진행 상태를 확인할 수 있어야 합니다

## 파일 결과 확인 (virustotal_get_result)

```python
def virustotal_get_result(token:str)->dict:
    pass
```

*인자*

- `token` : `virustotal_upload`에서 가져온 토큰을 인자로 넣습니다

*리턴*

해당 토큰에 대응되는 상태 정보를 딕셔너리 형태로 리턴합니다

상태 정보 포맷에 대해선 아래를 참고하세요

### 상태 정보 포맷

`virustotal_get_result()`가 리턴하는 딕셔너리의 필드는 다음과 같습니다

```python
{
    "status" : "", 
    "detected" : True,
    "detail" : [], 
}
```

- `status` : 문자열 입니다. 현재 해당 파일의 검사 상태를 나타냅니다. `ready`, `progress`, `done`, `error` 로 나뉘어집니다
    - `ready` : 해당 검사가 아직 진행되지 않은 상태. 구현에 따라 이 상태 없이 바로 `progress`로 넘어갈 수 있습니다
    - `progress` : 검사가 진행 중임을 나타냅니다
    - `done` : 검사가 끝나고 "detected", "detail"에 정보가 추가되어있음을 나타냅니다
    - `error` : 검사가 실패했음을 나타냅니다
- `detected` : bool 자료형입니다. 검사 결과 해당 파일이 악성 파일인지 유무를 나타냅니다. 악성이라면 True, 아니라면 False입니다
- `detail` : 리스트 자료형입니다. 새부 정보를 담습니다
    - 리스트 내 딕셔너리 형태로 정보를 추가하며, VendorName, VerdorVersion, ScanDetected 등의 정보를 담습니다


## 바이러스 토탈 작업 수행 (__virustotal_progress)

```python
def __virustotal_progress(...):
    pass
```

모듈 내부적으로 사용되는 함수로 꼭 해당 이름일 필요는 없으며 인자 및 리턴의 정해진 형식은 없습니다

`virustotal_upload`에서 비동기로 호출되며 검사 진행과 검사 진행에 따른 `상태 정보` 딕셔너리의 status값을 변화시킵니다

`try-finally` 를 이용해 예기치 못한 상황에도 status값이 제대로 업데이트 될 수 있도록 해야합니다

```python
info = {"status":"ready"} # virustotal_get_result로 리턴하는 상태 정보 딕셔너리라 가정

try:
    # 검사 수행전 status를 progress로 변경
    info["status"] = "progress"

    # 검사를 수행하는 코드가 있는 부분

    # 모든 검사가 정상적으로 끝났다면 status를 done으로 변경
    info["status"] = "done"
finally:
    # 만약 에러 등으로 status가 done이 아닌 상태로 함수가 종료된다면, error로 변경
    if info["status"] != "done":
        info["status"] = "error"
```

## 랜덤 문자열(토큰) 생성 예시

```python
import hashlib
import random
import time

def makeid():
    rawid = random.randint(-2147483648, 2147483647) + int(time.time())
    return hashlib.sha256(str(rawid).encode()).hexdigest()
```

해당 코드 사용시 혹시나있을 해시 충돌을 한번 체크 후 사용해야 합니다 (토큰 생성후 이미 동일한 토큰이 저장되어있다면 새로 토큰 생성)