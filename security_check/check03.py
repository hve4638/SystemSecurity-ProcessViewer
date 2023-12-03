import re
import winreg
import urllib.request
from html.parser import HTMLParser
from datetime import datetime
import subprocess
from queue import Queue
from urllib.request import urlopen

# check_pc06 : HOT FIX 등 최신 보안패치 적용 확인
# check_pc07 : 최신 서비스팩 적용 확인
# check_pc08 : 한글, 어도비 아크로뱃 등의 응용프로그램에 대한 최신 보안패치 적용 확인
# check_pc09 : Windows 보호 업데이트 주기적 업데이트

cand_encoding = ['utf-8', 'cp949', 'latin-1']

def cmd(command):
    for encoding in cand_encoding:
        try:
            return subprocess.check_output(command, shell=True, text=True, encoding=encoding)
        except UnicodeError:
            continue
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError()

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

    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')

    parser = CatalogParser()
    parser.feed(html_content)

    return parser.hotfix_id, parser.date

def get_recent_hotfix_id_pc_06(hotfix_id):
    installed_version = f"Installed Version for {hotfix_id}"  

    powershell_cmd = f'Get-HotFix -Id {hotfix_id} | Select-Object HotFixID,Description,InstalledBy,InstalledOn'
    result = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)

    hotfix_line = result.stdout.strip()

    if hotfix_line:
        match = re.match(r'\s*(KB\d+)\s+(.+)\s+(\S+)\s+(\S+)', hotfix_line)
        if match:
            installed_version = match.group(1)

            latest_version, date_str = get_latest_version_and_date(hotfix_id)

            if latest_version is None or date_str is None:
                return 1

            installed_date = datetime.strptime(date_str, '%m/%d/%Y').date()

            if installed_date < datetime.now().date():
                return 1  # 최신 버전이 아닌 경우 1을 리턴

    return 0  # 최신 버전인 경우 0을 리턴

def get_hotfix():
    command = "wmic qfe get Hotfixid,InstalledOn"

    result = cmd(["cmd.exe", "/c", command])

    hotfix_ids = []
    installed_dates = []

    hotfix_info = result.strip().split('\r\n')

    if len(hotfix_info) <= 1:
        return None

    for info in hotfix_info[1:]:  # Skip the title   
        parts = info.split()

        if len(parts) >= 2:
            hotfix_id, installed_on = parts[0], parts[-1]
            hotfix_ids.append(hotfix_id)
            installed_dates.append(installed_on)

    return hotfix_ids, installed_dates

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

# HOT FIX 등 최신 보안패치 적용
def check_pc06():
    results = Queue()

    hotfix_info = get_hotfix()
    
    if hotfix_info is None:
        results.put({
            "id" : "PC-06",
            "sub-id" : "PC-06-update_.ver",
            "type" : "error",
            "reason" : "보안패치 설치 필요"
        })
        return results
        
    else:
        hotfix_ids, installed_dates = get_hotfix()
        for i, hotfix_id in enumerate(hotfix_ids):
            installed_date_str = installed_dates[i]

            result = get_recent_hotfix_id_pc_06(hotfix_id)

            if result == 1:
                check = 1  # 최신 버전이 아닌 경우 1을 리턴

        check = 0
    if check == 1:
        results.put({
            "id" : "PC-06",
            "sub-id" : "PC-06-update_.ver",
            "type" : "error",
            "reason" : "최신업데이트 설치 필요"
        })
    
    return results

# 최신 서비스팩 적용
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

# 응용프로그램에 대한 최신 패치 적용
def check_pc08():
    results = Queue()
    adb = compare_acrobat_versions()
    hangul = compare_update_version_hangul()
    
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
            "type" : "info",
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
    elif hangul == 2:
        results.put({
            "id" : "PC-08",
            "sub-id" : "PC-08-update_.ver",
            "type" : "info",
            "reason" : "한글이 설치되어있지 않습니다。",
        })
      
        
    return results

# Windows 보호 업데이트 주기적 업데이트
def check_pc09():
    results = Queue()
    powershell_script = '''
    $updateSession = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()

    $searchResult = $updateSearcher.Search("IsInstalled=0")

    if ($searchResult.Updates.Count -gt 0) {
        Write-Output "1"  # 보안 업데이트가 있음
    } else {
        Write-Output "0"  # 보안 업데이트가 없음
    }
    '''

    result = subprocess.run(['powershell', '-Command', powershell_script], capture_output=True, text=True, check=True)

    has_security_updates = int(result.stdout.strip())
    if has_security_updates == 1:
        results.put({
            "id" : "PC-09",
            "sub-id" : "PC-09-security-update",
            "type" : "error",
            "reason" : "보안 업데이트 필요"
        })

    return results

def test_check(results:Queue):
    while not results.empty():
        print(results.get())

if __name__ == "__main__":
    test_check(check_pc06())
    test_check(check_pc07())
    test_check(check_pc08())
    test_check(check_pc09())
