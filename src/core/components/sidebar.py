from PyQt5.QtWidgets import (QWidget, QToolButton, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, 
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QParallelAnimationGroup, QSize
from PyQt5.QtGui import QPixmap, QPainter, QFont, QIcon

from .sidebar_ui import Ui_Sidebar
from .settings_dialog import SettingsDialog

def emoji_icon(emoji: str, size: int = 42) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    font = QFont("Segoe UI Emoji", int(size * 0.7))  # Emoji 전용 폰트 사용
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, emoji)
    painter.end()

    return QIcon(pixmap)

class CollapsibleSidebarUI(QWidget):
    """QtDesigner UI를 사용하는 접기/펼치기 가능한 사이드바"""
    
    tool_selected = pyqtSignal(str)  # 툴 선택 신호
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Sidebar()
        self.ui.setupUi(self)
        
        self.expanded_width = int(280 * 0.9)  # 90% = 252px
        self.collapsed_width = int(60 * 1.1)  # 110% = 66px
        self.is_expanded = True
        
        self.setup_ui()
        self.setup_tools()
        self.setup_connections()
        
    def setup_ui(self):
        """UI 추가 설정"""
        # UI 파일에서 초기 크기가 설정됨
        
        # 헤더 수정 (UKSDT + 서브타이틀)
        self.setup_header()
        
        # 하단 설정 영역 추가
        self.create_settings_area()
        
        # 애니메이션 그룹 설정
        self.animation_group = QParallelAnimationGroup()
        
        # 최소 너비 애니메이션
        self.min_width_animation = QPropertyAnimation(self, b"minimumWidth")
        self.min_width_animation.setDuration(300)
        self.min_width_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 최대 너비 애니메이션
        self.max_width_animation = QPropertyAnimation(self, b"maximumWidth")
        self.max_width_animation.setDuration(300)
        self.max_width_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 애니메이션 그룹에 추가
        self.animation_group.addAnimation(self.min_width_animation)
        self.animation_group.addAnimation(self.max_width_animation)
        
    def setup_header(self):
        """헤더 영역 수정 - UI 파일에서 이미 UKSDT와 서브타이틀이 설정됨"""
        # UI 파일에서 이미 설정되어 있으므로 추가 작업 불필요
        # 필요시 폰트나 스타일 조정만 수행
        pass
        
    def create_settings_area(self):
        """하단 설정 영역 연결 - UI 파일에서 이미 생성됨"""
        # UI 파일에서 이미 settings_btn이 생성되어 있으므로 연결만 수행
        self.ui.settings_btn.clicked.connect(self.show_settings)
            
    def show_settings(self):
        """설정 다이얼로그 표시"""
        settings_dialog = SettingsDialog(self)
        settings_dialog.settings_changed.connect(self.on_settings_changed)
        settings_dialog.exec_()
        
    def on_settings_changed(self):
        """설정 변경 시 호출"""
        print("설정이 변경되었습니다.")
        # 실제 구현에서는 여기서 설정을 적용
        
    def setup_tools(self):
        """툴 버튼들 설정"""
        tools = [
            ("Projects", "Projects", emoji_icon("📂")),
            ("Control_DR_Reviewer", "Control DR Reviewer", emoji_icon("🔍")),
            ("ECO_PPT_Maker", "ECO PPT Maker", emoji_icon("📊")),
            ("Externals", "Externals", emoji_icon("🔨"))
        ]
        
        self.tool_buttons = []
        
        # 스페이서 제거
        spacer_item = self.ui.tools_layout.takeAt(0)
        if spacer_item:
            spacer_item.widget().deleteLater() if spacer_item.widget() else None
        
        for tool_id, tool_name, icon in tools:
            btn = self.create_tool_button(tool_id, tool_name, icon)
            self.ui.tools_layout.addWidget(btn)
            self.tool_buttons.append(btn)
            
        # 스페이서 다시 추가
        self.ui.tools_layout.addStretch()
        
    def create_tool_button(self, tool_id, tool_name, icon):
        btn = QToolButton()
        btn.setCheckable(False)
        btn.setAutoRaise(False)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setText("     " + tool_name or "")
        btn.setIcon(icon)
        btn.setIconSize(QSize(32, 32))
        

        """툴 버튼 생성 - 텍스트 크기에 맞게 자동 조정 및 클리핑 방지"""
        
        
        # 버튼 크기 정책 - 수직은 최소 크기를 보장하되 확장 가능하게 설정
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # 최소 높이 설정으로 클리핑 방지 및 터치 친화성 확보
        btn.setMinimumHeight(40)  # 최소 40px 높이 보장
           
        # 클릭 이벤트
        btn.clicked.connect(lambda checked, tid=tool_id: self.tool_selected.emit(tid))

        return btn
        
    def setup_connections(self):
        """시그널 연결"""
        self.ui.toggle_btn.clicked.connect(self.toggle_sidebar)
        
    def toggle_sidebar(self):
        """사이드바 토글"""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
            
    def collapse(self):
        """사이드바 접기"""
        # 애니메이션 중이면 중단
        if self.animation_group.state() == QParallelAnimationGroup.Running:
            self.animation_group.stop()
        
        # 너비 애니메이션 설정
        self.min_width_animation.setStartValue(self.expanded_width)
        self.min_width_animation.setEndValue(self.collapsed_width)
        self.max_width_animation.setStartValue(self.expanded_width)
        self.max_width_animation.setEndValue(self.collapsed_width)
        
        # 애니메이션 시작
        self.animation_group.start()
        
        # UI 요소 변경
        self.ui.toggle_btn.setText("▶")
        self.ui.title_label.hide()
        
        # 서브타이틀 숨기기
        self.ui.subtitle_label.hide()
        
        # 텍스트 라벨 숨기기
        for btn in self.tool_buttons:
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        
        # 설정 버튼은 접혀도 보이도록 유지 (아이콘만)
        self.ui.settings_btn.setText("⚙")
            
        self.is_expanded = False
        
    def expand(self):
        """사이드바 펼치기"""
        # 애니메이션 중이면 중단
        if self.animation_group.state() == QParallelAnimationGroup.Running:
            self.animation_group.stop()
        
        # 너비 애니메이션 설정
        self.min_width_animation.setStartValue(self.collapsed_width)
        self.min_width_animation.setEndValue(self.expanded_width)
        self.max_width_animation.setStartValue(self.collapsed_width)
        self.max_width_animation.setEndValue(self.expanded_width)
        
        # 애니메이션 시작
        self.animation_group.start()
        
        # UI 요소 변경
        self.ui.toggle_btn.setText("◀")
        self.ui.title_label.show()
        
        # 서브타이틀 표시
        self.ui.subtitle_label.show()
        
        # 텍스트 라벨 표시
        for btn in self.tool_buttons:
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # 설정 버튼은 항상 아이콘으로 표시
        self.ui.settings_btn.setText("⚙")
            
        self.is_expanded = True