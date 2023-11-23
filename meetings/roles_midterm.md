# 인원

- 이한빈
- 조리노
- 염지훈
- 오진섭
- 조준영
- 지전일
- 김호준

# 인원 별 담당 (중간고사 이전)

## 김호준 파트

### 파일정보 표시

```def info_file(filename:str)->dict```

filename 인자로 받은 파일의 정보를 리턴합니다

*입력*

- filename:str - 파일 경로

*출력*

- dict - `FILE_INFO` 포맷의 딕셔너리

---

### 디렉토리 내 파일정보 표시

```def info_directory(directory:str)->Tuple(queue.Queue, dict)```

비동기적으로 작동

directory내 파일 정보를 Queue에 추가합니다

접근이 불가능한 폴더에 접근 등의 예외 처리도 해야 합니다

*입력*

- directory:str - 탐색할 디렉토리

*출력
- queue.Queue
    - 디렉토리 내 파일 정보를 담습니다
    - 내부 원소는 `File_INFO` 포맷의 딕셔너리
    - 모든 탐색이 끝나면 `EOD` 포맷의 딕셔너리를 넣습니다
- dict
    - `ASYNC_INTERRUPT` 포맷의 딕셔너리

---

## 오진섭

### 파일 탐색

```def search_files(directory:str, filters:dict)->Tuple(queue.Queue, dict)```

비동기로 작동

directory 인자를 시작으로 재귀적으로 파일을 탐색해 파일 정보 Queue에 추가합니다

접근이 불가능한 폴더에 접근 등의 예외 처리도 해야 합니다

*입력*

- directory:str,
- filters = 하단 `FILENAME_FILTERS` 참조
  
*출력*

- queue.Queue() 객체
    - 탐색한 파일 결과를 나타냅니다
    - 내부 원소는 `FILE_INFO` 포맷으로 들어갑니다
    - 모든 탐색이 끝나면 `EOD` 포맷의 딕셔너리를 넣습니다
- dict
    - `ASYNC_INTERRUPT` 포맷의 딕셔너리

*note*

`FILE_INFO`에 해당하는 파일 정보를 가져오기 위해 *김호준 파트*의 `info_file()`을 사용해 제작합니다

완성되기 전에는 `info_file()`의 mock함수를 만들어서 사용

---

## 지전일 파트

### 핀 추가

```def add_pin(filename:str)```

filename 파일에 핀(상단고정)을 추가

*입력*

- filename:str

*출력*

- 없음

---

### 핀 제거

```def remove_pin(filename:str)```

filename 파일에 핀을 제거

*입력*

- filename:str

*출력*

- 없음

---

### 핀 확인

```def has_pin(filename:str)->bool```

filename 파일이 핀을 가졌는지 여부를 리턴

*입력*

- filename:str

*출력*

- bool

---

### 디렉토리 내 핀 확인

```def has_pin_in_directory(directory:str)->bool```

directory 폴더 내 핀을 가진 파일이 존재하는 지 여부를 리턴

*입력*

- directory:str

*출력*

- bool

---

### 분석 날짜 확인

```def get_inspect_date(filename:str)->DateTime```

filename 파일의 inspect_date를 확인

*입력*

- filename:str

*출력*

- DateTime

---

### 분석 날짜 추가

```def set_inspect_date(filename:str, date:DateTime)```

filename 파일의 inspect_date를 추가

*입력*

- filename:str
- date:DateTime 분석날짜

---

### 추가 정보

파일명이 바뀌거나 상위 디렉토리 명이 바뀌는 경우는 생각하지 않습니다

특정 경로의 파일을 효율적으로 가져올 수 있어야 합니다

또, 같은 디렉토리 내 파일의 정보를 연속적으로 요청할 가능성이 높으니 상태를 가지는 방식(캐시?)이 좋을 수 있습니다.

## 염지훈 파트

### 확장자 추측

```def guess_ext(filename:str)->list[str]```

filename 인자로 받은 파일의 내부 시그니처를 확인해 가능한 확장자 목록을 리턴합니다

*입력*

- filename:str - 파일 경로

*출력*

- list[str] - 가능한 확장자명을 리스트에 담아 출력


# 딕셔너리 포맷

### FILENAME_FILTERS 포맷

딕셔너리 형태

```python
{
    filename, # 파일명 정규표현식 매치. str 타입
    date_lastchanged, # 마지막 변경날짜. Tuple(DateTime,DateTime) 타입
    date_lastaccess, # 마지막 접근날짜. Tuple(DateTime,DateTime) 타입
    date_create, # 만든 날짜. Tuple(DateTime,DateTime) 타입
    size, # 파일사이즈. byte기준  Tuple(int, int) 타입
}
```

### FILE_INFO 포맷

딕셔너리 형태

```python
{
    path, # 파일 경로 (예시: "c:/windows/system32"). str 타입
    filename, #  전체 파일명 (예시: vscode.exe). str 타입
    ext, # 확장자 (예시: exe). str 타입
    date_lastchanged, # 마지막 변경날짜. DateTime 타입
    date_lastaccess, # 마지막 접근날짜. DateTime 타입
    date_create, # 만든 날짜. DateTime 타입
    addition, # 추가적인 정보를 담은 딕셔너리. 딕셔너리 타입
    eod, # 항상 false. bool 타입
}
```

### EOD

비동기 작업 결과를 저장하는 Queue에서 모든 작업이 끝났음을 알리는 딕셔너리 포맷입니다

```python
{
    eod # 항상 true. bool 타입
}
```

### ASYNC_INTERRUPT 포맷

비동기 작업을 도중에 중단하기 위한 방법

이 방법으로 비동기 작업을 중단시 Queue에 별도로 `EOD`를 추가하지 않고 작업을 종료합니다

```python
{
    interrupt # 초기값은 false, true가 되면 비동기 작업이 중단. bool 타입
}
```

# GUI 파트

`gui` 폴더 내 `readme.md` 참조
