# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from .gui.uis.windows.main_window.functions_main_window import *
import sys
import os
from queue import Queue
import queue

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from .qt_core import *
# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from .gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from .gui.uis.windows.main_window import *

from PyQt6.QtCore import pyqtSignal

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////
from front_api import FrontAPI

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# SecurityCheckThread 클래스 정의
"""
class SecurityCheckThread(QThread):
    def __init__(self, check_functions, parent=None):
        super().__init__(parent)  # 부모 클래스(QThread)의 초기화
        self.check_functions = check_functions  # 검사 함수 리스트 저장
    def run(self):
        print("보안 검사 시작...")
        for index, check_function in enumerate(self.check_functions):
            try:
                check_result = check_function()
                self.result_queue.put(check_result)

                # 여기서 검사 결과에 따라 상태 설정
                if ...:  # 성공 조건
                    self.signal_update_status(index, "success")
                elif ...:  # 실패 조건
                    self.signal_update_status(index, "failure")
                else:  # 로딩 또는 기타 상태
                    self.signal_update_status(index, "loading")

            except Exception as e:
                print(f"보안 검사 중 예외 발생: {e}")
        print("보안 검사 완료.")

    signal_update_status = pyqtSignal(int, str)  # 상태 업데이트 시그널
"""

def queueiter(q:queue.Queue):
    while not q.empty():
        yield q.get()

"""
class SecurityCheckThread(QThread):
    # 결과 업데이트 시그널 정의
    signal_update_error_link = pyqtSignal(int, object)
    def __init__(self, check_functions, parent=None):
        super().__init__(parent)
        self.check_functions = check_functions
        self.result_queue = Queue()

    def run(self):
        for index, check_function in enumerate(self.check_functions):
            try:
                check_result = check_function()
                self.result_queue.put(check_result)

                # 각 검사 결과에 따라 상태를 설정
                has_error = False
                for log in queueiter(check_result):
                    if log['type'] == 'error':
                        has_error = True
                        break

                # 상태 업데이트 신호 발생
                if has_error:
                    self.signal_update_status.emit(index, "failure")
                else:
                    self.signal_update_status.emit(index, "success")

            except Exception as e:
                print(f"Exception: {e}")
                self.signal_update_status.emit(index, "failure")

            # 메인 윈도우의 메서드 호출
            result = self.result_queue.get()
            if isinstance(self.parent(), MainWindow):
                self.parent().update_error_link(index, result)
"""

class SecurityCheckThread(QThread):
    # 결과 업데이트 시그널 정의
    signal_update_error_link = pyqtSignal(int, object)

    def __init__(self, check_functions, parent=None):
        super().__init__(parent)
        self.check_functions = check_functions
        self.result_queue = Queue()

    def run(self):
        for index, check_function in enumerate(self.check_functions):
            try:
                check_result = check_function()
                self.result_queue.put(check_result)
                self.signal_update_error_link.emit(index, check_result)
            except Exception as e:
                print(f"Exception: {e}")
                self.signal_update_error_link.emit(index, None)

def security_check(api):
    apisc = api.SecurityCheck
    checklist = apisc.get_checklist()

    check_functions = [apisc.get_check_caller(c["id"]) for c in checklist]

    # SecurityCheckThread 시작
    check_thread = SecurityCheckThread(check_functions)
    check_thread.start()

    # 검사 결과를 실시간으로 콘솔에 출력
    for c in checklist:
        print(f"[{c['id']}] {c['name']}... ", end="")
        check_thread.join()  # 각 검사가 완료될 때까지 대기

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self, front_api):
        super().__init__()
        self.api = front_api
        #self.setupUi()
        #self.setupThreads()


        # 나머지 코드...
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # 보안 검사 함수들을 리스트로 생성
        checklist = self.api.SecurityCheck.get_checklist()
        check_functions = [self.api.SecurityCheck.get_check_caller(item["id"]) for item in checklist]

        # SecurityCheckThread 인스턴스 생성 및 시그널 연결
        self.check_thread = SecurityCheckThread(check_functions)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)
        # Open Page 2
        if btn.objectName() == "btn_Kisa":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)
        # Open Page3
        if btn.objectName() == "btn_Check":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)

                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    def action_button_clicked(self, row):
        print(f"{row}번 행에서 조치 버튼이 클릭되었습니다.")
        # 해당 행에 대한 조치를 취하는 코드를 추가


    def set_test_status(self, row, status):
        label = QLabel(self)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if status == "loading":
            movie = QMovie(os.path.join(current_dir, "gui/images/svg_images/loading.gif"))
            movie.setScaledSize(QSize(24, 24))  # GIF의 크기를 조절
            label.setMovie(movie)
            movie.start()
        elif status == "success":
            label.setPixmap(QPixmap(os.path.join(current_dir, "gui/images/svg_images/check_mark.svg")).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
        elif status == "failure":
            label.setPixmap(QPixmap(os.path.join(current_dir, "gui/images/svg_images/cross_mark.svg")).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_widget.setCellWidget(row, 1, label)

    """
    def perform_security_checks(self):
        checklist = self.api.SecurityCheck.get_checklist()
        for index, item in enumerate(checklist):
            check_function = self.api.SecurityCheck.get_check_caller(item["id"])
            check_thread = SecurityCheckThread(check_function)
            check_thread.start()
            self.set_test_status(index, "loading")
            QTimer.singleShot(1000, lambda: self.update_check_status(index, check_thread))
    """

    def perform_security_checks(self):
        checklist = self.api.SecurityCheck.get_checklist()
        check_functions = [self.api.SecurityCheck.get_check_caller(item["id"]) for item in checklist]
        check_thread = SecurityCheckThread(check_functions)
        check_thread.start()

    # 보안 검사 결과 업데이트
    def update_check_status(self, index, check_thread):
        if not check_thread.result_queue.empty():
            result = check_thread.result_queue.get()
            # 결과에 따라 상태 업데이트
            if result.get("type") == "error":
                self.set_test_status(index, "failure")
            else:
                self.set_test_status(index, "success")
        else:
            QTimer.singleShot(1000, lambda: self.update_check_status(index, check_thread))

    def update_table_row(self, row_index, result):
        # 테이블의 row_index에 있는 행을 result에 따라 업데이트하는 코드
        pass

    def add_error_item_with_link(self, row, result, link_text, link_url):
        # QLabel 생성 및 설정
        if result.get("type") == "error":
            error_text = f"오류 발생 <a href='{link_url}' style='text-decoration:none; color:blue;'><span style='text-decoration: underline;'>{link_text}</span></a>"
        else:
            error_text = "정상"

        label = QLabel(error_text)
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # QLabel 텍스트 가운데 정렬
        label.setMinimumSize(200, 20)  # QLabel의 최소 크기 설정

        # QLabel을 QWidget에 넣고 가운데 정렬
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)  # 마진 설정을 0으로 변경
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(layout)

        # 테이블 위젯에 위젯 추가
        self.table_widget.setCellWidget(row, 2, widget)

    """
    def setupThreads(self):
        checklist = self.api.SecurityCheck.get_checklist()
        check_functions = [self.api.SecurityCheck.get_check_caller(item["id"]) for item in checklist]
        self.check_thread = SecurityCheckThread(check_functions)
        self.check_thread.signal_update_error_link.connect(self.update_error_link)
        self.check_thread.start()
    """

    def update_error_link(self, index, result):
        if result is not None:
            # 결과에 따른 UI 업데이트
            if any(log['type'] == 'error' for log in result):
                self.set_test_status(index, "failure")
            else:
                self.set_test_status(index, "success")
        else:
            self.set_test_status(index, "failure")

    def update_error_link_in_table(self, index, result):
        # result는 검사 결과 데이터
        # 여기서 오류가 있는지 확인하고 add_error_item_with_link 함수를 호출
        if result.get("type") == "error":
            # 오류 메시지와 링크 추가
            self.setup_main_window.add_error_item_with_link(index, True, "자세히 보기", "http://naver.com")
        else:
            # 정상 상태 메시지 추가
            self.setup_main_window.add_error_item_with_link(index, False, "정상", "#")

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    # 버튼 클릭 이벤트 핸들러
    def KISAButtonClick(self):

        # 검사 시작 메시지 표시
        self.show_status_message("보안 검사 시작 중...")

        # 페이지 2로 전환
        MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # 검사 시작
        self.perform_security_checks()


        # 검사 종료 메시지 표시
        self.show_status_message("모든 보안 검사가 완료되었습니다.")

    def show_status_message(self, message):
        # 콘솔에 메시지를 출력합니다.
        print(message)

    def show_additional_actions(self):
        # 추가 조치 사항을 표시하는 코드
        pass


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
def GUimain(front_api):
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow(front_api)

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())


