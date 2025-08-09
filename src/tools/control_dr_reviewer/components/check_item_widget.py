"""
CheckItemWidget: 재사용 가능한 체크 항목 위젯

Pass/Fail 라디오 버튼을 가진 체크 항목 컴포넌트입니다.
Control DR Reviewer 등 체크리스트가 필요한 곳에서 사용할 수 있습니다.
"""

from PyQt5.QtWidgets import QWidget, QButtonGroup, QFrame
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

from ui_generated.ui_check_item import Ui_CheckItem

class CheckItemWidget(QFrame):
    """
    재사용 가능한 체크 항목 위젯
    
    Signals:
        status_changed(str): 상태가 변경될 때 발생 ('Pass', 'Fail', 'None')
    """
    
    # 시그널 정의
    status_changed = pyqtSignal(str)
    
    def __init__(self, item_text: str = "체크 항목", parent=None):
        """
        CheckItemWidget 초기화
        
        Args:
            item_text: 체크 항목 텍스트
            parent: 부모 위젯
        """
        super().__init__(parent)
        
        # UI 설정
        self.ui = Ui_CheckItem()
        self.ui.setupUi(self)
        
        self.item_text = item_text
        self.button_group = None
        
        # UI 요소에 대한 참조 설정
        self.item_label = self.ui.item_label
        self.pass_radio = self.ui.pass_radio
        self.fail_radio = self.ui.fail_radio
        self.na_radio = self.ui.na_radio
        self.comment_text = self.ui.comment_text
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """UI 추가 설정"""
        # 라디오 버튼 그룹 설정 (하나만 선택 가능)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.pass_radio)
        self.button_group.addButton(self.fail_radio)
        self.button_group.addButton(self.na_radio)
        
        # 버튼 그룹을 exclusive하지 않게 설정하여 모두 해제 가능
        self.button_group.setExclusive(False)
        
        # 항목 텍스트 설정
        self.item_label.setText(self.item_text)
        
        # 기본 상태는 아무것도 선택하지 않은 None 상태
            
    def setup_connections(self):
        """시그널 연결"""
        self.pass_radio.toggled.connect(self._on_pass_toggled)
        self.fail_radio.toggled.connect(self._on_fail_toggled)
        self.na_radio.toggled.connect(self._on_na_toggled)
    
    def _on_pass_toggled(self, checked):
        """Pass 버튼 토글 시 호출"""
        if checked:
            # Pass가 선택되면 Fail, N/A 해제
            self.fail_radio.setChecked(False)
            self.na_radio.setChecked(False)
            self.status_changed.emit('Pass')
        else:
            # Pass가 해제되면 상태 확인
            if not self.fail_radio.isChecked() and not self.na_radio.isChecked():
                self.status_changed.emit('None')
    
    def _on_fail_toggled(self, checked):
        """Fail 버튼 토글 시 호출"""
        if checked:
            # Fail이 선택되면 Pass, N/A 해제
            self.pass_radio.setChecked(False)
            self.na_radio.setChecked(False)
            self.status_changed.emit('Fail')
        else:
            # Fail이 해제되면 상태 확인
            if not self.pass_radio.isChecked() and not self.na_radio.isChecked():
                self.status_changed.emit('None')
    
    def _on_na_toggled(self, checked):
        """N/A 버튼 토글 시 호출"""
        if checked:
            # N/A가 선택되면 Pass, Fail 해제
            self.pass_radio.setChecked(False)
            self.fail_radio.setChecked(False)
            self.status_changed.emit('N/A')
        else:
            # N/A가 해제되면 상태 확인
            if not self.pass_radio.isChecked() and not self.fail_radio.isChecked():
                self.status_changed.emit('None')
    
    def get_status(self) -> str:
        """
        현재 선택된 상태를 반환
        
        Returns:
            str: 'Pass', 'Fail', 'N/A', 'None'
        """
        if self.pass_radio.isChecked():
            return 'Pass'
        elif self.fail_radio.isChecked():
            return 'Fail'
        elif self.na_radio.isChecked():
            return 'N/A'
        else:
            return 'None'  # 아무것도 선택하지 않은 상태
    
    def set_status(self, status: str):
        """
        상태를 설정
        
        Args:
            status: 'Pass', 'Fail', 'N/A', 'None' 중 하나
        """
            
        # 모든 버튼 해제
        self.pass_radio.setChecked(False)
        self.fail_radio.setChecked(False)
        self.na_radio.setChecked(False)
        
        # 상태에 따라 버튼 선택
        if status == 'Pass':
            self.pass_radio.setChecked(True)
        elif status == 'Fail':
            self.fail_radio.setChecked(True)
        elif status == 'N/A':
            self.na_radio.setChecked(True)
        # None인 경우 모든 버튼이 해제된 상태로 유지
    
    def get_item_text(self) -> str:
        """항목 텍스트 반환"""
        return self.item_text
    
    def set_item_text(self, text: str):
        """
        항목 텍스트 설정
        
        Args:
            text: 새로운 항목 텍스트
        """
        self.item_text = text
        self.item_label.setText(text)
    
    def clear_selection(self):
        """선택 해제 (None 상태로 리셋)"""
        self.set_status('None')
    
    def is_checked(self) -> bool:
        """Pass, Fail, N/A 중 하나가 선택되었는지 확인 (None이 아닌지)"""
        return self.get_status() in ['Pass', 'Fail', 'N/A']
    
    def get_comment(self) -> str:
        """코멘트 텍스트 반환"""
        return self.comment_text.toPlainText()
    
    def set_comment(self, text: str):
        """
        코멘트 텍스트 설정
        
        Args:
            text: 코멘트 텍스트
        """
        self.comment_text.setPlainText(text)