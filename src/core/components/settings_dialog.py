from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from .settings_dialog_ui import Ui_SettingsDialog

class SettingsDialog(QDialog):
    """통합앱 설정 다이얼로그"""
    
    settings_changed = pyqtSignal()  # 설정 변경 신호
    login_requested = pyqtSignal(str, str, bool)  # ID, PW, auto_login
    logout_requested = pyqtSignal()
    
    def __init__(self, parent=None, login_manager=None):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.login_manager = login_manager
        
        self.setup_connections()
        self.update_login_status()
        
    def setup_connections(self):
        """시그널 연결"""
        # 버튼 연결
        self.ui.apply_btn.clicked.connect(self.apply_settings)
        self.ui.ok_btn.clicked.connect(self.accept_settings)
        self.ui.cancel_btn.clicked.connect(self.reject)
        
        # Account 탭 연결
        self.ui.login_btn.clicked.connect(self.handle_login)
        self.ui.logout_btn.clicked.connect(self.handle_logout)
        self.ui.change_password_btn.clicked.connect(self.handle_change_password)
        self.ui.clear_credentials_btn.clicked.connect(self.handle_clear_credentials)
        
    def handle_login(self):
        """로그인 처리"""
        user_id = self.ui.user_id_edit.text().strip()
        password = self.ui.password_edit.text()
        auto_login = self.ui.auto_login_check.isChecked()
        
        if not user_id or not password:
            QMessageBox.warning(self, "입력 오류", "사용자 ID와 비밀번호를 모두 입력해주세요.")
            return
            
        self.login_requested.emit(user_id, password, auto_login)
        
    def handle_logout(self):
        """로그아웃 처리"""
        self.logout_requested.emit()
        
    def handle_change_password(self):
        """비밀번호 변경 처리"""
        # TODO: 비밀번호 변경 다이얼로그 구현
        QMessageBox.information(self, "기능 준비 중", "비밀번호 변경 기능은 준비 중입니다.")
        
    def handle_clear_credentials(self):
        """저장된 인증 정보 삭제"""
        reply = QMessageBox.question(self, "인증 정보 삭제", 
                                   "저장된 모든 인증 정보를 삭제하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes and self.login_manager:
            self.login_manager.clear_credentials()
            self.ui.user_id_edit.clear()
            self.ui.password_edit.clear()
            self.ui.auto_login_check.setChecked(False)
            self.update_login_status()
            QMessageBox.information(self, "완료", "인증 정보가 삭제되었습니다.")
            
    def update_login_status(self):
        """로그인 상태 UI 업데이트"""
        if self.login_manager and self.login_manager.is_authenticated():
            user_id = self.login_manager.get_current_user()
            last_login = self.login_manager.get_last_login_time()
            
            self.ui.current_status_label.setText(f"🔐 로그인됨: {user_id}")
            self.ui.last_login_label.setText(f"마지막 로그인: {last_login}")
            self.ui.login_btn.setEnabled(False)
            self.ui.logout_btn.setEnabled(True)
            self.ui.change_password_btn.setEnabled(True)
            
            # 현재 사용자 정보로 폼 채우기
            self.ui.user_id_edit.setText(user_id)
            self.ui.password_edit.clear()  # 보안상 비밀번호는 표시하지 않음
        else:
            self.ui.current_status_label.setText("🔒 로그인되지 않음")
            self.ui.last_login_label.setText("마지막 로그인: -")
            self.ui.login_btn.setEnabled(True)
            self.ui.logout_btn.setEnabled(False)
            self.ui.change_password_btn.setEnabled(False)
            
            # 저장된 자격 증명이 있으면 ID만 채우기
            if self.login_manager:
                saved_creds = self.login_manager.get_saved_credentials()
                if saved_creds:
                    self.ui.user_id_edit.setText(saved_creds.get('user_id', ''))
                    self.ui.auto_login_check.setChecked(saved_creds.get('auto_login', False))
        
    def apply_settings(self):
        """설정 적용"""
        print("설정이 적용되었습니다.")
        self.settings_changed.emit()
        
    def accept_settings(self):
        """설정 적용 후 닫기"""
        self.apply_settings()
        self.accept()