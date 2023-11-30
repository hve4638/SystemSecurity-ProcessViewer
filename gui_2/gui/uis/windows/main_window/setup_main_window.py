# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui_2.gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from .functions_main_window import *

import sys
import os

from PySide6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QHBoxLayout, QCheckBox, QTableWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QMovie
from PyQt6.QtCore import QThread, QTimer

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from .qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui_2.gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui_2.gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui_2.gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *

from PyQt6.QtCore import pyqtSignal

# SecurityCheckThread 클래스 정의


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self, front_api):
        self.api = front_api
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon": "icon_file.svg",
            "btn_id": "btn_Kisa",
            "btn_text": "Kisa Check",
            "btn_tooltip": "Kisa Check Open",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_file.svg",
            "btn_id": "btn_Check",
            "btn_text": "Check",
            "btn_tooltip": "Check Open",
            "show_top": True,
            "is_active": True
        },

        {
            "btn_icon" : "icon_info.svg",
            "btn_id" : "btn_info",
            "btn_text" : "Information",
            "btn_tooltip" : "Open informations",
            "show_top" : False,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_settings",
            "btn_text" : "Settings",
            "btn_tooltip" : "Open settings",
            "show_top" : False,
            "is_active" : False
        }
    ]

    # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_search",
            "btn_tooltip" : "Search",
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_top_settings",
            "btn_tooltip" : "Top settings",
            "is_active" : False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # LEFT COLUMN
        # ///////////////////////////////////////////////////////////////

        # BTN 1
        self.left_btn_1 = PyPushButton(
            text="Btn 1",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.left_btn_1.setMaximumHeight(40)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)

        # PAGES
        # ///////////////////////////////////////////////////////////////

        # PAGE 1 - ADD LOGO TO MAIN PAGE
        # 홈 페이지에 버튼 추가
        self.homeButton = QPushButton("KISA Check", self.ui.load_pages.page_1)
        self.homeButton.setMinimumHeight(40) \
            # PyPushButton 스타일 적용
        self.homeButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: 8px;
                color: {self.themes["app_color"]["text_foreground"]};
                background-color: {self.themes["app_color"]["dark_one"]};
            }}
            QPushButton:hover {{
                background-color: {self.themes["app_color"]["dark_three"]};
            }}
            QPushButton:pressed {{
                background-color: {self.themes["app_color"]["dark_four"]};
            }}
        """)


        # 버튼 크기 설정 - 부모 위젯의 너비의 1/4
        parent_width = self.ui.load_pages.page_1.width()
        button_width = parent_width / 2
        button_height = 60  # 버튼의 높이, 필요에 따라 조정
        self.homeButton.setFixedSize(button_width, button_height)

        # QVBoxLayout을 생성합니다.
        layout = QVBoxLayout(self.ui.load_pages.page_1)

        # 레이아웃의 상단에 빈 공간을 추가하여 버튼을 아래로 밀어냅니다.
        layout.addStretch()

        # 버튼을 레이아웃에 추가합니다.
        layout.addWidget(self.homeButton, 0, Qt.AlignHCenter)

        # 페이지에 레이아웃을 설정합니다.
        self.ui.load_pages.page_1.setLayout(layout)
        # 버튼 클릭 이벤트 연결
        self.homeButton.clicked.connect(self.KISAButtonClick)

        # PAGE 2

        # ICON BUTTON 1
        self.icon_button_1 = PyIconButton(
            icon_path = Functions.set_svg_icon("icon_heart.svg"),
            parent = self,
            app_parent = self.ui.central_widget,
            tooltip_text = "Icon button - Heart",
            width = 40,
            height = 40,
            radius = 20,
            dark_one = self.themes["app_color"]["dark_one"],
            icon_color = self.themes["app_color"]["icon_color"],
            icon_color_hover = self.themes["app_color"]["icon_hover"],
            icon_color_pressed = self.themes["app_color"]["icon_active"],
            icon_color_active = self.themes["app_color"]["icon_active"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["pink"]
        )

        # ICON BUTTON 2
        self.icon_button_2 = PyIconButton(
            icon_path = Functions.set_svg_icon("icon_add_user.svg"),
            parent = self,
            app_parent = self.ui.central_widget,
            tooltip_text = "BTN with tooltip",
            width = 40,
            height = 40,
            radius = 8,
            dark_one = self.themes["app_color"]["dark_one"],
            icon_color = self.themes["app_color"]["icon_color"],
            icon_color_hover = self.themes["app_color"]["icon_hover"],
            icon_color_pressed = self.themes["app_color"]["white"],
            icon_color_active = self.themes["app_color"]["icon_active"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["green"],
        )

        # ICON BUTTON 3
        self.icon_button_3 = PyIconButton(
            icon_path = Functions.set_svg_icon("icon_add_user.svg"),
            parent = self,
            app_parent = self.ui.central_widget,
            tooltip_text = "BTN actived! (is_actived = True)",
            width = 40,
            height = 40,
            radius = 8,
            dark_one = self.themes["app_color"]["dark_one"],
            icon_color = self.themes["app_color"]["icon_color"],
            icon_color_hover = self.themes["app_color"]["icon_hover"],
            icon_color_pressed = self.themes["app_color"]["white"],
            icon_color_active = self.themes["app_color"]["icon_active"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["context_color"],
            is_active = True
        )

        # PUSH BUTTON 1
        self.push_button_1 = PyPushButton(
            text = "Button Without Icon",
            radius  =8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.push_button_1.setMinimumHeight(40)

        # PUSH BUTTON 2
        self.push_button_2 = PyPushButton(
            text = "Button With Icon",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.push_button_2.setMinimumHeight(40)
        self.push_button_2.setIcon(self.icon_2)

        # PY LINE EDIT
        self.line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.line_edit.setMinimumHeight(30)

        # TOGGLE BUTTON
        self.toggle_button = PyToggle(
            width = 50,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["context_color"]
        )

        # TABLE WIDGETS
        self.table_widget = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.table_widget.setColumnCount(4)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("점검 사항")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("Pass")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("오류 발생")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("조치")

        # 표 부분
        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)
        self.table_widget.setHorizontalHeaderItem(3, self.column_4)

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setStretchLastSection(False)  # Make sure this is False so that stretch factors work as intended
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        apisc = self.api.SecurityCheck
        checklist = apisc.get_checklist()
        for i, item in enumerate(checklist):
            row_number = self.table_widget.rowCount()
            self.table_widget.insertRow(row_number)
            self.table_widget.setRowHeight(row_number, 22)
            table_item = QTableWidgetItem(str(item["name"]))
            self.table_widget.setItem(i, 0, table_item)
            self.set_test_status(i, "loading")  # 초기 상태를 'loading'으로 설정



            """
            def setup_table_widget(self):
                # 테이블 위젯 설정 코드...

                # 보안 검사 항목을 테이블에 추가
                apisc = self.api.SecurityCheck
                checklist = apisc.get_checklist()
                for i, item in enumerate(checklist):
                    row_number = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_number)  # 행 추가
                    self.table_widget.setRowHeight(row_number, 22)
                    table_item = QTableWidgetItem(str(item["name"]))
                    self.table_widget.setItem(i, 0, table_item)
            """

        """
        # 검사 결과에 따라 오류 메시지와 링크 추가
        for i, item in enumerate(checklist):
            check_result = self.api.SecurityCheck.get_check_result(item["id"])
            self.add_error_item_with_link(i, check_result, "자세히 보기", "http://naver.com")
        """

        # "조치" 열에 버튼 추가
        for row in range(self.table_widget.rowCount()):
            action_button = QPushButton("조치", self)
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
            action_button.clicked.connect(lambda checked=False, row=19, parent=self: parent.action_button_clicked(row))
            self.table_widget.setCellWidget(row, 3, action_button)

            # 체크리스트 항목들을 테이블 위젯에 추가
            for i, item in enumerate(checklist):
                table_item = QTableWidgetItem(str(item["name"]))
                self.table_widget.setItem(i, 0, table_item)

            def action_button_clicked(self, row):
                print(f"조치 버튼이 {row}번 행에서 클릭되었습니다.")




        # Kisa Page 위젯 추가
        self.ui.load_pages.row_5_layout.addWidget(self.table_widget)

        # RIGHT COLUMN
        # ///////////////////////////////////////////////////////////////

        # BTN 1
        self.right_btn_1 = PyPushButton(
            text="Show Menu 2",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.icon_right = QIcon(Functions.set_svg_icon("icon_arrow_right.svg"))
        self.right_btn_1.setIcon(self.icon_right)
        self.right_btn_1.setMaximumHeight(40)
        self.right_btn_1.clicked.connect(lambda: MainFunctions.set_right_column_menu(
            self,
            self.ui.right_column.menu_2
        ))
        self.ui.right_column.btn_1_layout.addWidget(self.right_btn_1)

        # BTN 2
        self.right_btn_2 = PyPushButton(
            text="Show Menu 1",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.icon_left = QIcon(Functions.set_svg_icon("icon_arrow_left.svg"))
        self.right_btn_2.setIcon(self.icon_left)
        self.right_btn_2.setMaximumHeight(40)
        self.right_btn_2.clicked.connect(lambda: MainFunctions.set_right_column_menu(
            self,
            self.ui.right_column.menu_1
        ))
        self.ui.right_column.btn_2_layout.addWidget(self.right_btn_2)

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

