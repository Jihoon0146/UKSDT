# QtDesigner UI 가이드

## 디렉토리 구조

```
src/
├── ui/                     # QtDesigner UI 파일들
│   ├── main_window.ui     # 메인 윈도우 UI
│   ├── sidebar.ui         # 사이드바 UI
│   ├── welcome_page.ui    # 웰컴 페이지 UI
│   ├── compile_ui.py      # UI 컴파일 스크립트
│   └── generated/         # 생성된 Python UI 파일들
│       ├── __init__.py
│       ├── ui_main_window.py
│       ├── ui_sidebar.py
│       └── ui_welcome_page.py
├── core/
│   ├── main_window_ui.py  # UI를 사용하는 메인 윈도우
│   └── sidebar_ui.py      # UI를 사용하는 사이드바
└── ...
```

## QtDesigner 사용 방법

### 1. UI 파일 편집

1. QtDesigner 실행:
   ```bash
   # Windows - 배치 파일 사용 (권장)
   run_designer.bat
   
   # 또는 직접 실행
   source venv/Scripts/activate
   pyqt5-tools designer
   ```

2. `src/ui/` 디렉토리의 `.ui` 파일을 열어서 편집

3. 저장 후 다음 단계로 컴파일

### 2. UI 파일 컴파일

UI 파일을 편집한 후 Python 파일로 컴파일해야 합니다:

```bash
cd src/ui
python compile_ui.py
```

또는 자동 감지 모드 (개발 중 편리):
```bash
cd src/ui
python compile_ui.py watch
```

### 3. 컴파일 결과

- `ui/generated/` 디렉토리에 Python 파일들이 생성됩니다
- `ui_main_window.py`, `ui_sidebar.py` 등
- `__init__.py`도 자동으로 업데이트됩니다

### 4. 코드에서 사용

```python
from ui.generated import Ui_MainWindow

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # UI 요소 접근
        self.ui.some_button.clicked.connect(self.on_button_click)
```

## 주요 UI 파일 설명

### main_window.ui
- 메인 윈도우의 전체 레이아웃
- 사이드바 placeholder와 콘텐츠 영역 포함
- 헤더 영역과 스택 위젯

### sidebar.ui
- 왼쪽 사이드바 레이아웃
- 헤더, 토글 버튼, 스크롤 영역
- 툴 버튼들이 동적으로 추가됨

### welcome_page.ui
- 웰컴 페이지 레이아웃
- 타이틀, 서브타이틀, 기능 카드들

## 개발 워크플로우

1. **UI 수정이 필요한 경우:**
   - QtDesigner에서 `.ui` 파일 편집
   - `compile_ui.py` 실행하여 Python 파일 생성
   - 코드에서 UI 요소에 접근하여 로직 구현

2. **새로운 UI 추가:**
   - QtDesigner에서 새 `.ui` 파일 생성
   - `ui/` 디렉토리에 저장
   - `compile_ui.py` 실행
   - Python 코드에서 UI 클래스 import하여 사용

3. **자동화:**
   - `compile_ui.py watch` 명령으로 UI 파일 변경 시 자동 컴파일
   - 개발 중에는 이 모드를 켜두면 편리함

## 주의사항

- `ui/generated/` 디렉토리의 파일들은 자동 생성되므로 직접 편집하지 마세요
- UI 파일을 수정한 후 반드시 컴파일해야 변경사항이 반영됩니다
- QtDesigner에서 스타일시트 편집 가능하지만, 복잡한 스타일은 Python 코드에서 처리하는 것이 좋습니다