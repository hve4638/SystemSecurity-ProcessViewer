from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QAction, QToolBar, \
    QLineEdit, QWidget, QVBoxLayout, QMenu, QDialog, QLabel, QTextEdit, QSplitter
from PyQt5.QtCore import QDir, Qt
import sys

class InfoDialog(QDialog):
    def __init__(self, file_info):
        super().__init__()
        self.setWindowTitle(f"Info for {file_info.fileName()}")
        layout = QVBoxLayout()
        label = QLabel(f"Full Path: {file_info.absoluteFilePath()}\nSize: {file_info.size()} bytes")
        layout.addWidget(label)
        self.setLayout(layout)

class FileExplorer(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialogs = []  # 생성된 QDialog 객체들을 저장하기 위한 리스트
        self.ctrl_pressed = False  # 컨트롤 키가 눌려 있는지 확인
        self.back_history = []  # 뒤로 가기를 위한 히스토리
        self.forward_history = []  # 앞으로 가기를 위한 히스토리
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("File Explorer")

        # QSplitter를 사용하여 수평 레이아웃 생성
        splitter = QSplitter(Qt.Horizontal)

        # 파일 시스템 모델 생성
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # 파일 시스템 뷰 생성
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)  # ExtendedSelection 모드로 설정
        self.tree_view.doubleClicked.connect(self.navigateToClickedPath)  # 클릭 이벤트를 새 메서드에 연결

        # 터미널 창 생성
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)  # 읽기 전용 모드로 설정
        self.terminal_output.setMinimumHeight(100)  # 터미널 창의 최소 높이 설정

        # QSplitter에 위젯 추가
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.terminal_output)

        # 수평 레이아웃에서 비율을 4:3으로 설정
        sizes = [4, 3]
        splitter.setSizes(sizes)

        # 중앙 위젯 설정
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)  # QSplitter를 중앙 위젯에 추가
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 툴바 생성
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        self.back_action = QAction("←", self)
        self.back_action.triggered.connect(self.goBack)
        toolbar.addAction(self.back_action)
        self.forward_action = QAction("→", self)
        self.forward_action.triggered.connect(self.goForward)
        toolbar.addAction(self.forward_action)

        # 현재 경로 표시 및 수정
        self.path_input = QLineEdit(self)
        self.path_input.returnPressed.connect(self.navigateToPath)  # 엔터 키 이벤트 연결
        toolbar.addWidget(self.path_input)  # 입력란을 툴바에 추가
        self.back_history.append(self.model.index(QDir.rootPath()))

        # Clicked 추가
        self.tree_view.clicked.connect(self.handleTreeViewClick)

    def handleTreeViewClick(self, index):
        self.updateStatusbar(index)
        self.updateHistoryOnClick(index)

    def updateHistoryOnClick(self, index):
        current_index = self.tree_view.rootIndex()
        if current_index != index.parent():
            self.back_history.append(current_index)
            self.forward_history.clear()
            self.updateButtonState()

    def navigateToPath(self):
        current_index = self.tree_view.rootIndex()
        path = self.path_input.text()
        index = self.model.index(path)
        if index.isValid():
            if current_index != index:
                self.back_history.append(current_index)
                self.forward_history.clear()
            self.tree_view.setRootIndex(index)
            self.updateStatusbar(index)
            self.updateButtonState()

    def navigateToClickedPath(self, index):
        if index.isValid() and self.model.isDir(index):
            current_index = self.tree_view.rootIndex()
            if current_index != index:
                if not self.back_history or self.back_history[-1] != current_index:
                    self.back_history.append(current_index)
                self.forward_history.clear()
                self.tree_view.setRootIndex(index)
                self.updateStatusbar(index)
                self.updateButtonState()

    def updateNavigationButtons(self):
        self.back_action.setEnabled(bool(self.back_history))
        self.forward_action.setEnabled(bool(self.forward_history))

    def goBack(self):
        if self.back_history:
            current_index = self.tree_view.rootIndex()
            self.forward_history.append(current_index)
            self.tree_view.setRootIndex(self.back_history.pop())
            self.updateStatusbar(self.tree_view.rootIndex())
            self.updateButtonState()

    def goForward(self):
        if self.forward_history:
            current_index = self.tree_view.rootIndex()
            self.back_history.append(current_index)
            self.tree_view.setRootIndex(self.forward_history.pop())
            self.updateStatusbar(self.tree_view.rootIndex())
            self.updateButtonState()

    def searchFiles(self):
        query = self.search_input.text()
        if query:
            root_index = self.tree_view.rootIndex()
            self.search_results = []
            self.findFiles(root_index, query)
            self.updateTreeView()
            self.updateStatusbar(root_index)

    def findFiles(self, index, query):
        if index.isValid():
            if query.lower() in self.model.fileName(index).lower():
                self.search_results.append(index)
            if self.model.isDir(index):
                for i in range(self.model.rowCount(index)):
                    child_index = self.model.index(i, 0, index)
                    self.findFiles(child_index, query)

    def updateTreeView(self):
        self.tree_view.setModel(None)
        self.model.setNameFilters([])
        self.model.setRootPath("")
        self.model.setNameFilters(['*'])
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.tree_view.model().index(QDir.rootPath()))
        for index in self.search_results:
            self.tree_view.expand(index)

    def showContextMenu(self, pos):
        index = self.tree_view.indexAt(pos)
        if index.isValid():
            self.context_menu.exec_(self.tree_view.mapToGlobal(pos))

    def showDetails(self):
        all_selected_indexes = self.tree_view.selectionModel().selectedIndexes()
        selected_indexes = [index for index in all_selected_indexes if index.column() == 0]

        if len(selected_indexes) > 1:
            for index in selected_indexes:
                file_info = self.model.fileInfo(index)
                details_dialog = QDialog(self)
                layout = QVBoxLayout(details_dialog)
                self.addFileInfoToLayout(file_info, layout)

                details_dialog.setWindowTitle(file_info.fileName())
                details_dialog.setLayout(layout)
                details_dialog.show()

                self.dialogs.append(details_dialog)

            self.dialogs = [dialog for dialog in self.dialogs if dialog.isVisible()]

        else:
            index = self.tree_view.currentIndex()
            if index.isValid():
                file_info = self.model.fileInfo(index)

                details_dialog = QDialog(self)
                layout = QVBoxLayout(details_dialog)
                self.addFileInfoToLayout(file_info, layout)

                details_dialog.setWindowTitle(file_info.fileName())
                details_dialog.setLayout(layout)
                details_dialog.exec_()

    def addFileInfoToLayout(self, file_info, layout):
        file_name_label = QLabel(f"파일 이름: {file_info.fileName()}")
        layout.addWidget(file_name_label)
        file_size_label = QLabel(f"파일 크기: {file_info.size()} 바이트")
        layout.addWidget(file_size_label)
        file_path_label = QLabel(f"파일 경로: {file_info.filePath()}")
        layout.addWidget(file_path_label)
        last_modified_label = QLabel(f"마지막 변경날짜: {file_info.lastModified().toString()}")
        layout.addWidget(last_modified_label)
        last_accessed_label = QLabel(f"마지막 접근날짜: {file_info.lastRead().toString()}")
        layout.addWidget(last_accessed_label)
        created_label = QLabel(f"생성 날짜: {file_info.birthTime().toString()}")
        layout.addWidget(created_label)

    def updateStatusbar(self, index):
        current_path = self.model.filePath(index)
        self.path_input.setText(current_path)

    def updateButtonState(self):
        self.back_action.setEnabled(bool(self.back_history))
        self.forward_action.setEnabled(bool(self.forward_history))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())
