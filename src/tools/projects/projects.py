import json
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore
from .projects_ui import Ui_Projects

from .components.prj_models import DataModel, Project
from .components.prj_treebuilder import *
from .components.prj_detailview import *
from .components.prj_treeview import *

DATA_PATH = Path(os.path.join(os.environ.get("UKSDT_RESOURCE_PATH",""), "data", "projects.sample.json"))

class ProjectsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Projects()
        self.ui.setupUi(self)

        # 컴포넌트 탑재
        self.leftPanel = ProjectsTreeViewWidget(self)
        self.rightPanel = ProjectsDetailViewWidget(self)
        self.ui.leftPane.layout().addWidget(self.leftPanel)
        self.ui.rightPane.layout().addWidget(self.rightPanel)

        # 데이터 로드 및 트리 구성
        self.data_model = self._load_data()
        self.model = build_tree_model(self.data_model)
        self.leftPanel.setModel(self.model)

        # 시그널 연결
        self.leftPanel.selectionChanged.connect(self.on_selection_changed)
        self.rightPanel.saveRequested.connect(self.on_save_clicked)
        self.rightPanel.resetRequested.connect(self.on_reset_clicked)

        # 초기
        self.rightPanel.showChildren()

        # wrapper 콤보 초기화
        self._refresh_wrapper_combo()

    # ---------- IO ----------
    def _load_data(self) -> DataModel:
        obj = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        return DataModel.from_json(obj)

    def _save_data(self):
        DATA_PATH.write_text(
            json.dumps(self.data_model.to_json(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---------- UI helpers ----------
    def _refresh_wrapper_combo(self):
        d = self.rightPanel.detail
        d.comboWrapper.clear()
        d.comboWrapper.addItem("(없음)", "")
        for w in self.data_model.wrappers:
            d.comboWrapper.addItem(w.name, w.id)

    def _fill_children_table(self, items):
        t = self.rightPanel.children.tableChildren
        t.clearContents()
        t.setRowCount(len(items))
        t.setColumnCount(3)
        t.setHorizontalHeaderLabels(["ID", "이름", "상태"])
        for r, it in enumerate(items):
            t.setItem(r, 0, self._mk_item(it["id"]))
            t.setItem(r, 1, self._mk_item(it["name"]))
            t.setItem(r, 2, self._mk_item(it["status"]))
        t.resizeColumnsToContents()

    @staticmethod
    def _mk_item(text):
        from PyQt5.QtWidgets import QTableWidgetItem
        it = QTableWidgetItem(str(text))
        it.setFlags(it.flags() ^ QtCore.Qt.ItemIsEditable)
        return it

    # ---------- selection ----------
    def on_selection_changed(self, idx):
        if idx is None:
            self.rightPanel.showChildren()
            self._fill_children_table([])
            return
        node_type = idx.data(ROLE_TYPE)
        node_id   = idx.data(ROLE_ID)
        if node_type == "project":
            self._show_project_detail(node_id)
        elif node_type in ("status_root", "wrapper"):
            items = self._children_of(node_type, node_id)
            self._fill_children_table(items)
            self.rightPanel.showChildren()

    def _children_of(self, node_type, node_id):
        children = []
        if node_type == "status_root":
            status = node_id
            # wrappers
            for w in [w for w in self.data_model.wrappers if w.status == status]:
                children.append({"id": w.id, "name": w.name, "status": w.status})
            # loose projects
            for p in [p for p in self.data_model.projects if p.status == status and not p.wrapper_id]:
                children.append({"id": p.id, "name": p.name, "status": p.status})
        elif node_type == "wrapper":
            for p in [p for p in self.data_model.projects if p.wrapper_id == node_id]:
                children.append({"id": p.id, "name": p.name, "status": p.status})
        return children

    # ---------- detail ----------
    def _show_project_detail(self, project_id: str):
        p = next((x for x in self.data_model.projects if x.id == project_id), None)
        if not p:
            QMessageBox.warning(self, "오류", "프로젝트를 찾을 수 없음")
            return
        d = self.rightPanel.detail
        d.valId.setText(p.id)
        d.editName.setText(p.name)
        d.editOwner.setText(p.owner)
        d.comboStatus.setCurrentText(p.status)
        # wrapper
        idx = d.comboWrapper.findData(p.wrapper_id or "")
        d.comboWrapper.setCurrentIndex(max(0, idx))
        # dates
        from PyQt5.QtCore import QDate
        y, m, d0 = map(int, p.start_date.split("-"))
        d.dateStart.setDate(QDate(y, m, d0))
        y, m, d0 = map(int, p.end_date.split("-"))
        d.dateEnd.setDate(QDate(y, m, d0))

        d.comboType.setCurrentText(p.type)
        d.editNotes.setPlainText(p.notes or "")
        self.rightPanel.showProjectDetail()

    # ---------- save/reset ----------
    def on_save_clicked(self):
        d = self.rightPanel.detail
        pid = d.valId.text()
        p = next((x for x in self.data_model.projects if x.id == pid), None)
        if not p:
            QMessageBox.warning(self, "오류", "프로젝트를 찾을 수 없음")
            return
        p.name = d.editName.text()
        p.owner = d.editOwner.text()
        p.status = d.comboStatus.currentText()  # type: ignore
        wdata = d.comboWrapper.currentData()
        p.wrapper_id = wdata if wdata else None
        p.start_date = d.dateStart.date().toString("yyyy-MM-dd")
        p.end_date = d.dateEnd.date().toString("yyyy-MM-dd")
        p.type = d.comboType.currentText()  # type: ignore
        p.notes = d.editNotes.toPlainText()

        self._save_data()
        # 트리 재구성(상태/랩퍼 변경 반영)
        self.model = build_tree_model(self.data_model)
        self.leftPanel.setModel(self.model)
        QMessageBox.information(self, "저장", "프로젝트 정보 저장 완료")

    def on_reset_clicked(self):
        d = self.rightPanel.detail
        pid = d.valId.text()
        if pid:
            self._show_project_detail(pid)
