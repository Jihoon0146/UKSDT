import sys
import os
import subprocess
import locale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QFontDatabase, QFont
import qdarkstyle

def apply_qdark_theme(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

def apply_gtronick_theme(app):
    """GTRONICK QSS 테마 적용"""
    try:
        # QSS 파일 경로
        qss_path = os.path.join(os.environ.get("UKSDT_RESOURCE_PATH",""), "styles", "ElegantDark.qss")
        
        # QSS 파일 읽기
        with open(qss_path, 'r', encoding='utf-8') as f:
            stylesheet = f.read()
        
        # 애플리케이션에 스타일시트 적용
        app.setStyleSheet(stylesheet)
        print("\tTheme : GTRONICK --- Complete.")
        return True
        
    except FileNotFoundError:
        print(f"\tTheme : GTRONICK --- Fail. Can not find QSS, {qss_path}")
        print("\tTheme : Use default theme.")
        return False
    except Exception as e:
        print(f"\tTheme : GTRONICK --- Fail. Can not adapt. {e}")
        print("\tTheme : Use default theme.")
        return False
def setup_custom_theme(app):
    #apply_gtronick_theme(app)
    apply_qdark_theme(app)




def setup_custom_font(app):
    try:
        # 폰트 파일 경로
        font_path = os.path.join(os.environ.get("UKSDT_RESOURCE_PATH",""), "fonts", "LGEITextTTF-Regular.ttf")
        
        # 폰트 파일 존재 확인
        if not os.path.exists(font_path):
            print(f"\tFont : LG Font --- Fail. Can not find TTF, {font_path}")
            return False
        
        # 폰트 데이터베이스에 폰트 추가
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        if font_id == -1:
            print("\tFont : LG Font --- Fail. Can not load.")
            return False
        
        # 폰트 패밀리명 가져오기
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if not font_families:
            print("\tFont : LG Font --- Fail. Can not find font family.")
            return False
        
        font_family = font_families[0]
        print(f"\tFont : LG Font --- Complete. {font_family}")
        
        # 애플리케이션 기본 폰트 설정
        default_font = QFont(font_family, 10)  # 기본 크기 10pt
        app.setFont(default_font)
        
        return True
        
    except Exception as e:
        print(f"\tFont : Can not be setting. {e}")
        return False

def main():
    """UKSDT 통합 툴 앱 실행"""
   
    # 고해상도 디스플레이 지원 (QApplication 생성 전에 설정)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # QApplication 생성
    app = QApplication(sys.argv)
    
    # 애플리케이션 기본 설정
    app.setApplicationName("UKSDT 통합 툴")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("UKSDT")
    
    # 커스텀 폰트 설정 (테마 적용 전에)
    setup_custom_font(app)
    
    setup_custom_theme(app)
     
    # 현재 디렉토리를 Python 경로에 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from core.main_window import MainWindowUI as MainWindow
    
    # 메인 윈도우 생성 및 표시
    main_window = MainWindow()
    main_window.show()
    
    # 이벤트 루프 시작
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()