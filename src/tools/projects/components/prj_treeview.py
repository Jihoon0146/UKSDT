# app/tree_panel.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from .prj_treeview_ui import Ui_ProjectsTreeView

class ProjectsTreeViewWidget(QWidget):
    """
    좌측 트리 패널. 외부 주입:
      - setModel(model): QStandardItemModel 주입
    외부 신호:
      - selectionChanged(QModelIndex or None)
    """
    selectionChanged = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectsTreeView()
        self.ui.setupUi(self)

    def setModel(self, model):
        self.ui.treeProjects.setModel(model)
        self.ui.treeProjects.expandAll()
        
        # '완료' 루트를 접힌 상태로 설정
        if model.rowCount() >= 2:  # 진행 중, 완료 순서
            completed_index = model.index(1, 0)  # 두 번째 루트 (완료)
            if completed_index.isValid():
                collapsed_flag = model.data(completed_index, Qt.UserRole + 10)
                if collapsed_flag:
                    self.ui.treeProjects.setExpanded(completed_index, False)
        
        sel = self.ui.treeProjects.selectionModel()
        if sel is not None:
            sel.selectionChanged.connect(self._emit_selection)

    def _emit_selection(self, *_):
        sel = self.ui.treeProjects.selectionModel()
        idxs = sel.selectedIndexes() if sel else []
        self.selectionChanged.emit(idxs[0] if idxs else None)

    # 선택 인덱스 조회(옵션)
    def selectedIndex(self):
        sel = self.ui.treeProjects.selectionModel()
        idxs = sel.selectedIndexes() if sel else []
        return idxs[0] if idxs else None

    # QTreeView 직접 접근(옵션)
    def view(self):
        return self.ui.treeProjects
