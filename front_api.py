import os
import time
from queue import Queue
from datetime import datetime
import date_pin
import guess_ext
import file_info
import security_check
import VirusTotal as vt

class FrontAPI:
    initialized = False
    @classmethod
    def initialize(cls):
        if cls.initialized:
            raise Exception("initialize()는 한번만 호출되어야 합니다")
        cls.initialized = True

        vt.virustotal_init()

    class SecurityCheck:
        checkers = {
            "PC-01" : security_check.check_pc01,
            "PC-02" : security_check.check_pc02,
            "PC-03" : security_check.check_pc03,
            "PC-04" : security_check.check_pc04,
            "PC-05" : security_check.check_pc05,
            "PC-06" : security_check.check_pc06,
            #"PC-07" : security_check.check_pc07,
            "PC-08" : security_check.check_pc08,
            "PC-09" : security_check.check_pc09,
            "PC-10" : security_check.check_pc10,
            "PC-11" : security_check.check_pc11,
            "PC-12" : security_check.check_pc12,
            "PC-13" : security_check.check_pc13,
            "PC-15" : security_check.check_pc15,
            "PC-16" : security_check.check_pc16,
            "PC-17" : security_check.check_pc17,
            "PC-18" : security_check.check_pc18,
            "PC-19" : security_check.check_pc19,
        }
        solvers = {
            "PC-02" : security_check.solve_pc02,
            "PC-03" : security_check.solve_pc03,
            "PC-11" : security_check.solve_pc11,
            "PC-12" : security_check.solve_pc12,
            "PC-13" : security_check.solve_pc13,
            "PC-15" : security_check.solve_pc15,
            "PC-16" : security_check.solve_pc16,
            "PC-19" : security_check.solve_pc19,
        }
        linker = {
            "PC-01" : security_check.solve_pc01,
            "PC-04" : security_check.solve_pc04,
            "PC-05" : security_check.solve_pc05,
            "PC-06" : security_check.solve_pc06,
            "PC-07" : security_check.solve_pc07,
            "PC-08" : security_check.solve_pc08,
            "PC-09" : security_check.solve_pc09,
            "PC-10" : security_check.solve_pc10,
        }

        @classmethod
        def check(cls, id:str):
            caller = cls.get_check_caller(id)
            results = caller()

            errors = []
            while not results.empty():
                result = results.get()
                match result['type']:
                    case 'error':
                        errors.append(result)
                    case _:
                        pass
            
            if not errors:
                return {
                    "pass" : True,
                    "detail" : [],
                    "cansolve" : False,
                    "solver" : lambda : None,
                }
            else:
                svtype, solver = cls.get_solve(id)
                details = []
                for error in errors:
                    details.append(error["reason"])
                return {
                    "pass" : False,
                    "detail" : details,
                    "cansolve" : svtype == "solve",
                    "solver" : solver,
                }
            

        @classmethod
        def get_checklist(cls):
            return [
                { "id" : "PC-01", "name" : "패스워드의 주기적 변경" },
                { "id" : "PC-02", "name" : "패스워드 정책 충족" },
                { "id" : "PC-15", "name" : "복구 콘솔에서 자동 로그온 금지" },
                { "id" : "PC-03", "name" : "공유 폴더 제거" },
                { "id" : "PC-04", "name" : "불필요한 서비스 제거" },
                { "id" : "PC-05", "name" : "상용 메신저 사용 금지" },
                { "id" : "PC-16", "name" : "NTFS 파일시스템 설정" },
                { "id" : "PC-17", "name" : "멀티부팅 방지" },
                { "id" : "PC-18", "name" : "브라우저 종료시 임시 인터넷 파일 내용을 삭제하도록 설정" },
                { "id" : "PC-06", "name" : "최신 보안패치 적용" },
                { "id" : "PC-07", "name" : "최신 서비스팩 적용" },
                { "id" : "PC-08", "name" : "응용 프로그램에 대한 최신 보안패치 및 벤더 권고사항 적용" },
                { "id" : "PC-09", "name" : "백신 설치 및 주기적 업데이트" },
                { "id" : "PC-10", "name" : "백신 프로그램에서 제공하는 실시간 감시 기능 활성화" },
                { "id" : "PC-11", "name" : "OS에서 제공하는 침입차단 기능 활성화" },
                { "id" : "PC-12", "name" : "화면보호기 대기 시간 설정 및 재시작 시 암호 보호 설정" },
                { "id" : "PC-13", "name" : "이동식 미디어에 대한 보안대책 수립" },
                # { "id" : "PC-14", "name" : "PC 내부의 미사용 ActiveX 제거" },
                { "id" : "PC-19", "name" : "원격지원 금지 정책" },
            ]
        
        """
        """
        @classmethod
        def get_check_caller(cls, id:str):
            def nocheck():
                q = Queue()
                q.put({
                    "id" : id,
                    "sub-id" : f"{id}-IMPLEMENTATIONERROR",
                    "type": "error",
                    "reason" : "Implementation Error",
                    "addition" : {}})
                return q

            if id in cls.checkers:
                return cls.checkers[id]
            else:
                return nocheck
                
        @classmethod
        def get_solve(cls, id):
            if id in cls.solvers:
                return "solve", cls.solvers[id]
            elif id in cls.linker:
                return "linker", cls.linker[id]
            else:
                return "linker", lambda : None

            def solve():
                for svcall in exportset:
                    svcall()
            def add(id):
                svtype, svcall = cls.__getsolvecaller(id)
                match svtype:
                    case "solve":
                        solveset.add(svcall)
                    case "link":
                        linkset.add(svcall)
                    case "none":
                        pass
            exportset = None
            solveset = set()
            linkset = set()
            
            if type(id_or_errorlog) is str:
                add(id_or_errorlog)
            elif type(id_or_errorlog) is list:
                for log in id_or_errorlog:
                    add(log["sub-id"])
            
            if solveset:
                exportset = solveset
                return "solve", solve
            elif linkset:
                exportset = linkset
                return "link", solve
            else:
                return "none", (lambda : None)
        
        @classmethod
        def __getsolvecaller(cls, id):
            match id:
                case "PC-01-MINPWAGE":
                    return "solve", (lambda : None)
                case "PC-16-SERVICE-INVALIDFS":
                    return "link", (lambda : None)
                case _:
                    return "none", None
    
    class FS:
        @classmethod
        def check_unmatched_ext(cls, fileinfo:dict)->bool:
            guess_ext.guess_ext(fileinfo)
        
        @classmethod
        def get_fileinfo_in_directory(cls, directory:str):
            q = Queue()
            q.put({
                "path" : directory,
                "filename" : "test1.exe",
                "ext" : "exe",
                "date_lastchanged" : datetime(2022,10,2, 12,30,4),
                "date_lastaccess" : datetime(2022,10,2, 14,12,10),
                "date_create" : datetime(2022,10,2, 12,30,4),
                "addition" : {},
                "eod" : False
            })
            q.put({
                "path" : directory,
                "filename" : "test2.txt",
                "ext" : "txt",
                "date_lastchanged" : datetime(2022,10,4, 12,30,4),
                "date_lastaccess" : datetime(2022,10,4, 12,30,4),
                "date_create" : datetime(2022,10,3, 3,3,20),
                "addition" : {},
                "eod" : False
            })
            q.put({
                "eod" : True
            })
            return q
        
        @classmethod
        def get_fileinfo(cls):
            pass

        def search_files(cls, directory:str, filefilters:dict):
            q = Queue()
            q.put({
                "path" : directory,
                "filename" : "searchresult.txt",
                "ext" : "txt",
                "date_lastchanged" : datetime(2022,10,4, 12,30,4),
                "date_lastaccess" : datetime(2022,10,4, 12,30,4),
                "date_create" : datetime(2022,10,3, 3,3,20),
                "addition" : {},
                "eod" : False
            })
            q.put({
                "eod" : True
            })

            return q
    
    class VirusTotal:
        @classmethod
        def mock_upload_files(cls, filenames):
            pass
            def getlog():
                yield "start\n"
                yield ""
                yield ""
                yield ""
                yield f'detected! (file:"example.exe")\n'
                yield ""
                yield ""
                yield f'detected! (file:"example2.exe")\n'
                yield "work done\n"
                yield None

        @classmethod
        def upload_file(cls, filename:str):
            return cls.upload_files([filename])

        @classmethod
        def upload_files(cls, filenames:list[str]):
            tokens = []
            def getlog():
                for filename, token in tokens:
                    while True:
                        result = vt.virustotal_get_result(token, True)
                        match result["status"]:
                            case "error":
                                yield f'error occured (file:"{filename}")\n'
                                break
                            case "done":
                                if result["detected"]:
                                    yield f'detected! (file:"{filename}")\n'
                                    for v in result["detail"]:
                                        try:
                                            if v["detected"]:
                                                vname = result["vendor"]
                                                vver = result["version"]
                                                vresult = result["result"]
                                                yield f'- detected by {vname}({vver}) - {vresult}"\n'
                                        except KeyError as e:
                                            yield f'- error occured : {filename} ({e})"\n'
                                        except Exception as e:
                                            yield f'- Exception occured : {type(e)}, {e}"\n'
                                else:
                                    yield f'normal (file:"{filename}")\n'
                                break
                            case _:
                                yield ""
                                time.sleep(0)
                                continue
                yield "work done\n"
                yield None

            for filename in filenames:
                token = vt.virustotal_upload(filename)
                tokens.append((filename, token))

            return getlog

        @classmethod
        def upload_directory(cls, dirname:str):
            def __get_recursively(directory):
                filenames = []

                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        filenames.append(file_path)

                return filenames
            
            return cls.upload_files(__get_recursively(dirname))


if __name__ == "__main__":
    security_check.solve_pc01()
