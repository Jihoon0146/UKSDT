"""
리소스 로딩 유틸리티

이 모듈은 애플리케이션에서 사용하는 다양한 리소스(이미지, 폰트, 스타일시트 등)를
쉽게 로드하고 관리하기 위한 유틸리티 함수들을 제공합니다.
"""

import os
from pathlib import Path
from typing import Optional, Union
from PyQt5.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from resources import get_resource_path, resource_exists

class ResourceLoader:
    """리소스 로딩을 위한 유틸리티 클래스"""
    
    _loaded_fonts = {}  # 로드된 폰트 캐시
    _loaded_stylesheets = {}  # 로드된 스타일시트 캐시
    
    @classmethod
    def load_pixmap(cls, resource_type: str, filename: str, 
                   size: Optional[tuple] = None) -> Optional[QPixmap]:
        """
        이미지를 QPixmap으로 로드합니다.
        
        Args:
            resource_type: 리소스 타입 ('images', 'logos', 'icons' 등)
            filename: 파일명
            size: 선택적 크기 조정 (width, height)
        
        Returns:
            QPixmap 또는 None (파일이 없는 경우)
        """
        if not resource_exists(resource_type, filename):
            print(f"Warning: Resource not found: {resource_type}/{filename}")
            return None
        
        path = get_resource_path(resource_type, filename)
        pixmap = QPixmap(str(path))
        
        if pixmap.isNull():
            print(f"Warning: Failed to load pixmap: {path}")
            return None
        
        if size:
            width, height = size
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, 
                                 Qt.SmoothTransformation)
        
        return pixmap
    
    @classmethod
    def load_icon(cls, resource_type: str, filename: str,
                  size: Optional[tuple] = None) -> Optional[QIcon]:
        """
        이미지를 QIcon으로 로드합니다.
        
        Args:
            resource_type: 리소스 타입
            filename: 파일명
            size: 선택적 크기 조정 (width, height)
        
        Returns:
            QIcon 또는 None
        """
        pixmap = cls.load_pixmap(resource_type, filename, size)
        if pixmap:
            return QIcon(pixmap)
        return None
    
    @classmethod
    def load_stylesheet(cls, filename: str, cache: bool = True) -> Optional[str]:
        """
        스타일시트 파일을 로드합니다.
        
        Args:
            filename: 스타일시트 파일명
            cache: 캐시 사용 여부
        
        Returns:
            스타일시트 문자열 또는 None
        """
        if cache and filename in cls._loaded_stylesheets:
            return cls._loaded_stylesheets[filename]
        
        if not resource_exists('styles', filename):
            print(f"Warning: Stylesheet not found: {filename}")
            return None
        
        path = get_resource_path('styles', filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
            
            if cache:
                cls._loaded_stylesheets[filename] = stylesheet
            
            return stylesheet
        except Exception as e:
            print(f"Error loading stylesheet {filename}: {e}")
            return None
    
    @classmethod
    def load_font(cls, filename: str, point_size: int = 12) -> Optional[QFont]:
        """
        폰트 파일을 로드하고 QFont 객체를 반환합니다.
        
        Args:
            filename: 폰트 파일명
            point_size: 폰트 크기
        
        Returns:
            QFont 또는 None
        """
        if not resource_exists('fonts', filename):
            print(f"Warning: Font not found: {filename}")
            return None
        
        path = get_resource_path('fonts', filename)
        font_id = QFontDatabase.addApplicationFont(str(path))
        
        if font_id == -1:
            print(f"Error: Failed to load font: {filename}")
            return None
        
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if not font_families:
            print(f"Error: No font families found in: {filename}")
            return None
        
        font_family = font_families[0]
        font = QFont(font_family, point_size)
        
        # 캐시에 저장
        cls._loaded_fonts[filename] = font_family
        
        return font
    
    @classmethod
    def get_font_family(cls, filename: str) -> Optional[str]:
        """
        로드된 폰트의 패밀리명을 반환합니다.
        
        Args:
            filename: 폰트 파일명
        
        Returns:
            폰트 패밀리명 또는 None
        """
        if filename in cls._loaded_fonts:
            return cls._loaded_fonts[filename]
        
        # 폰트가 로드되지 않았다면 로드 시도
        font = cls.load_font(filename)
        if font:
            return cls._loaded_fonts[filename]
        
        return None
    
    @classmethod
    def apply_stylesheet_to_app(cls, filename: str):
        """
        전체 애플리케이션에 스타일시트를 적용합니다.
        
        Args:
            filename: 스타일시트 파일명
        """
        app = QApplication.instance()
        if not app:
            print("Warning: No QApplication instance found")
            return
        
        stylesheet = cls.load_stylesheet(filename)
        if stylesheet:
            app.setStyleSheet(stylesheet)
        else:
            print(f"Failed to apply stylesheet: {filename}")
    
    @classmethod
    def load_template_path(cls, template_type: str, filename: str) -> Optional[Path]:
        """
        템플릿 파일의 경로를 반환합니다.
        
        Args:
            template_type: 템플릿 타입 ('reports', 'excel', 'pdf')
            filename: 파일명
        
        Returns:
            Path 또는 None
        """
        template_resource_type = f"{template_type}_templates"
        if resource_exists(template_resource_type, filename):
            return get_resource_path(template_resource_type, filename)
        return None
    
    @classmethod
    def clear_cache(cls):
        """캐시를 모두 정리합니다."""
        cls._loaded_fonts.clear()
        cls._loaded_stylesheets.clear()
    
    @classmethod
    def get_cache_info(cls) -> dict:
        """캐시 정보를 반환합니다."""
        return {
            'loaded_fonts': len(cls._loaded_fonts),
            'loaded_stylesheets': len(cls._loaded_stylesheets),
            'font_list': list(cls._loaded_fonts.keys()),
            'stylesheet_list': list(cls._loaded_stylesheets.keys())
        }

# 편의를 위한 전역 함수들
def load_image(resource_type: str, filename: str, size: Optional[tuple] = None) -> Optional[QPixmap]:
    """이미지를 로드하는 편의 함수"""
    return ResourceLoader.load_pixmap(resource_type, filename, size)

def load_icon(resource_type: str, filename: str, size: Optional[tuple] = None) -> Optional[QIcon]:
    """아이콘을 로드하는 편의 함수"""
    return ResourceLoader.load_icon(resource_type, filename, size)

def load_style(filename: str) -> Optional[str]:
    """스타일시트를 로드하는 편의 함수"""
    return ResourceLoader.load_stylesheet(filename)

def apply_style(filename: str):
    """전체 앱에 스타일을 적용하는 편의 함수"""
    ResourceLoader.apply_stylesheet_to_app(filename)

def load_font(filename: str, size: int = 12) -> Optional[QFont]:
    """폰트를 로드하는 편의 함수"""
    return ResourceLoader.load_font(filename, size)

def get_lgeui_font(size: int = 10, weight: str = 'Regular') -> Optional[QFont]:
    """
    LGEIHeadlineTTF 폰트를 쉽게 사용하기 위한 편의 함수
    
    Args:
        size: 폰트 크기
        weight: 폰트 굵기 ('Regular', 'Light', 'Bold', 'Semibold', 'Thin')
    
    Returns:
        QFont 또는 None
    """
    weight_map = {
        'Thin': 'LGEIHeadlineTTF-Thin.ttf',
        'Light': 'LGEIHeadlineTTF-Light.ttf', 
        'Regular': 'LGEIHeadlineTTF-Regular.ttf',
        'Semibold': 'LGEIHeadlineTTF-Semibold.ttf',
        'Bold': 'LGEIHeadlineTTF-Bold.ttf'
    }
    
    filename = weight_map.get(weight, 'LGEIHeadlineTTF-Regular.ttf')
    return ResourceLoader.load_font(filename, size)