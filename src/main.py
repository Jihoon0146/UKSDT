import sys
import os
import subprocess
import locale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QFontDatabase, QFont

def apply_gtronick_theme(app):
    """GTRONICK QSS 테마 적용"""
    try:
        # QSS 파일 경로
        qss_path = os.path.join(os.path.dirname(__file__), "resources", "styles", "ElegantDark.qss")
        
        # QSS 파일 읽기
        with open(qss_path, 'r', encoding='utf-8') as f:
            stylesheet = f.read()
        
        # 애플리케이션에 스타일시트 적용
        app.setStyleSheet(stylesheet)
        print("GTRONICK 테마 적용 완료")
        return True
        
    except FileNotFoundError:
        print(f"QSS 파일을 찾을 수 없습니다: {qss_path}")
        print("기본 테마를 사용합니다.")
        return False
    except Exception as e:
        print(f"GTRONICK 테마 적용 중 오류: {e}")
        print("기본 테마를 사용합니다.")
        return False

def setup_custom_font(app):
    """LGEIHeadlineTTF 커스텀 폰트 설정"""
    try:
        # 폰트 파일 경로
        font_path = os.path.join(os.path.dirname(__file__), "resources", "fonts", "LGEITextTTF-Regular.ttf")
        
        # 폰트 파일 존재 확인
        if not os.path.exists(font_path):
            print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
            return False
        
        # 폰트 데이터베이스에 폰트 추가
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        if font_id == -1:
            print("폰트 로드에 실패했습니다.")
            return False
        
        # 폰트 패밀리명 가져오기
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if not font_families:
            print("폰트 패밀리를 찾을 수 없습니다.")
            return False
        
        font_family = font_families[0]
        print(f"폰트 로드 완료: {font_family}")
        
        # 애플리케이션 기본 폰트 설정
        default_font = QFont(font_family, 10)  # 기본 크기 10pt
        app.setFont(default_font)
        
        print("애플리케이션 기본 폰트가 LGEIHeadlineTTF-Regular로 설정되었습니다.")
        return True
        
    except Exception as e:
        print(f"폰트 설정 중 오류: {e}")
        return False

def compile_ui_files():
    """UI 파일 컴파일"""
    try:
        # compile_ui.py 경로
        compile_script_path = os.path.join(os.path.dirname(__file__), "ui", "compile_ui.py")
        
        if not os.path.exists(compile_script_path):
            print(f"compile_ui.py 파일을 찾을 수 없습니다: {compile_script_path}")
            return False
        
        # UI 파일 컴파일 실행 (시스템 로케일 인코딩 사용)
        system_encoding = locale.getpreferredencoding()
        
        # 환경변수 설정 (UTF-8 출력 강제)
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run([sys.executable, compile_script_path], 
                              cwd=os.path.join(os.path.dirname(__file__), "ui"),
                              capture_output=True, text=True, 
                              encoding='utf-8', errors='replace', env=env)
        
        if result.returncode == 0:
            print("UI 파일 컴파일 완료")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("UI 파일 컴파일 실패")
            if result.stderr:
                print(f"오류: {result.stderr}")
            return False
            
    except UnicodeDecodeError as e:
        print(f"UI 파일 컴파일 중 인코딩 오류 발생: {e}")
        print("UI 파일 컴파일을 건너뜁니다.")
        return False
            
    except Exception as e:
        print(f"UI 파일 컴파일 중 오류: {e}")
        return False

def main():
    """UKSDT 통합 툴 앱 실행"""
    
	# UI 파일 컴파일
    print("UI 파일 컴파일 중...")
    compile_ui_files()
    
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
    
    # GTRONICK QSS 테마 적용
    apply_gtronick_theme(app)
    

     
    # 현재 디렉토리를 Python 경로에 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from core.main_window_ui import MainWindowUI as MainWindow
    
    # 메인 윈도우 생성 및 표시
    main_window = MainWindow()
    main_window.show()
    
    # 이벤트 루프 시작
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()