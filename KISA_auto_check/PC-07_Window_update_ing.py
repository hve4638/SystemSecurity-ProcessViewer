import urllib.request
from html.parser import HTMLParser
from datetime import datetime
import subprocess


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
            print(f'First row hotfix ID: {self.hotfix_id}, Date: {self.date}')
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

def check_pc06():
    hotfix_ids, installed_dates = get_hotfix()
    for i, hotfix_id in enumerate(hotfix_ids):
        installed_version = f"Installed Version for {hotfix_id}"  # 여기에서 실제 설치된 버전
        installed_date_str = installed_dates[i]
        
        latest_version, date_str = get_latest_version_and_date(hotfix_id)

        if latest_version is None or date_str is None:
            print(f'Hotfix ID: {hotfix_id}를 찾을 수 없습니다.')
            continue

        print(f'{hotfix_id}의 최신 버전은 {latest_version}이며, 업데이트 날짜는 {date_str}입니다.')

        installed_date = datetime.strptime(installed_date_str, '%m/%d/%Y').date()
        update_date = datetime.strptime(date_str, '%m/%d/%Y').date()

        if update_date > installed_date:
            print(f'{hotfix_id}는 최신 버전이 아닙니다. 업데이트가 필요합니다.')
        else:
            print(f'{hotfix_id}는 이미 최신 버전입니다.')

def get_hotfix():
    # Command to check Windows Update status
    command = "wmic qfe get Hotfixid,InstalledOn"

    hotfix_ids = []
    installed_dates = []
    
    # Running the command
    process = subprocess.Popen(["cmd.exe", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()
    #print(result)
    
    if error:
        print("Error retrieving Windows Update status:", error.decode('cp949'))
    else:
        # Decode with 'cp949' to handle Korean characters
        hotfix_info = result.decode('cp949').strip().split('\r\n')

        # If only 'HotFixID' is returned, no updates are installed
        if len(hotfix_info) <= 1:
            print("설치된 업데이트가 없습니다.")
        else:
            for info in hotfix_info[1:]:  # Skip the title   
                parts = info.split()

                # hotfix id와 설치 날짜 얻기
                if len(parts) >= 2:
                    hotfix_id, installed_on = parts[0], parts[-1]
                    hotfix_ids.append(hotfix_id)
                    installed_dates.append(installed_on)
                else:
                    pass
                
    return hotfix_ids, installed_dates

check_pc06()
