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

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'



def queueiter(q:queue.Queue):
    while not q.empty():
        yield q.get()




# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self, front_api):
        super(MainWindow, self).__init__()
        self.api = front_api  # 외부 API 인스턴스

        # UI 초기화
        self.ui = UI_MainWindow(front_api)
        self.ui.setup_ui(self)

        #self.setupSecurityCheck()  # 보안 검사 설정




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

    def perform_security_checks(self):
        apisc = self.api.SecurityCheck
        checklist = apisc.get_checklist()
        self.row_solvers = {}
        all_results_message = ""

        for index, item in enumerate(checklist):
            print(f"Checking {item['name']}... ", end="")

            # apisc.check 메소드를 사용하여 검사 결과를 받아옴
            result = apisc.check(item['id'])
            # 각 행에 대한 solver 함수 저장
            self.row_solvers[index] = result["solver"]

            result_message = f"Checking {item['name']}...\n"
            result_message += f"자세한 문제 : {result['detail']}\n"
            all_results_message += result_message

            # 결과 출력
            print("양호 :", result["pass"])
            print("자세한 문제 :", result["detail"])

            # cansolve 값에 따른 추가 처리
            print("solve or link :", "solve" if result["cansolve"] else "link")
            print("solver 함수 :", result["solver"])
            print("")

            # cansolve 값에 따라 조치 버튼 업데이트
            self.update_action_buttons(index, result["cansolve"], result["solver"])

            # 결과에 따른 상태 업데이트
            if result["pass"]:
                print(f"{item['name']} Passed")
                self.set_test_status(index, "success")
                # 정상 상태 메시지 추가
                self.add_normal_item_with_link(index)

            else:
                print(f"{item['name']} Failed")
                for detail in result["detail"]:
                    print(f"- {detail}")
                self.set_test_status(index, "failure")
                # 오류 메시지와 링크를 테이블에 추가
                self.add_error_item_with_button(index, '\n'.join(result["detail"]))
        self.show_message("보안 검사 전체 결과", all_results_message)

    def show_message(self, title, message):
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle(title)
        self.msg_box.move(2000, 380)
        self.msg_box.setText("")
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.msg_box.setStyleSheet("""
                  QMessageBox {
                      background-color: #2C313C;
                  }
                  QLabel {
                      font-size: 12px; 
                      color: white;
                  }
              """)


        self.lines = message.split('\n')
        self.current_line = 0
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # 0.1초 간격
        self.timer.timeout.connect(self.updateMessageBox)
        self.timer.start()

        self.msg_box.exec()

    def updateMessageBox(self):
        if self.current_line < len(self.lines):
            existing_text = self.msg_box.text()
            new_text = existing_text + self.lines[self.current_line] + '\n'
            self.msg_box.setText(new_text)
            self.current_line += 1
        else:
            self.timer.stop()
            self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg_box.accept()





    def update_action_buttons(self, row, cansolve, solver):
        # cansolve 값에 따라 버튼 텍스트 결정
        button_text = "자동 조치" if cansolve else "수동 조치"
        action_button = QPushButton(button_text, self)
        # 스타일 설정
        action_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF; /* 텍스트 색상 */
                background-color: #5A5A5A; /* 배경색 */
                border-radius: 10px; /* 테두리 둥근 정도 */
                padding: 5px; /* 안쪽 여백 */
                border: none; /* 테두리 없음 */
            }
            QPushButton:hover {
                background-color: #6E6E6E; /* 마우스 오버 시 배경색 */
            }
            QPushButton:pressed {
                background-color: #484848; /* 클릭 시 배경색 */
            }
        """)


        # 람다 함수를 사용하여 클릭 이벤트 연결
        action_button.clicked.connect(lambda: self.action_button_clicked(row, cansolve, solver))
        self.table_widget.setCellWidget(row, 3, action_button)

    def action_button_clicked(self, row, cansolve, solver):
        if cansolve:
            print(f"{row}번 행에서 자동 조치 버튼이 클릭되었습니다.")
            solver()
            # 자동 조치 처리 로직
        else:
            print(f"{row}번 행에서 수동 조치 버튼이 클릭되었습니다.")
            # 수동 조치 처리 로직



    def add_normal_item_with_link(self, row):
        # QLabel 생성 및 설정
        normal_text = "정상"

        label = QLabel(normal_text)
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

    def add_error_item_with_button(self, row, detail_text):
        # 오류 발생 텍스트와 버튼을 위한 위젯 생성
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 오류 발생 텍스트 라벨 생성
        error_label = QLabel("오류 발생")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spacer = QSpacerItem(75, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addSpacerItem(spacer)
        layout.addWidget(error_label)

        # 자세히 보기 버튼 생성
        detail_button = QPushButton("자세히 보기")
        detail_button.setFixedSize(70, 20)  # 버튼 크기 설정
        detail_button.clicked.connect(lambda: self.show_detail_message(detail_text))

        layout.addWidget(detail_button)  # 버튼을 레이아웃에 추가
        layout.setContentsMargins(5, 5, 5, 5)
        widget.setLayout(layout)

        detail_button.setStyleSheet("""
                            QPushButton {
                                color: #FFFFFF; /* 텍스트 색상 */
                                background-color: #5A5A5A; /* 배경색 */
                                border-radius: 10px; /* 테두리 둥근 정도 */
                                padding: 5px; /* 안쪽 여백 */
                                border: none; /* 테두리 없음 */
                            }
                            QPushButton:hover {
                                background-color: #6E6E6E; /* 마우스 오버 시 배경색 */
                            }
                            QPushButton:pressed {
                                background-color: #484848; /* 클릭 시 배경색 */
                            }
                        """)
        detail_button.clicked.connect(lambda: self.show_detail_message(detail_text))

        # 테이블 위젯에 위젯 추가
        self.table_widget.setCellWidget(row, 2, widget)

    def add_detail_button(self, row, detail_text):
        btn = QPushButton("자세히 보기")
        btn.setStyleSheet("""
                    QPushButton {
                        color: #FFFFFF; /* 텍스트 색상 */
                        background-color: #5A5A5A; /* 배경색 */
                        border-radius: 10px; /* 테두리 둥근 정도 */
                        padding: 5px; /* 안쪽 여백 */
                        border: none; /* 테두리 없음 */
                    }
                    QPushButton:hover {
                        background-color: #6E6E6E; /* 마우스 오버 시 배경색 */
                    }
                    QPushButton:pressed {
                        background-color: #484848; /* 클릭 시 배경색 */
                    }
                """)
        btn.clicked.connect(lambda: self.show_detail_message(detail_text))
        self.table_widget.setCellWidget(row, 2, btn)

    def show_detail_message(self, detail_text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("자세히 보기")
        msg_box.setText(detail_text)
        msg_box.exec()

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

        # 검사 시작
        self.perform_security_checks()

        # 검사 종료 메시지 표시
        self.show_status_message("모든 보안 검사가 완료되었습니다.")

        # 페이지 2로 전환
        MainFunctions.set_page(self, self.ui.load_pages.page_2)

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

