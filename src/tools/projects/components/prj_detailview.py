# app/tree_panel.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from .prj_detailview_ui import Ui_ProjectsDetailView
from .prj_form_ui import Ui_ProjectDetailForm
from .prj_child_ui import Ui_ChildrenView
from .prj_wrapper_form_ui import Ui_WrapperDetailForm

class ProjectsDetailViewWidget(QWidget):
    """
    우측 스택 패널. 내부 페이지:
      - pageChildren: 상위 선택 시 1레벨 하위 목록
      - pageProjectDetail: 프로젝트 상세/편집
      - pageWrapperDetail: Wrapper 상세/편집
    외부 신호:
      - saveRequested()
      - resetRequested()
      - completeRequested()
      - wrapperSaveRequested()
      - wrapperResetRequested()
      - wrapperCompleteRequested()
    외부 메서드:
      - showChildren()
      - showProjectDetail()
      - showWrapperDetail()
      - detail / wrapper / children 서브-UI 핸들에 접근해 필드 바인딩 수행
    """
    saveRequested = pyqtSignal()
    resetRequested = pyqtSignal()
    completeRequested = pyqtSignal()
    wrapperSaveRequested = pyqtSignal()
    wrapperResetRequested = pyqtSignal()
    wrapperCompleteRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectsDetailView()
        self.ui.setupUi(self)

        # 서브 UI 로드
        self.detail = Ui_ProjectDetailForm()
        self.children = Ui_ChildrenView()
        self.wrapper = Ui_WrapperDetailForm()

        # 각 페이지에 장착
        self.detail.setupUi(self.ui.pageProjectDetail)
        self.children.setupUi(self.ui.pageChildren)
        self.wrapper.setupUi(self.ui.pageWrapperDetail)

        # 버튼 신호 재노출
        self.detail.btnSave.clicked.connect(self.saveRequested.emit)
        self.detail.btnReset.clicked.connect(self.resetRequested.emit)
        self.detail.btnComplete.clicked.connect(self.completeRequested.emit)
        
        # Wrapper 버튼 신호 연결
        self.wrapper.btnSave.clicked.connect(self.wrapperSaveRequested.emit)
        self.wrapper.btnReset.clicked.connect(self.wrapperResetRequested.emit)
        self.wrapper.btnComplete.clicked.connect(self.wrapperCompleteRequested.emit)

        # 초기 페이지
        self.ui.stackRight.setCurrentWidget(self.ui.pageChildren)

    def showChildren(self):
        self.ui.stackRight.setCurrentWidget(self.ui.pageChildren)

    def showProjectDetail(self):
        self.ui.stackRight.setCurrentWidget(self.ui.pageProjectDetail)
    
    def showWrapperDetail(self):
        self.ui.stackRight.setCurrentWidget(self.ui.pageWrapperDetail)
