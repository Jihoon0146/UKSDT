"""
리소스 사용 예시 코드

이 파일은 resources 패키지와 ResourceLoader 유틸리티를 사용하는 방법을 보여줍니다.
실제 프로젝트에서 이 예시들을 참고하여 리소스를 로드하고 사용하세요.
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# 상위 디렉토리를 Python 경로에 추가 (예시 실행을 위해)
sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.resource_loader import ResourceLoader, load_image, load_icon, load_style, apply_style

class ResourceExampleWindow(QMainWindow):
    """리소스 사용 예시를 보여주는 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resource Loading Examples")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_ui()
        self.load_resources()
    
    def setup_ui(self):
        """UI 구성"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 로고 표시용 라벨
        self.logo_label = QLabel("로고가 여기에 표시됩니다")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("border: 2px dashed #ccc; padding: 20px;")
        layout.addWidget(self.logo_label)
        
        # 아이콘이 있는 버튼
        self.icon_button = QPushButton("아이콘 버튼")
        layout.addWidget(self.icon_button)
        
        # 배경 이미지가 있는 위젯
        self.bg_widget = QWidget()
        self.bg_widget.setFixedHeight(200)
        self.bg_widget.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.bg_widget)
        
        # 폰트 예시 라벨
        self.font_label = QLabel("커스텀 폰트 예시")
        self.font_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.font_label)
        
        # 스타일 적용 버튼
        self.style_button = QPushButton("다크 테마 적용")
        self.style_button.clicked.connect(self.apply_dark_theme)
        layout.addWidget(self.style_button)
        
        # 캐시 정보 버튼
        self.cache_button = QPushButton("캐시 정보 보기")
        self.cache_button.clicked.connect(self.show_cache_info)
        layout.addWidget(self.cache_button)
    
    def load_resources(self):
        """리소스 로드 예시"""
        
        # 1. 이미지 로드 예시
        # 실제 파일이 있다면 이렇게 사용:
        # logo_pixmap = load_image('logos', 'company_logo.png', size=(200, 100))
        # if logo_pixmap:
        #     self.logo_label.setPixmap(logo_pixmap)
        
        # 2. 아이콘 로드 예시
        # icon = load_icon('toolbar_icons', 'save.svg', size=(24, 24))
        # if icon:
        #     self.icon_button.setIcon(icon)
        
        # 3. 폰트 로드 예시
        # custom_font = ResourceLoader.load_font('custom_font.ttf', 16)
        # if custom_font:
        #     self.font_label.setFont(custom_font)
        
        # 4. 배경 이미지 설정 예시
        # bg_image_path = ResourceLoader.get_resource_path('backgrounds', 'pattern.png')
        # if bg_image_path and bg_image_path.exists():
        #     self.bg_widget.setStyleSheet(f"""
        #         background-image: url({bg_image_path});
        #         background-repeat: repeat;
        #         border: 1px solid #ccc;
        #     """)
        
        print("리소스 로드 예시가 실행되었습니다.")
        print("실제 리소스 파일들을 추가하면 위의 주석 처리된 코드들을 활용할 수 있습니다.")
    
    def apply_dark_theme(self):
        """다크 테마 적용 예시"""
        # 실제 스타일시트 파일이 있다면:
        # apply_style('dark_theme.qss')
        
        # 임시 다크 스타일 적용
        dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLabel {
            background-color: transparent;
            color: #ffffff;
            border: 2px dashed #555;
        }
        QPushButton {
            background-color: #404040;
            color: #ffffff;
            border: 2px solid #606060;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #353535;
        }
        """
        self.setStyleSheet(dark_style)
        print("다크 테마가 적용되었습니다.")
    
    def show_cache_info(self):
        """캐시 정보 표시"""
        cache_info = ResourceLoader.get_cache_info()
        print("\n=== 리소스 캐시 정보 ===")
        print(f"로드된 폰트 수: {cache_info['loaded_fonts']}")
        print(f"로드된 스타일시트 수: {cache_info['loaded_stylesheets']}")
        
        if cache_info['font_list']:
            print(f"폰트 목록: {', '.join(cache_info['font_list'])}")
        
        if cache_info['stylesheet_list']:
            print(f"스타일시트 목록: {', '.join(cache_info['stylesheet_list'])}")

def main():
    """예시 애플리케이션 실행"""
    app = QApplication(sys.argv)
    
    # 기본 스타일 설정
    app.setStyle('Fusion')  # 모던한 스타일
    
    window = ResourceExampleWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    print("리소스 로딩 예시 프로그램")
    print("실제 리소스 파일들을 resources/ 디렉토리에 추가한 후 코드의 주석을 해제하여 사용하세요.")
    print("-" * 60)
    
    main()