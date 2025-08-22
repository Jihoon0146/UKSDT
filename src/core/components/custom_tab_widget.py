from PyQt5.QtWidgets import QTabWidget, QTabBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

class CustomTabBar(QTabBar):
    """탭 라벨 크기를 텍스트 길이에 맞게 조정하는 커스텀 탭바"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_tab_width = 80   # 최소 탭 너비
        self.max_tab_width = 250  # 최대 탭 너비
        
    def tabSizeHint(self, index):
        """탭 크기 힌트 반환 - 텍스트 길이에 맞게 조정"""
        size = super().tabSizeHint(index)
        
        # 탭 텍스트 가져오기
        tab_text = self.tabText(index)
        if not tab_text:
            return size
            
        # 폰트 메트릭 계산
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.horizontalAdvance(tab_text)
        
        # 패딩 추가 (좌우 16px씩 + 닫기 버튼 공간 20px)
        total_width = text_width + 52
        
        # 최소/최대 너비 적용
        if total_width < self.min_tab_width:
            size.setWidth(self.min_tab_width)
        elif total_width > self.max_tab_width:
            size.setWidth(self.max_tab_width)
        else:
            size.setWidth(total_width)
            
        return size

class CustomTabWidget(QTabWidget):
    """탭 라벨 크기를 텍스트 길이에 맞게 조정하는 커스텀 탭 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 커스텀 탭바 설정
        self.custom_tab_bar = CustomTabBar()
        self.setTabBar(self.custom_tab_bar)
        
        # 기본 시스템 스타일 사용
        
    def addTab(self, widget, label):
        """탭 추가 - 전체 라벨 표시 (잘림 없음)"""
        # 전체 라벨 표시
        index = super().addTab(widget, label)
        
        # 긴 텍스트의 경우 툴팁으로도 설정
        if len(label) > 15:
            self.setTabToolTip(index, label)
        
        return index
        
    def setTabText(self, index, text):
        """탭 텍스트 설정 - 전체 텍스트 표시 (잘림 없음)"""
        # 전체 텍스트 표시
        super().setTabText(index, text)
        
        # 긴 텍스트의 경우 툴팁으로도 설정
        if len(text) > 15:
            self.setTabToolTip(index, text)