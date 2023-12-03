# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from .qt_core import *
from qt_core import QFileSystemModel, QTreeView, QVBoxLayout
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox


class Ui_MainPages:
    def __init__(self, front_api):
        self.api = front_api
        super().__init__()

    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 16pt")



        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")

        self.pages.addWidget(self.page_3)

        self.main_pages_layout.addWidget(self.pages)
        # page_3 설정
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")

        # 파일 시스템 모델 생성
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath('')  # 여기에 원하는 시작 경로를 설정할 수 있습니다.

        # QTreeView 생성
        self.file_tree_view = QTreeView(self.page_3)
        self.file_tree_view.setModel(self.file_system_model)  # QTreeView에 모델 설정
        self.file_tree_view.setRootIndex(self.file_system_model.index(''))  # 여기에 원하는 시작 경로를 설정할 수 있습니다.
        self.file_tree_view.setObjectName(u"file_tree_view")
        self.file_tree_view.setAnimated(False)
        self.file_tree_view.setIndentation(20)
        self.file_tree_view.setSortingEnabled(True)
        self.file_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_tree_view.setStyleSheet("""
                        QTreeView {
                            border: none;
                            background-color: #2C313C;
                        }
                        QTreeView::header {
                        border: none; 
                        background-color: #2C313C; /* 
                          }
                    """)
        # FileTreeView에 최소 크기를 설정하는 예시
        self.file_tree_view.setMinimumSize(1300, 600)

        # page_3_layout에 file_tree_view를 추가
        self.page_3_layout.addWidget(self.file_tree_view)
        # QTreeView의 헤더를 가져와서 설정
        header = self.file_tree_view.header()

        # 첫 번째 열의 너비를 내용에 맞게 조정
        header.resizeSection(0, header.sectionSizeHint(0))

        # 모든 열이 내용에 맞게 자동으로 조정되도록 설정
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # 또는 특정 열을 사용 가능한 공간에 맞춰서 스트레치하도록 설정
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        # Enable the context menu for the file_tree_view
        self.file_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree_view.customContextMenuRequested.connect(self.openContextMenu)

        self.pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainPages)

    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Kisa 점검사항", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi

#우클릭 이벤트
    def openContextMenu(self, position):
        index = self.file_tree_view.indexAt(position)
        if not index.isValid():
            return  # 유효한 인덱스가 아니면 함수를 종료합니다.

        # 필요에 따라 다른 열 번호로 변경할 수 있습니다.
        model = self.file_tree_view.model()
        filename = model.filePath(index)

        menu = QMenu()
        action_virus_total = QAction("Virus Total", self.file_tree_view)
        action_detailed_info = QAction("상세정보", self.file_tree_view)

        menu.addAction(action_virus_total)
        menu.addAction(action_detailed_info)

        # QAction의 triggered 이벤트에 연결할 때, filename을 전달합니다.
        action_virus_total.triggered.connect(lambda: self.virus_total_clicked(filename))
        action_detailed_info.triggered.connect(self.detailed_info_clicked)

        menu.exec_(self.file_tree_view.viewport().mapToGlobal(position))

    def virus_total_clicked(self, filename):
        print(filename)
        try:
            # API 호출 결과를 저장
            response_texts_generator = self.api.VirusTotal.upload_file(filename)
            response_texts = response_texts_generator()
            # 로그 메시지를 저장하기 위한 문자열 초기화
            combined_text = ""

            # 제너레이터에서 로그 메시지를 순서대로 읽어옴
            for text in response_texts:
                if text is None:
                    break
                combined_text += text
            # QMessageBox를 생성하여 텍스트 표시
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Information)
            message_box.setWindowTitle("Virus Total 결과")
            message_box.setText(combined_text)
            message_box.setStandardButtons(QMessageBox.Ok)
            ok_button = message_box.button(QMessageBox.Ok)
            if ok_button:
                ok_button.setStyleSheet(f"""
                               QPushButton {{
                                   border-radius: 8px;
                                   color: #8a95aa;
                                   background-color: #1b1e23;
                               }}
                           """)
                ok_button.setMinimumSize(100, 40)

            message_box.setStyleSheet("""
                     QMessageBox {
                         background-color: #2C313C;
                     }
                     QLabel {
                         font-size: 20px; 
                         color: white;
                     }

                     """)
            spacer = QSpacerItem(500, 500, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout = message_box.layout()
            layout.addItem(spacer, layout.rowCount(), 0, 1, layout.columnCount())

            # QMessageBox 표시
            message_box.exec_()

        except Exception as e:
            print(f"오류 발생: {e}")

    def detailed_info_clicked(self):
        selected_indexes = self.file_tree_view.selectionModel().selectedIndexes()
        selected_indexes = [index for index in selected_indexes if index.column() == 0]

        if selected_indexes:
            index = selected_indexes[0]  # 첫 번째 선택된 항목
            file_info = self.file_system_model.fileInfo(index)

            file_details = (
                f"파일 이름: {file_info.fileName()}\n"
                f"파일 경로: {file_info.filePath()}\n"
                f"파일 크기: {file_info.size()} 바이트\n"
                f"마지막 변경 날짜: {file_info.lastModified().toString('yyyy-MM-dd hh:mm:ss')}\n"
                f"생성 날짜: {file_info.birthTime().toString('yyyy-MM-dd hh:mm:ss')}"
            )

            # QMessageBox를 생성하고 설정합니다.
            detailed_info_msg = QMessageBox()
            detailed_info_msg.setIcon(QMessageBox.Information)
            detailed_info_msg.setText(file_details)
            detailed_info_msg.setWindowTitle("파일 상세 정보")
            detailed_info_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            # QMessageBox를 실행합니다.
            retval = detailed_info_msg.exec_()

            if retval == QMessageBox.Ok:
                print("확인 버튼이 클릭되었습니다.")

                # 여기까지