from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QCheckBox, QComboBox, QPushButton,
                             QSpinBox, QGroupBox, QFormLayout, QLineEdit, 
                             QSlider, QButtonGroup, QRadioButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class SettingsDialog(QDialog):
    """통합앱 설정 다이얼로그"""
    
    settings_changed = pyqtSignal()  # 설정 변경 신호
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("UKSDT 설정")
        self.setModal(True)
        self.resize(500, 400)
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 각 탭 생성
        self.create_general_tab()
        self.create_appearance_tab()
        self.create_tools_tab()
        self.create_advanced_tab()
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.apply_btn = QPushButton("적용")
        self.ok_btn = QPushButton("확인")
        self.cancel_btn = QPushButton("취소")
        
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def create_general_tab(self):
        """일반 설정 탭"""
        general_widget = QWidget()
        layout = QVBoxLayout(general_widget)
        
        # 시작 설정 그룹
        startup_group = QGroupBox("시작 설정")
        startup_layout = QFormLayout(startup_group)
        
        self.auto_start_check = QCheckBox("시스템 시작 시 자동 실행")
        self.restore_tabs_check = QCheckBox("이전 세션의 탭 복원")
        self.show_welcome_check = QCheckBox("시작 시 환영 메시지 표시")
        
        startup_layout.addRow("자동 시작:", self.auto_start_check)
        startup_layout.addRow("탭 복원:", self.restore_tabs_check)
        startup_layout.addRow("환영 메시지:", self.show_welcome_check)
        
        layout.addWidget(startup_group)
        
        # 작업 디렉토리 설정 그룹
        workspace_group = QGroupBox("작업 공간")
        workspace_layout = QFormLayout(workspace_group)
        
        self.default_path_edit = QLineEdit("C:\\Projects")
        self.auto_save_check = QCheckBox("자동 저장 활성화")
        self.save_interval_spin = QSpinBox()
        self.save_interval_spin.setRange(1, 60)
        self.save_interval_spin.setValue(5)
        self.save_interval_spin.setSuffix(" 분")
        
        workspace_layout.addRow("기본 경로:", self.default_path_edit)
        workspace_layout.addRow("자동 저장:", self.auto_save_check)
        workspace_layout.addRow("저장 간격:", self.save_interval_spin)
        
        layout.addWidget(workspace_group)
        layout.addStretch()
        
        self.tab_widget.addTab(general_widget, "일반")
        
    def create_appearance_tab(self):
        """외관 설정 탭"""
        appearance_widget = QWidget()
        layout = QVBoxLayout(appearance_widget)
        
        # 테마 설정 그룹
        theme_group = QGroupBox("테마 설정")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["다크 테마", "라이트 테마", "자동 (시스템 설정)"])
        
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setRange(8, 18)
        self.font_size_slider.setValue(11)
        self.font_size_label = QLabel("11pt")
        
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(self.font_size_slider)
        font_size_layout.addWidget(self.font_size_label)
        
        theme_layout.addRow("테마:", self.theme_combo)
        theme_layout.addRow("글꼴 크기:", font_size_layout)
        
        layout.addWidget(theme_group)
        
        # UI 설정 그룹
        ui_group = QGroupBox("UI 설정")
        ui_layout = QFormLayout(ui_group)
        
        self.animations_check = QCheckBox("애니메이션 효과")
        self.animations_check.setChecked(True)
        self.toolbar_icons_check = QCheckBox("툴바 아이콘 표시")
        self.toolbar_icons_check.setChecked(True)
        self.status_bar_check = QCheckBox("상태바 표시")
        self.status_bar_check.setChecked(True)
        
        ui_layout.addRow("애니메이션:", self.animations_check)
        ui_layout.addRow("툴바 아이콘:", self.toolbar_icons_check)
        ui_layout.addRow("상태바:", self.status_bar_check)
        
        layout.addWidget(ui_group)
        layout.addStretch()
        
        self.tab_widget.addTab(appearance_widget, "외관")
        
    def create_tools_tab(self):
        """도구 설정 탭"""
        tools_widget = QWidget()
        layout = QVBoxLayout(tools_widget)
        
        # 도구 활성화 설정 그룹
        tools_group = QGroupBox("도구 활성화")
        tools_layout = QVBoxLayout(tools_group)
        
        self.control_dr_check = QCheckBox("Control DR Reviewer")
        self.control_dr_check.setChecked(True)
        self.eco_ppt_check = QCheckBox("ECO PPT Maker")
        self.eco_ppt_check.setChecked(True)
        
        tools_layout.addWidget(self.control_dr_check)
        tools_layout.addWidget(self.eco_ppt_check)
        
        layout.addWidget(tools_group)
        
        # 도구 기본 설정 그룹
        defaults_group = QGroupBox("기본 설정")
        defaults_layout = QFormLayout(defaults_group)
        
        # 현재는 특별한 기본 설정이 필요하지 않으므로 빈 그룹으로 유지
        info_label = QLabel("도구별 기본 설정은 각 도구 내에서 관리됩니다.")
        info_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        defaults_layout.addRow(info_label)
        
        layout.addWidget(defaults_group)
        layout.addStretch()
        
        self.tab_widget.addTab(tools_widget, "도구")
        
    def create_advanced_tab(self):
        """고급 설정 탭"""
        advanced_widget = QWidget()
        layout = QVBoxLayout(advanced_widget)
        
        # 성능 설정 그룹
        performance_group = QGroupBox("성능 설정")
        performance_layout = QFormLayout(performance_group)
        
        self.memory_limit_spin = QSpinBox()
        self.memory_limit_spin.setRange(512, 8192)
        self.memory_limit_spin.setValue(2048)
        self.memory_limit_spin.setSuffix(" MB")
        
        self.thread_count_spin = QSpinBox()
        self.thread_count_spin.setRange(1, 16)
        self.thread_count_spin.setValue(4)
        
        self.cache_enabled_check = QCheckBox("캐시 사용")
        self.cache_enabled_check.setChecked(True)
        
        performance_layout.addRow("메모리 제한:", self.memory_limit_spin)
        performance_layout.addRow("스레드 수:", self.thread_count_spin)
        performance_layout.addRow("캐시:", self.cache_enabled_check)
        
        layout.addWidget(performance_group)
        
        # 로깅 설정 그룹
        logging_group = QGroupBox("로깅 설정")
        logging_layout = QFormLayout(logging_group)
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.log_level_combo.setCurrentText("INFO")
        
        self.log_to_file_check = QCheckBox("파일로 로그 저장")
        self.log_to_file_check.setChecked(True)
        
        logging_layout.addRow("로그 레벨:", self.log_level_combo)
        logging_layout.addRow("파일 저장:", self.log_to_file_check)
        
        layout.addWidget(logging_group)
        layout.addStretch()
        
        self.tab_widget.addTab(advanced_widget, "고급")
        
    def setup_connections(self):
        """시그널 연결"""
        self.font_size_slider.valueChanged.connect(
            lambda v: self.font_size_label.setText(f"{v}pt")
        )
        
        self.apply_btn.clicked.connect(self.apply_settings)
        self.ok_btn.clicked.connect(self.accept_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
    def apply_settings(self):
        """설정 적용"""
        # 실제 구현에서는 여기서 설정을 저장하고 적용
        print("설정이 적용되었습니다.")
        self.settings_changed.emit()
        
    def accept_settings(self):
        """설정 적용 후 닫기"""
        self.apply_settings()
        self.accept()
        
    def get_settings(self):
        """현재 설정값들을 딕셔너리로 반환"""
        return {
            'general': {
                'auto_start': self.auto_start_check.isChecked(),
                'restore_tabs': self.restore_tabs_check.isChecked(),
                'show_welcome': self.show_welcome_check.isChecked(),
                'default_path': self.default_path_edit.text(),
                'auto_save': self.auto_save_check.isChecked(),
                'save_interval': self.save_interval_spin.value()
            },
            'appearance': {
                'theme': self.theme_combo.currentText(),
                'font_size': self.font_size_slider.value(),
                'animations': self.animations_check.isChecked(),
                'toolbar_icons': self.toolbar_icons_check.isChecked(),
                'status_bar': self.status_bar_check.isChecked()
            },
            'tools': {
                'control_dr_enabled': self.control_dr_check.isChecked(),
                'eco_ppt_enabled': self.eco_ppt_check.isChecked()
            },
            'advanced': {
                'memory_limit': self.memory_limit_spin.value(),
                'thread_count': self.thread_count_spin.value(),
                'cache_enabled': self.cache_enabled_check.isChecked(),
                'log_level': self.log_level_combo.currentText(),
                'log_to_file': self.log_to_file_check.isChecked()
            }
        }