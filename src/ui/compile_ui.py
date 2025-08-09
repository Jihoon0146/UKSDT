#!/usr/bin/env python3
"""
QtDesigner UI 파일을 Python 파일로 컴파일하는 스크립트

새로운 디렉토리 구조:
- src/ui/*.ui (메인 UI 파일들)  
- src/ui/components/*.ui (컴포넌트 UI 파일들)
- src/ui_generated/*.py (생성된 Python 파일들)

사용법:
1. QtDesigner에서 UI 파일(.ui) 생성 후 해당 디렉토리에 저장
2. 이 스크립트 실행: python compile_ui.py  
3. src/ui_generated/ 디렉토리에 Python 파일(.py) 생성됨

UI 파일 변경 시 자동으로 재컴파일됩니다.
"""

import os
import sys
import subprocess
from pathlib import Path

def compile_ui_files():
    """UI 디렉토리의 모든 .ui 파일을 .py 파일로 컴파일"""
    
    # 경로 설정
    ui_dir = Path(__file__).parent  # src/ui
    src_dir = ui_dir.parent         # src  
    generated_dir = src_dir / "ui_generated"  # src/ui_generated
    
    # generated 디렉토리가 없으면 생성
    generated_dir.mkdir(exist_ok=True)
    
    # .ui 파일들 찾기 (루트 UI 디렉토리 + components 디렉토리)
    ui_files = []
    
    # 메인 UI 파일들 (src/ui/*.ui)
    ui_files.extend(ui_dir.glob("*.ui"))
    
    # 컴포넌트 UI 파일들 (src/ui/components/*.ui)  
    components_dir = ui_dir / "components"
    if components_dir.exists():
        ui_files.extend(components_dir.glob("*.ui"))
    
    if not ui_files:
        print("UI 파일(.ui)이 없습니다.")
        print("QtDesigner로 UI 파일을 생성한 후 해당 디렉토리에 저장하세요.")
        return
    
    compiled_count = 0
    
    for ui_file in ui_files:
        # 출력 파일명 생성 (ui_main_window.py 형태)
        py_filename = f"ui_{ui_file.stem}.py"
        py_file = generated_dir / py_filename
        
        # UI 파일이 Python 파일보다 새로운 경우에만 컴파일
        if not py_file.exists() or ui_file.stat().st_mtime > py_file.stat().st_mtime:
            try:
                # pyuic5 명령어로 컴파일
                cmd = [
                    sys.executable, "-m", "PyQt5.uic.pyuic",
                    str(ui_file),
                    "-o", str(py_file)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[OK] {ui_file.relative_to(src_dir)} -> ui_generated/{py_filename}")
                    compiled_count += 1
                else:
                    print(f"[ERROR] {ui_file.name} 컴파일 실패:")
                    print(result.stderr)
                    
            except FileNotFoundError:
                print("PyQt5.uic.pyuic를 찾을 수 없습니다.")
                print("PyQt5가 제대로 설치되었는지 확인하세요.")
                return
                
        else:
            print(f"- {ui_file.relative_to(src_dir)} (변경사항 없음)")
    
    if compiled_count > 0:
        print(f"\n{compiled_count}개의 UI 파일이 컴파일되었습니다.")
        
        # __init__.py 파일 자동 업데이트
        update_init_file(generated_dir, ui_files)
    else:
        print("\n컴파일할 UI 파일이 없습니다.")

def update_init_file(generated_dir, ui_files):
    """generated/__init__.py 파일을 자동으로 업데이트"""
    init_file = generated_dir / "__init__.py"
    
    imports = []
    for ui_file in ui_files:
        module_name = f"ui_{ui_file.stem}"
        class_name = f"Ui_{ui_file.stem.title().replace('_', '')}"
        imports.append(f"from .{module_name} import {class_name}")
    
    content = "# Generated UI files from QtDesigner\n"
    content += "# This file is auto-generated. Do not edit manually.\n\n"
    content += "\n".join(sorted(imports)) + "\n"
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] ui_generated/__init__.py 업데이트됨")

def watch_ui_files():
    """UI 파일 변경을 감지하여 자동 컴파일 (개발용)"""
    try:
        import time
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class UIFileHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if not event.is_directory and event.src_path.endswith('.ui'):
                    print(f"\n{event.src_path} 파일이 변경되었습니다.")
                    compile_ui_files()
        
        ui_dir = Path(__file__).parent
        observer = Observer()
        observer.schedule(UIFileHandler(), str(ui_dir), recursive=True)
        observer.start()
        
        print("UI 파일 변경 감지 시작... (Ctrl+C로 종료)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    except ImportError:
        print("watchdog 패키지가 설치되지 않았습니다.")
        print("자동 감지 기능을 사용하려면 'pip install watchdog'를 실행하세요.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        watch_ui_files()
    else:
        compile_ui_files()