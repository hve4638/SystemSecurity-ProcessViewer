import re
import queue

def queueiter(q:queue.Queue):
    while not q.empty():
        yield q.get()

def input_match(prompt:str, pattern:str):
    p = re.compile(pattern)
    while True:
        value = input(prompt)
        if p.match(value):
            return value

class RunAsCLI:
    def __init__(self, front_api):
        self.api = front_api

    def security_check_new(self):
        apisc = self.api.SecurityCheck
        checklist = apisc.get_checklist()

        for c in checklist:
            print(f"[{c['id']}] {c['name']}")
        
        input("press enter")
        for c in checklist:
            print(f"Check {c['id']}")
            result = apisc.check(c['id'])

            print("양호 :", result["pass"])
            print("자세한 문제 :", result["detail"])

            cs = "solve" if result["cansolve"] else "link"
            print("solve or link :", cs)
            print("solver 함수 :", result["solver"])
            print("")
            print("")
            
        


    def security_check(self):
        apisc = self.api.SecurityCheck

        checklist = apisc.get_checklist()

        for c in checklist:
            print(f"[{c['id']}] {c['name']}")
        
        print("")
        print("do security-check? ", end="")
        answer = input_match("[Y/N] ", "[yYnN]")
        match answer:
            case "y" | "Y":
                for c in checklist:
                    print(f"{c['name']}... ", end="")

                    check = apisc.get_check_caller(c["id"])
                    result = check()

                    errorlog = []
                    warninglog = []
                    infolog = []
                    for log in queueiter(result):
                        match log['type']:
                            case 'error':
                                errorlog.append(log)
                            case 'warning':
                                warninglog.append(log)
                            case 'info':
                                infolog.append(log)

                    if errorlog:
                        svtype, svcall = apisc.get_solve(errorlog)
                        print(f"Fail  [{svtype}]")

                        
                        for log in errorlog:
                            print(f"    - {log['reason']}")
                    else:
                        print("Pass")
                    
            case _:
                pass


    def main(self):
        while True:
            print("", end="\n"*3)
            print("Run as CLI", end="\n"*2)
            print("[1] Security Check")
            print("[2] Security Check (NEW)")
            print("[3] Exit")
            value = input_match("> ", r"[1-3]")
            match value:
                case "1":
                    try:
                        self.security_check()
                    except Exception as e:
                        print("Exception Occur!")
                        print(e)
                        raise
                case "2":
                    #print("explorer")
                    self.security_check_new()
                case "3":
                    break

        return 0


    pass