# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Python project configured for development with VS Code. The project follows a standard Python structure:

- `src/` - Main source code directory, with `src/main.py` as the main application entry point
- `tests/` - Test directory for pytest tests
- `venv/` - Virtual environment (excluded from version control)

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Install dependencies (when requirements-dev.txt exists)
./venv/bin/pip install -r requirements-dev.txt
```

### Running the Application
```bash
# Run main application
python src/main.py
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run tests for a specific file
python -m pytest path/to/test_file.py -v
```

### Code Quality
```bash
# Format code (black is configured)
black src/ tests/

# Lint code (pylint is configured)
pylint src/
```

## Development Configuration

- **Python Path**: `src/` directory is included in Python path
- **Testing Framework**: pytest
- **Code Formatter**: black
- **Linter**: pylint
- **Environment Variables**: Loaded from `.env` file in workspace root

The VS Code configuration includes debug configurations for running the main application, current file, and tests.

## UI Development Notes

### Sidebar QPushButton Style Issue (2025-08-05)

**Problem**: Sidebar tool buttons lack visible borders and hover effects
**Root Cause**: Empty styleSheet properties in sidebar.ui override Breeze theme styles

**Files to be modified for fix**:
- `src/ui/sidebar.ui` - Remove empty styleSheet properties from QPushButtons

**Original state before fix**:
- Lines 139, 331 in sidebar.ui contain `<string notr="true"></string>` for styleSheet properties
- These empty stylesheets prevent Breeze theme QPushButton styles from applying
- Breeze theme defines proper borders and hover effects but gets overridden

**Expected after fix**:
- QPushButton borders: 0.04em solid #76797c (default), 0.04em solid #3daee9 (hover)  
- Background changes on hover from #31363b to highlighted state

**Rollback instructions**: Restore empty styleSheet properties if fix causes issues

### PyQt Widget Border Visibility Issue (2025-08-05)

**Root Cause Analysis**: 
- Breeze 다크 테마의 색상 대비 부족으로 인한 테두리 가시성 문제
- 배경색 `#31363b` (RGB: 49,54,59, 밝기: 53.1)
- 테두리색 `#76797c` (RGB: 118,121,124, 밝기: 120.4)  
- 대비 비율: 2.79:1 (WCAG 기준 미달 - 최소 3.0:1 필요)

**해결 방안**: 테두리 색상을 더 밝게 조정하여 가시성 향상
- 기존: `#76797c` → 개선: `#9CA0A4` (더 밝은 회색)
- 새로운 대비 비율: 4.2:1 (WCAG AA 기준 만족)

## Qt Designer 워크플로우

### UI 파일 수정 후 반영하는 방법

1. **Qt Designer로 .ui 파일 수정**
   ```bash
   # Qt Designer 실행 (설치되어 있는 경우)
   designer.exe src/ui/main_window.ui
   ```

2. **UI 파일 컴파일**
   ```bash
   cd src/ui
   python compile_ui.py
   ```

3. **생성되는 파일들**
   - `src/ui/generated/ui_main_window.py` - 메인 윈도우 UI 클래스
   - `src/ui/generated/ui_sidebar.py` - 사이드바 UI 클래스  
   - `src/ui/generated/ui_welcome_page.py` - 웰컴 페이지 UI 클래스

### 현재 UI 구조
- **정적 설정**: UI 파일에서 관리 (크기, 레이아웃, 기본 속성)
- **동적 로직**: Python 코드에서 관리 (애니메이션, 이벤트, 커스텀 위젯)

### 수정 가능한 부분 (UI 파일)
- 위젯 크기 및 위치
- 레이아웃 마진, 스페이싱
- 폰트, 색상 등 스타일 속성
- 기본 텍스트 및 라벨

### 수정 불가능한 부분 (Python 코드 필요)
- 동적 위젯 생성
- 애니메이션 및 특수 효과
- 커스텀 위젯 클래스
- 이벤트 처리 로직