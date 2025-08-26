from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, QSplitter)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont

from .main_window_ui import Ui_MainWindow
from .components.welcome_page_ui import Ui_WelcomePage
from .components.sidebar import CollapsibleSidebarUI
from .components.custom_tab_widget import CustomTabWidget

class MainWindowUI(QMainWindow):
    """QtDesigner UI를 사용하는 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # UI 파일에서 최소 크기가 설정됨
        
        # 열린 탭들을 추적
        self.open_tabs = {}
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """UI 추가 설정"""
        # Splitter 추가 및 사이드바 설정
        self.setup_splitter()
        
        # 기존 탭 위젯을 커스텀 탭 위젯으로 교체
        self.setup_custom_tabs()
        
        # 웰컴 탭 추가 (기본)
        welcome_page = self.create_welcome_page()
        self.ui.tool_tabs.addTab(welcome_page, "홈")
        
        # 탭 닫기 비활성화 (첫 번째 홈 탭)
        self.ui.tool_tabs.tabBar().setTabButton(0, self.ui.tool_tabs.tabBar().RightSide, None)
        
        # 홈 탭 가시성 제어를 위한 초기 설정
        self.home_tab_index = 0
        
    def setup_splitter(self):
        """Splitter 설정 - UI 파일에서 이미 splitter가 생성됨"""
        # UI 파일에서 생성된 splitter 사용
        self.splitter = self.ui.splitter
        
        # 기존 위젯들을 임시로 보관
        content_area = self.ui.content_area
        
        # splitter에서 모든 위젯 제거
        while self.splitter.count() > 0:
            widget = self.splitter.widget(0)
            widget.setParent(None)
        
        # sidebar_placeholder 삭제
        self.ui.sidebar_placeholder.deleteLater()
        
        # 올바른 순서로 위젯들 추가
        # 1. 사이드바 (왼쪽, index 0)
        self.sidebar = CollapsibleSidebarUI()
        self.splitter.addWidget(self.sidebar)
        
        # 2. 콘텐츠 영역 (오른쪽, index 1)
        self.splitter.addWidget(content_area)
        
        # 스플리터 비율 설정 (사이드바:구분선:콘텐츠 = 280:1:1640)
        self.splitter.setSizes([280, 1640])
        self.splitter.setCollapsible(0, False)  # 사이드바 완전 축소 방지
        
    def setup_custom_tabs(self):
        """커스텀 탭 위젯 설정"""
        content_layout = self.ui.content_layout
        content_layout.removeWidget(self.ui.tool_tabs)
        self.ui.tool_tabs.deleteLater()
        
        # 새로운 커스텀 탭 위젯 생성
        self.ui.tool_tabs = CustomTabWidget()
        self.ui.tool_tabs.setTabsClosable(True)
        self.ui.tool_tabs.setMovable(True)
        content_layout.addWidget(self.ui.tool_tabs)
        
    def create_welcome_page(self):
        """웰컴 페이지 생성"""
        welcome_widget = QWidget()
        welcome_ui = Ui_WelcomePage()
        welcome_ui.setupUi(welcome_widget)
        
        # 웰컴 페이지 텍스트 업데이트
        welcome_ui.welcome_subtitle.setText("왼쪽 사이드바에서 원하는 도구를 선택하여 시작하세요.")
        
        return welcome_widget
        
    def create_tool_widget(self, tool_id, tool_name):
        """툴 위젯 생성"""
        if tool_id == "Control_DR_Reviewer":
            from tools.control_dr_reviewer import ControlDRReviewerWidget
            return ControlDRReviewerWidget()
        if tool_id == "Externals":
            from tools.externals import ExternalsWidget
            return ExternalsWidget()
        if tool_id == "Projects":
            from tools.projects import ProjectsWidget
            return ProjectsWidget()
        else:
            # 기본 임시 위젯
            tool_widget = QWidget()
            layout = QVBoxLayout(tool_widget)
            layout.setAlignment(Qt.AlignCenter)
            
            # 툴 제목
            title_label = QLabel(f"{tool_name}")
            title_label.setFont(QFont("Arial", 24, QFont.Bold))
            title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)
            
            # 설명
            desc_label = QLabel("이 도구는 현재 개발 중입니다.")
            desc_label.setFont(QFont("Arial", 14))
            desc_label.setStyleSheet("color: #7f8c8d;")
            desc_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(desc_label)
            
            return tool_widget
        
    def setup_connections(self):
        """시그널 연결"""
        self.sidebar.tool_selected.connect(self.on_tool_selected)
        self.ui.tool_tabs.tabCloseRequested.connect(self.close_tab)
        
    def on_tool_selected(self, tool_id):
        """툴 선택 시 호출"""
        # 툴 이름 매핑
        tool_names = {
            "Projects": "Projects",
            "Control_DR_Reviewer": "Control DR Reviewer",
            "ECO_PPT_Maker": "ECO PPT Maker",
            "Externals": "Externals"
        }
        
        tool_name = tool_names.get(tool_id, tool_id)
        
        # 이미 열린 탭이 있는지 확인
        if tool_id in self.open_tabs:
            # 기존 탭으로 전환
            tab_index = self.open_tabs[tool_id]
            self.ui.tool_tabs.setCurrentIndex(tab_index)
        else:
            # 새 탭 생성
            tool_widget = self.create_tool_widget(tool_id, tool_name)
            tab_index = self.ui.tool_tabs.addTab(tool_widget, tool_name)
            self.open_tabs[tool_id] = tab_index
            self.ui.tool_tabs.setCurrentIndex(tab_index)
            
            # 홈 탭 가시성 업데이트
            self.update_home_tab_visibility()
        
        print(f"Selected tool: {tool_id}")
        
    def close_tab(self, index):
        """탭 닫기"""
        if index == 0:  # 홈 탭은 닫을 수 없음
            return
            
        # open_tabs 딕셔너리에서 해당 탭 제거
        tab_to_remove = None
        for tool_id, tab_index in self.open_tabs.items():
            if tab_index == index:
                tab_to_remove = tool_id
                break
                
        if tab_to_remove:
            del self.open_tabs[tab_to_remove]
            
        # 나머지 탭들의 인덱스 업데이트
        for tool_id in self.open_tabs:
            if self.open_tabs[tool_id] > index:
                self.open_tabs[tool_id] -= 1
        
        # 탭 제거
        self.ui.tool_tabs.removeTab(index)
        
        # 홈 탭 가시성 업데이트
        self.update_home_tab_visibility()
        
    def update_home_tab_visibility(self):
        """홈 탭 가시성 업데이트 - 다른 탭이 있으면 홈 탭 숨김, 없으면 표시"""
        tab_count = self.ui.tool_tabs.count()
        
        if tab_count > 1:
            # 다른 탭이 있으면 홈 탭 숨기기
            if self.ui.tool_tabs.tabBar().tabButton(self.home_tab_index, self.ui.tool_tabs.tabBar().LeftSide) is None:
                # 홈 탭이 보이는 상태이면 숨기기
                self.ui.tool_tabs.tabBar().setTabVisible(self.home_tab_index, False)
        else:
            # 홈 탭만 남은 경우 홈 탭 보이기
            self.ui.tool_tabs.tabBar().setTabVisible(self.home_tab_index, True)
            # 홈 탭으로 자동 전환
            self.ui.tool_tabs.setCurrentIndex(self.home_tab_index)
        
    def resizeEvent(self, event):
        """창 크기 변경 이벤트"""
        super().resizeEvent(event)
        # 반응형 레이아웃 조정이 필요한 경우 여기에 구현