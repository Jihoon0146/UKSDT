import json
import os
import time
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QMenu
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from .projects_ui import Ui_Projects

from .components.prj_models import DataModel, Project, Wrapper
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
        self.rightPanel.completeRequested.connect(self.on_complete_clicked)
        
        # Wrapper 시그널 연결
        self.rightPanel.wrapperSaveRequested.connect(self.on_wrapper_save_clicked)
        self.rightPanel.wrapperResetRequested.connect(self.on_wrapper_reset_clicked)
        self.rightPanel.wrapperCompleteRequested.connect(self.on_wrapper_complete_clicked)
        
        # 컨텍스트 메뉴 설정
        self.setup_context_menu()

        # 초기
        self.rightPanel.showChildren()

        # wrapper 콤보 초기화
        self._refresh_wrapper_combo()
    
    def setup_context_menu(self):
        """트리뷰 컨텍스트 메뉴 설정"""
        tree_view = self.leftPanel.view()
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_view.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """컨텍스트 메뉴 표시"""
        tree_view = self.leftPanel.view()
        index = tree_view.indexAt(position)
        
        menu = QMenu(self)
        
        if index.isValid():
            node_type = index.data(ROLE_TYPE)
            node_id = index.data(ROLE_ID)
            
            if node_type == "status_root":
                # 상태 루트: Wrapper/Project 추가
                menu.addAction("Wrapper 추가", lambda: self.add_wrapper(node_id))
                menu.addAction("Project 추가", lambda: self.add_project(node_id))
            elif node_type == "wrapper":
                # Wrapper: Project 추가, Wrapper 삭제
                wrapper_status = self.get_wrapper_status(node_id)
                menu.addAction("Project 추가", lambda: self.add_project(wrapper_status, node_id))
                menu.addAction("Wrapper 삭제", lambda: self.delete_wrapper(node_id))
            elif node_type == "project":
                # Project: Project 삭제
                menu.addAction("Project 삭제", lambda: self.delete_project(node_id))
        
        if menu.actions():
            menu.exec_(tree_view.mapToGlobal(position))

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
        elif node_type == "wrapper":
            self._show_wrapper_detail(node_id)
        elif node_type == "status_root":
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
        # 상태를 읽기 전용 라벨에 표시
        status_text = "진행 중" if p.status == "in_progress" else "완료"
        d.valStatus.setText(status_text)
        
        # 완료 버튼은 진행 중일 때만 활성화
        d.btnComplete.setEnabled(p.status == "in_progress")
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
        # 상태는 완료 버튼을 통해서만 변경 가능
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
    
    # ---------- 추가/삭제 기능 ----------
    def get_pjt_name_input(self, title: str, label: str) -> str:
        """프로젝트/래퍼 이름 입력 다이얼로그"""
        name, ok = QInputDialog.getText(self, title, label)
        return name.strip() if ok and name.strip() else ""
    
    def generate_unique_id(self, prefix: str) -> str:
        """고유 ID 생성 (timestamp 기반)"""
        timestamp = str(int(time.time() * 1000))[-8:]  # 뒤 8자리 사용
        return f"{prefix}{timestamp}"
    
    def get_wrapper_status(self, wrapper_id: str) -> str:
        """Wrapper의 상태 조회"""
        wrapper = next((w for w in self.data_model.wrappers if w.id == wrapper_id), None)
        return wrapper.status if wrapper else "in_progress"
    
    def add_wrapper(self, status: str):
        """Wrapper 추가 (즉시 JSON 저장)"""
        name = self.get_pjt_name_input("Wrapper 추가", "Wrapper 이름을 입력하세요:")
        if not name:
            return
        
        new_id = self.generate_unique_id("w")
        wrapper = Wrapper(id=new_id, name=name, type="wrapper", status=status)
        self.data_model.wrappers.append(wrapper)
        
        # 즉시 저장
        self._save_data()
        
        # 트리 재구성 및 wrapper combo 업데이트
        self._rebuild_tree_and_refresh()
        
        QMessageBox.information(self, "추가 완료", f"Wrapper '{name}'이 추가되었습니다.")
    
    def add_project(self, status: str, wrapper_id: str = None):
        """Project 추가 (임시 추가 후 detail view 표시)"""
        name = self.get_pjt_name_input("Project 추가", "Project 이름을 입력하세요:")
        if not name:
            return
        
        new_id = self.generate_unique_id("p")
        project = Project(
            id=new_id,
            name=name,
            type="project",
            status=status,
            wrapper_id=wrapper_id,
            owner="",
            start_date="2025-01-01",
            end_date="2025-12-31",
            notes=""
        )
        self.data_model.projects.append(project)
        
        # 트리 재구성
        self._rebuild_tree_and_refresh()
        
        # 자동으로 detail view로 전환하여 편집 유도
        self._show_project_detail(new_id)
        
        QMessageBox.information(self, "추가 완료", 
                               f"Project '{name}'이 추가되었습니다.\n상세 정보를 입력한 후 저장 버튼을 클릭하세요.")
    
    def delete_wrapper(self, wrapper_id: str):
        """Wrapper 삭제 (하위 프로젝트 있으면 삭제 불가)"""
        # 하위 프로젝트 확인
        child_projects = [p for p in self.data_model.projects if p.wrapper_id == wrapper_id]
        if child_projects:
            project_names = ", ".join([p.name for p in child_projects])
            QMessageBox.warning(self, "삭제 불가", 
                               f"Wrapper에 하위 프로젝트가 있어 삭제할 수 없습니다.\n\n하위 프로젝트: {project_names}")
            return
        
        wrapper = next((w for w in self.data_model.wrappers if w.id == wrapper_id), None)
        if not wrapper:
            return
        
        # 확인 다이얼로그
        reply = QMessageBox.question(self, "Wrapper 삭제", 
                                   f"'{wrapper.name}' Wrapper를 삭제하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.data_model.wrappers = [w for w in self.data_model.wrappers if w.id != wrapper_id]
            self._save_data()
            self._rebuild_tree_and_refresh()
            
            # 우측 패널을 children view로 전환
            self.rightPanel.showChildren()
            self._fill_children_table([])
            
            QMessageBox.information(self, "삭제 완료", f"Wrapper '{wrapper.name}'이 삭제되었습니다.")
    
    def delete_project(self, project_id: str):
        """Project 삭제"""
        project = next((p for p in self.data_model.projects if p.id == project_id), None)
        if not project:
            return
        
        # 확인 다이얼로그
        reply = QMessageBox.question(self, "Project 삭제",
                                   f"'{project.name}' Project를 삭제하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.data_model.projects = [p for p in self.data_model.projects if p.id != project_id]
            self._save_data()
            self._rebuild_tree_and_refresh()
            
            # 우측 패널을 children view로 전환
            self.rightPanel.showChildren()
            self._fill_children_table([])
            
            QMessageBox.information(self, "삭제 완료", f"Project '{project.name}'이 삭제되었습니다.")
    
    def _rebuild_tree_and_refresh(self):
        """트리 재구성 및 UI 새로고침"""
        self.model = build_tree_model(self.data_model)
        self.leftPanel.setModel(self.model)
        self._refresh_wrapper_combo()
    
    # ---------- 완료 처리 로직 ----------
    def on_complete_clicked(self):
        """프로젝트 완료 처리"""
        d = self.rightPanel.detail
        pid = d.valId.text()
        project = next((p for p in self.data_model.projects if p.id == pid), None)
        
        if not project:
            QMessageBox.warning(self, "오류", "프로젝트를 찾을 수 없음")
            return
        
        if project.status == "completed":
            QMessageBox.information(self, "알림", "이미 완료된 프로젝트입니다.")
            return
        
        # 최종 확인
        reply = QMessageBox.question(self, "프로젝트 완료", 
                                   f"'{project.name}' 프로젝트를 완료 처리하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 프로젝트 상태 변경
            project.status = "completed"
            
            # 데이터 저장
            self._save_data()
            
            # UI 업데이트
            self._show_project_detail(pid)  # 상태 표시 및 버튼 상태 업데이트
            
            # 트리 재구성
            self._rebuild_tree_and_refresh()
            
            QMessageBox.information(self, "완료", f"'{project.name}' 프로젝트가 완료 처리되었습니다.")
            
            # Wrapper 자동 완료 체크
            if project.wrapper_id:
                self._check_wrapper_completion(project.wrapper_id)
    
    def _check_wrapper_completion(self, wrapper_id: str):
        """Wrapper의 모든 하위 프로젝트가 완료되었는지 체크하고 자동 완료 처리"""
        wrapper = next((w for w in self.data_model.wrappers if w.id == wrapper_id), None)
        if not wrapper or wrapper.status == "completed":
            return
        
        # 해당 wrapper의 모든 프로젝트 조회
        wrapper_projects = [p for p in self.data_model.projects if p.wrapper_id == wrapper_id]
        
        if not wrapper_projects:
            return
        
        # 모든 프로젝트가 완료 상태인지 확인
        all_completed = all(p.status == "completed" for p in wrapper_projects)
        
        if all_completed:
            # 사용자에게 Wrapper 완료 처리 여부 확인
            reply = QMessageBox.question(self, "Wrapper 완료", 
                                       f"'{wrapper.name}' Wrapper의 모든 하위 프로젝트가 완료되었습니다.\\n\\n"
                                       f"Wrapper도 완료 처리하시겠습니까?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                wrapper.status = "completed"
                self._save_data()
                self._rebuild_tree_and_refresh()
                
                QMessageBox.information(self, "완료", f"'{wrapper.name}' Wrapper가 완료 처리되었습니다.")
    
    # ---------- Wrapper 상세뷰 로직 ----------
    def _show_wrapper_detail(self, wrapper_id: str):
        """Wrapper 상세뷰 표시"""
        wrapper = next((w for w in self.data_model.wrappers if w.id == wrapper_id), None)
        if not wrapper:
            QMessageBox.warning(self, "오류", "Wrapper를 찾을 수 없음")
            return
        
        w = self.rightPanel.wrapper
        
        # 기본 정보
        w.valId.setText(wrapper.id)
        w.editName.setText(wrapper.name)
        status_text = "진행 중" if wrapper.status == "in_progress" else "완료"
        w.valStatus.setText(status_text)
        w.valType.setText(wrapper.type)
        
        # 하위 프로젝트 정보 계산
        wrapper_projects = [p for p in self.data_model.projects if p.wrapper_id == wrapper_id]
        total_count = len(wrapper_projects)
        completed_count = sum(1 for p in wrapper_projects if p.status == "completed")
        in_progress_count = total_count - completed_count
        progress_percent = int((completed_count / total_count * 100)) if total_count > 0 else 0
        
        # 현황 정보 업데이트
        w.valTotal.setText(f"{total_count}개")
        w.valInProgress.setText(f"{in_progress_count}개")
        w.valCompleted.setText(f"{completed_count}개")
        w.valProgress.setText(f"{progress_percent}%")
        w.progressBar.setValue(progress_percent)
        
        # 완료 버튼 상태 설정 (모든 하위 프로젝트가 완료되고 wrapper가 진행 중일 때만 활성화)
        can_complete = (wrapper.status == "in_progress" and 
                       total_count > 0 and 
                       completed_count == total_count)
        w.btnComplete.setEnabled(can_complete)
        
        # 하위 프로젝트 목록 테이블 업데이트
        self._fill_wrapper_projects_table(wrapper_projects)
        
        # Wrapper 상세뷰 표시
        self.rightPanel.showWrapperDetail()
    
    def _fill_wrapper_projects_table(self, projects):
        """Wrapper 상세뷰의 하위 프로젝트 테이블 채우기"""
        table = self.rightPanel.wrapper.tableProjects
        table.clearContents()
        table.setRowCount(len(projects))
        
        for row, project in enumerate(projects):
            # 프로젝트명 (상태 아이콘 포함)
            status_icon = "✅" if project.status == "completed" else "🔄"
            name_text = f"{status_icon} {project.name}"
            table.setItem(row, 0, self._mk_item(name_text))
            
            # 담당자
            table.setItem(row, 1, self._mk_item(project.owner))
            
            # 상태
            status_text = "완료" if project.status == "completed" else "진행 중"
            table.setItem(row, 2, self._mk_item(status_text))
            
            # 시작일/종료일
            table.setItem(row, 3, self._mk_item(project.start_date))
            table.setItem(row, 4, self._mk_item(project.end_date))
        
        table.resizeColumnsToContents()
    
    # ---------- Wrapper 버튼 핸들러 ----------
    def on_wrapper_save_clicked(self):
        """Wrapper 정보 저장"""
        w = self.rightPanel.wrapper
        wrapper_id = w.valId.text()
        wrapper = next((x for x in self.data_model.wrappers if x.id == wrapper_id), None)
        
        if not wrapper:
            QMessageBox.warning(self, "오류", "Wrapper를 찾을 수 없음")
            return
        
        # 이름만 수정 가능
        wrapper.name = w.editName.text()
        
        self._save_data()
        self._rebuild_tree_and_refresh()
        QMessageBox.information(self, "저장", "Wrapper 정보가 저장되었습니다.")
    
    def on_wrapper_reset_clicked(self):
        """Wrapper 정보 되돌리기"""
        w = self.rightPanel.wrapper
        wrapper_id = w.valId.text()
        if wrapper_id:
            self._show_wrapper_detail(wrapper_id)
    
    def on_wrapper_complete_clicked(self):
        """Wrapper 완료 처리"""
        w = self.rightPanel.wrapper
        wrapper_id = w.valId.text()
        wrapper = next((x for x in self.data_model.wrappers if x.id == wrapper_id), None)
        
        if not wrapper:
            QMessageBox.warning(self, "오류", "Wrapper를 찾을 수 없음")
            return
        
        if wrapper.status == "completed":
            QMessageBox.information(self, "알림", "이미 완료된 Wrapper입니다.")
            return
        
        # 하위 프로젝트 상태 재확인
        wrapper_projects = [p for p in self.data_model.projects if p.wrapper_id == wrapper_id]
        if not wrapper_projects:
            QMessageBox.warning(self, "오류", "하위 프로젝트가 없는 Wrapper는 완료 처리할 수 없습니다.")
            return
        
        completed_count = sum(1 for p in wrapper_projects if p.status == "completed")
        total_count = len(wrapper_projects)
        
        if completed_count < total_count:
            QMessageBox.warning(self, "완료 불가", 
                               f"모든 하위 프로젝트가 완료되지 않았습니다.\\n"
                               f"완료: {completed_count}개 / 전체: {total_count}개")
            return
        
        # 최종 확인
        reply = QMessageBox.question(self, "Wrapper 완료", 
                                   f"'{wrapper.name}' Wrapper를 완료 처리하시겠습니까?\\n\\n"
                                   f"모든 하위 프로젝트({total_count}개)가 완료된 상태입니다.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            wrapper.status = "completed"
            self._save_data()
            
            # UI 업데이트
            self._show_wrapper_detail(wrapper_id)  # 상태 및 버튼 업데이트
            self._rebuild_tree_and_refresh()
            
            QMessageBox.information(self, "완료", f"'{wrapper.name}' Wrapper가 완료 처리되었습니다.")
