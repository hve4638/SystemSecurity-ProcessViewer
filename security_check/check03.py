import re
import winreg
import urllib.request
from html.parser import HTMLParser
from datetime import datetime
import subprocess
from queue import Queue
from urllib.request import urlopen

# check_pc06 : 
# check_pc07 :
# check_pc08 : 

class CatalogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_date = False
        self.hotfix_id = None
        self.date = None
        self.first_row_parsed = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and ('class', 'resultsbottomBorder resultspadding') in attrs:
            self.in_title = True
        elif tag == 'td' and ('class', 'resultsbottomBorder resultspadding ') in attrs:
            self.in_date = True

    def handle_data(self, data):
        if self.in_title:
            # Extracting the hotfix ID from the <a> tag
            self.hotfix_id = data.strip().split(' ')[-1]
        elif self.in_date:
            # Extracting the date from the <td> tag and parsing it to the desired format
            raw_date = data.strip()
            # Use '%m/%d/%Y' format for parsing
            parsed_date = datetime.strptime(raw_date, '%m/%d/%Y').strftime('%m/%d/%Y')
            self.date = parsed_date

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_title = False
            self.in_date = False

        if tag == 'tr' and not self.first_row_parsed:
            # Print or use the parsed data from the first row
            self.first_row_parsed = True

def get_latest_version_and_date(hotfix_id):
    # Microsoft Update Catalog의 URL
    url = f'https://www.catalog.update.microsoft.com/Search.aspx?q={hotfix_id}'

    # 웹 페이지에 요청을 보내고 HTML을 가져옴
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')

    # HTML 파싱
    parser = CatalogParser()
    parser.feed(html_content)

    return parser.hotfix_id, parser.date

def get_recent_hotfix_id_pc_06(hotfix_id):
    installed_version = f"Installed Version for {hotfix_id}"  # 여기에서 실제 설치된 버전

    # PowerShell 명령어 실행
    powershell_cmd = f'Get-HotFix -Id {hotfix_id} | Select-Object HotFixID,Description,InstalledBy,InstalledOn'
    result = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)

    # PowerShell 출력에서 핫픽스 정보 추출
    hotfix_line = result.stdout.strip()

    # 핫픽스 정보가 존재하면 최신 버전인지 확인
    if hotfix_line:
        match = re.match(r'\s*(KB\d+)\s+(.+)\s+(\S+)\s+(\S+)', hotfix_line)
        if match:
            installed_version = match.group(1)
            # 여기에서 최신 버전인지 확인하는 조건을 추가할 수 있습니다.
            # 예를 들어, 최신 버전이라면 "KB" 다음에 오는 숫자가 현재 시스템에

            latest_version, date_str = get_latest_version_and_date(hotfix_id)

            if latest_version is None or date_str is None:
                return 1  # 최신 버전이 아닌 경우 1을 리턴

            installed_date = datetime.strptime(date_str, '%m/%d/%Y').date()

            if installed_date < datetime.now().date():
                return 1  # 최신 버전이 아닌 경우 1을 리턴

    return 0  # 최신 버전인 경우 0을 리턴

def get_hotfix():
    # Command to check Windows Update status
    command = "wmic qfe get Hotfixid,InstalledOn"

    hotfix_ids = []
    installed_dates = []
    
    # Running the command
    process = subprocess.Popen(["cmd.exe", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()
    
    if error:
        print("Error retrieving Windows Update status:", error.decode('cp949'))
    else:
        # Decode with 'cp949' to handle Korean characters
        hotfix_info = result.decode('cp949').strip().split('\r\n')

        # If only 'HotFixID' is returned, no updates are installed
        if len(hotfix_info) <= 1:
            return 1
        else:
            for info in hotfix_info[1:]:  # Skip the title   
                parts = info.split()

                # Check if there are enough parts to extract Hotfix ID and Installed Date
                if len(parts) >= 2:
                    hotfix_id, installed_on = parts[0], parts[-1]
                    hotfix_ids.append(hotfix_id)
                    installed_dates.append(installed_on)
                else:
                    pass
                
    return hotfix_ids, installed_dates

# MS-Office
class CatalogParser_ms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_date = False
        self.hotfix_id = None
        self.date = None
        self.first_row_parsed = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and ('class', 'resultsbottomBorder resultspadding') in attrs:
            self.in_title = True
        elif tag == 'td' and ('class', 'resultsbottomBorder resultspadding ') in attrs:
            self.in_date = True

    def handle_data(self, data):
        if self.in_title:
            self.hotfix_id = data.strip().split(' ')[-1]
        elif self.in_date:
            raw_date = data.strip()
            parsed_date = datetime.strptime(raw_date, '%m/%d/%Y').strftime('%m/%d/%Y')
            self.date = parsed_date

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_title = False
            self.in_date = False

        if tag == 'tr' and not self.first_row_parsed:
            self.first_row_parsed = True

def get_latest_version_and_date_ms(hotfix_id):
    url = f'https://www.catalog.update.microsoft.com/Search.aspx?q={hotfix_id}'
    response = urlopen(url)
    html_content = response.read().decode('utf-8')
    parser = CatalogParser_ms()
    parser.feed(html_content)
    return parser.hotfix_id, parser.date

def is_hotfix_up_to_date(hotfix_id):
    installed_version = f"Installed Version for {hotfix_id}"
    powershell_cmd = f'Get-HotFix -Id {hotfix_id} | Select-Object HotFixID,Description,InstalledBy,InstalledOn'
    result = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)

    hotfix_line = result.stdout.strip()

    if hotfix_line:
        match = re.match(r'\s*(KB\d+)\s+(.+)\s+(\S+)\s+(\S+)', hotfix_line)
        if match:
            installed_version = match.group(1)
            latest_version, date_str = get_latest_version_and_date_ms(hotfix_id)

            if latest_version is None or date_str is None:
                return 1

            installed_date = datetime.strptime(date_str, '%m/%d/%Y').date()

            if installed_date < datetime.now().date():
                return 1

    return 0

def get_hotfix():
    command = 'wmic qfe get Hotfixid,InstalledOn,Description'
    descriptions = []
    hotfix_ids = []
    installed_dates = []

    process = subprocess.Popen(["cmd.exe", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()

    if error:
        print("Error retrieving Windows Update status:", error.decode('cp949'))
    else:
        hotfix_info = result.decode('cp949').strip().split('\r\n')

        if len(hotfix_info) <= 1:
            print("설치된 업데이트가 없습니다.")
        else:
            for info in hotfix_info[1:]:
                parts = info.split()

                if len(parts) >= 2:
                    descriptions = parts[0]
                    if descriptions == 'Security':
                        continue
                    else:
                        hotfix_id, installed_on = parts[-2], parts[-1]
                        hotfix_ids.append(hotfix_id)
                        installed_dates.append(installed_on)
                else:
                    pass

    return hotfix_ids, installed_dates

def compare_update_version_MS():
    try:
        if get_hotfix() == 1:
            return 1
        else:
            hotfix_ids, installed_dates = get_hotfix()
            for i, hotfix_id in enumerate(hotfix_ids):
                installed_date_str = installed_dates[i]

                result = is_hotfix_up_to_date(hotfix_id)

                if result == 1:
                    return 1

            return 0
        
    except ValueError:
        return -1

# 어도비 아크로벳
def get_update_version_with_urllib():
    url = "https://helpx.adobe.com/kr/acrobat/release-note/release-notes-acrobat-reader.html"
    
    try:
        with urlopen(url) as response:
            html = response.read().decode('utf-8')

        # Use regular expression to extract version information
        pattern = r'DC (\d{4}년 \d{1,2}월\(([\d.]+)\))'
        match = re.search(pattern, html)

        if match:
            return match.group(2)
        else:
            return 'Version not found'

    except Exception as e:
        return '1'

def get_acrobat_update_version():
    registry_path = r"SOFTWARE\WOW6432Node\Adobe\Adobe ARM\Products\{291AA914-A987-4CE9-BD63-0C0A92D435E5}"

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        value, reg_type = winreg.QueryValueEx(key, "ProductVersion")
        winreg.CloseKey(key)
        return value

    except FileNotFoundError:
        return -1

def compare_acrobat_versions():
    try:
        if get_acrobat_update_version() == -1:
            return -1
        new_version = get_update_version_with_urllib()
        installed_version = get_acrobat_update_version()

        if installed_version == new_version:
            return 0
        else:
            return 1
    except ValueError:
        return -1


#한글 업데이트 정보 
def get_update_version():
    url = "https://www.hancom.com/main/main.do"
    with urlopen(url) as response:
        html = response.read().decode('utf-8')

    pattern = r'<a href="/cs_center/csDownload\.do" onclick="javascript:ga\(.*\);">.*?(\d{4}-\d{2}-\d{2}).*?</a>'
    match = re.search(pattern, html)

    if match:
        parsed_date = match.group(1)
        parsed_date = parsed_date.replace('-', '')
        return parsed_date
    else:
        return 1

def get_last_update_date():
    key_path = r"SOFTWARE\WOW6432Node\HNC\Shared\HncUpdate"
    value_name = "LastUpdate"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            value, _ = winreg.QueryValueEx(key, value_name)
            return value

    except FileNotFoundError:
        return 1
    except PermissionError:
        return 1
    except Exception as e:
        return 1

def compare_update_version_hangul():
    try:
        newver = int(get_update_version())
        ver = int(get_last_update_date())

        if ver >= newver:
            return 0
        else:
            return 1
    except ValueError:
        return -1

def check_pc06():
    results = Queue()
    if get_hotfix() == 1:
        check = 1
    else:
        hotfix_ids, installed_dates = get_hotfix()
        for i, hotfix_id in enumerate(hotfix_ids):
            installed_date_str = installed_dates[i]

            result = get_recent_hotfix_id_pc_06(hotfix_id)

            if result == 1:
                check = 1  # 최신 버전이 아닌 경우 1을 리턴

        # 모든 핫픽스가 최신이라면 0을 리턴
        check = 0
    if check == 1:
        results.put({
            "id" : "PC-06",
            "sub-id" : "PC-06-update_.ver",
            "type" : "error",
            "reason" : "최신업데이트 설치 필요"
        })
    
    return results

def check_pc07():
    results = Queue()
    hotfix_ids, installed_dates = get_hotfix()
    for i, hotfix_id in enumerate(hotfix_ids):
        installed_version = f"Installed Version for {hotfix_id}"  # 여기에서 실제 설치된 버전
        installed_date_str = installed_dates[i]
        
        latest_version, date_str = get_latest_version_and_date(hotfix_id)

        if latest_version is None or date_str is None:
            continue

        installed_date = datetime.strptime(installed_date_str, '%m/%d/%Y').date()
        update_date = datetime.strptime(date_str, '%m/%d/%Y').date()

        if update_date > installed_date:
            check = 0
        else:
            check = 1
    if check == 1:
        results.put({
            "id" : "PC-07",
            "sub-id" : "PC-07-update_.ver",
            "type" : "error",
            "reason" : "최신업데이트 설치 필요"
        })

    return results

def check_pc08():
    results = Queue()
    adb = compare_acrobat_versions()
    hangul = compare_update_version_hangul()
    ms = compare_update_version_MS()
    
    # Adobe Acrobat 이 최신버전이 아닐경우
    if adb == 1:
        results.put({
            "id" : "PC-08",
            "sub-id" : "PC-08-update_.ver",
            "type" : "error",
            "reason" : "Adobe Acrobat가 최신업데이트가 아닙니다.",
        })
    elif adb == -1:
        results.put({
            "id" : "PC-08",
            "sub-id" : "PC-08-uninstall",
            "type" : "warning",
            "reason" : "Adobe Acrobat가 설치되어있지 않습니다.",
        })
     
           
    # 한글이 최신버전이 아닐경우       
    if hangul == 1:
        results.put({
            "id" : "PC-08",
            "sub-id" : "PC-08-update_.ver",
            "type" : "error",
            "reason" : "한글이 최신업데이트가 아닙니다.",
        })

    if ms == 1:
        results.put({
            "id" : "PC-08",
            "sub-id" : "PC-08-update_.ver",
            "type" : "error",
            "reason" : "MS-Office가 최신업데이트가 아닙니다.",
        })       
        
    return results

def test_check(results:Queue):
    while not results.empty():
        print(results.get())
        # get_solve(results.get())

if __name__ == "__main__":
    test_check(check_pc06())
    test_check(check_pc07())
    test_check(check_pc08())
