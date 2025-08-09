# Resources package for UKSDT application
# This package contains all external resources like images, fonts, styles, etc.

import os
from pathlib import Path

# 리소스 디렉토리 경로
RESOURCES_DIR = Path(__file__).parent

# 서브 디렉토리 경로들
IMAGES_DIR = RESOURCES_DIR / "images"
ICONS_DIR = RESOURCES_DIR / "icons"
FONTS_DIR = RESOURCES_DIR / "fonts"
STYLES_DIR = RESOURCES_DIR / "styles"
TEMPLATES_DIR = RESOURCES_DIR / "templates"
DATA_DIR = RESOURCES_DIR / "data"
SOUNDS_DIR = RESOURCES_DIR / "sounds"

# 이미지 서브 카테고리
LOGOS_DIR = IMAGES_DIR / "logos"
BACKGROUNDS_DIR = IMAGES_DIR / "backgrounds"
UI_ELEMENTS_DIR = IMAGES_DIR / "ui_elements"
SCREENSHOTS_DIR = IMAGES_DIR / "screenshots"

# 아이콘 서브 카테고리
TOOLBAR_ICONS_DIR = ICONS_DIR / "toolbar"
MENU_ICONS_DIR = ICONS_DIR / "menu"
STATUS_ICONS_DIR = ICONS_DIR / "status"
SYSTEM_ICONS_DIR = ICONS_DIR / "system"

# 템플릿 서브 카테고리
REPORTS_TEMPLATES_DIR = TEMPLATES_DIR / "reports"
EXCEL_TEMPLATES_DIR = TEMPLATES_DIR / "excel"
PDF_TEMPLATES_DIR = TEMPLATES_DIR / "pdf"

def get_resource_path(resource_type: str, filename: str) -> Path:
    """
    리소스 파일의 전체 경로를 반환합니다.
    
    Args:
        resource_type: 리소스 타입 ('images', 'icons', 'fonts', etc.)
        filename: 파일명
    
    Returns:
        Path: 리소스 파일의 전체 경로
    """
    resource_dirs = {
        'images': IMAGES_DIR,
        'icons': ICONS_DIR,
        'fonts': FONTS_DIR,
        'styles': STYLES_DIR,
        'templates': TEMPLATES_DIR,
        'data': DATA_DIR,
        'sounds': SOUNDS_DIR,
        # 이미지 서브 카테고리
        'logos': LOGOS_DIR,
        'backgrounds': BACKGROUNDS_DIR,
        'ui_elements': UI_ELEMENTS_DIR,
        'screenshots': SCREENSHOTS_DIR,
        # 아이콘 서브 카테고리
        'toolbar_icons': TOOLBAR_ICONS_DIR,
        'menu_icons': MENU_ICONS_DIR,
        'status_icons': STATUS_ICONS_DIR,
        'system_icons': SYSTEM_ICONS_DIR,
        # 템플릿 서브 카테고리
        'reports_templates': REPORTS_TEMPLATES_DIR,
        'excel_templates': EXCEL_TEMPLATES_DIR,
        'pdf_templates': PDF_TEMPLATES_DIR,
    }
    
    if resource_type in resource_dirs:
        return resource_dirs[resource_type] / filename
    else:
        raise ValueError(f"Unknown resource type: {resource_type}")

def resource_exists(resource_type: str, filename: str) -> bool:
    """
    리소스 파일이 존재하는지 확인합니다.
    
    Args:
        resource_type: 리소스 타입
        filename: 파일명
    
    Returns:
        bool: 파일 존재 여부
    """
    try:
        path = get_resource_path(resource_type, filename)
        return path.exists()
    except ValueError:
        return False