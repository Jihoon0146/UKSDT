# app/tree_panel.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from .prj_detailview_ui import Ui_ProjectsDetailView
from .prj_form_ui import Ui_ProjectDetailForm
from .prj_child_ui import Ui_ChildrenView

class ProjectsDetailViewWidget(QWidget):
    """
    우측 스택 패널. 내부 페이지:
      - pageChildren: 상위 선택 시 1레벨 하위 목록
      - pageProjectDetail: 프로젝트 상세/편집
    외부 신호:
      - saveRequested()
      - resetRequested()
    외부 메서드:
      - showChildren()
      - showProjectDetail()
      - detail / children 서브-UI 핸들에 접근해 필드 바인딩 수행
    """
    saveRequested = pyqtSignal()
    resetRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectsDetailView()
        self.ui.setupUi(self)

        # 서브 UI 로드
        self.detail = Ui_ProjectDetailForm()
        self.children = Ui_ChildrenView()

        # 각 페이지에 장착
        self.detail.setupUi(self.ui.pageProjectDetail)
        self.children.setupUi(self.ui.pageChildren)

        # 버튼 신호 재노출
        self.detail.btnSave.clicked.connect(self.saveRequested.emit)
        self.detail.btnReset.clicked.connect(self.resetRequested.emit)

        # 초기 페이지
        self.ui.stackRight.setCurrentWidget(self.ui.pageChildren)

    def showChildren(self):
        self.ui.stackRight.setCurrentWidget(self.ui.pageChildren)

    def showProjectDetail(self):
        self.ui.stackRight.setCurrentWidget(self.ui.pageProjectDetail)
