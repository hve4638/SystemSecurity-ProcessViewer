import re
import winreg
from urllib.request import urlopen
from html.parser import HTMLParser
from datetime import datetime
import subprocess


# MS-Office
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
            print(f'First row hotfix ID: {self.hotfix_id}, Date: {self.date}')
            self.first_row_parsed = True

def get_latest_version_and_date(hotfix_id):
    url = f'https://www.catalog.update.microsoft.com/Search.aspx?q={hotfix_id}'
    response = urlopen(url)
    html_content = response.read().decode('utf-8')
    parser = CatalogParser()
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
            latest_version, date_str = get_latest_version_and_date(hotfix_id)

            if latest_version is None or date_str is None:
                print(f'Hotfix ID: {hotfix_id}를 찾을 수 없습니다.')
                return 1

            print(f'{hotfix_id}의 최신 버전은 {latest_version}이며, 업데이트 날짜는 {date_str}입니다.')

            installed_date = datetime.strptime(date_str, '%m/%d/%Y').date()

            if installed_date < datetime.now().date():
                print(f'{hotfix_id}는 최신 버전이 아닙니다. 업데이트가 필요합니다.')
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
        print(f"An error occurred: {e}")
        return '1'

def get_acrobat_update_version():
    registry_path = r"SOFTWARE\WOW6432Node\Adobe\Adobe ARM\Products\{291AA914-A987-4CE9-BD63-0C0A92D435E5}"

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        value, reg_type = winreg.QueryValueEx(key, "ProductVersion")
        winreg.CloseKey(key)
        return value

    except FileNotFoundError:
        print("Registry key not found.")
    except PermissionError:
        print("Permission error. Run the script as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

def compare_acrobat_versions():
    try:
        new_version = get_update_version_with_urllib()
        installed_version = get_acrobat_update_version()

        if installed_version == new_version:
            return 0
        else:
            return 1
    except ValueError:
        print("Error: Version value is incorrect.")
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
        print("오류: 날짜 값이 잘못되었습니다.")
        return -1

compare_acrobat_versions()
compare_update_version_hangul()
compare_update_version_MS()
