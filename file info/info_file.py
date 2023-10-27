import os
import asyncio
import queue
from typing import Tuple, Dict

# 파일 정보 포맷
File_INFO = {
    "path": str,                 # 파일 경로 (예시: "c:/windows/system32")
    "filename": str,             # 전체 파일명 (예시: vscode.exe)
    "ext": str,                  # 확장자 (예시: exe)
    "date_lastchanged": str,     # 마지막 변경날짜. DateTime 타입 (예시: "2023-10-23 10:30:00")
    "date_lastaccess": str,      # 마지막 접근날짜. DateTime 타입 (예시: "2023-10-23 10:30:00")
    "date_create": str,          # 만든 날짜. DateTime 타입 (예시: "2023-10-23 10:30:00")
    "addition": dict,            # 추가적인 정보를 담은 딕셔너리 (선택 사항)
    "eod": False                 # 항상 false
}

EOD = {
    "eod": True # 항상 true. bool 타입
}

def info_file(filename: str) -> Dict:
    file_info = {}
    
    # 파일 존재 유무 확인
    if not os.path.exists(filename):
        file_info['error'] = 'File not found'
        return file_info

    # 파일 경로
    file_info['path'] = filename
    
    # 전체 파일명
    file_info['filename'] = os.path.basename(filename)

    # 확장자
    file_info['ext'] = os.path.splitext(filename)[1]

    # 마지막 변경 시간
    file_info['date_lastchanged'] = str(os.path.getmtime(filename))

    # 마지막 접근 시간
    file_info['date_lastaccess'] = str(os.path.getatime(filename))

    # 만든 시간
    file_info['date_create'] = str(os.path.getctime(filename))
    
    return file_info
