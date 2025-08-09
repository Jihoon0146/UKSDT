# Resources Directory

이 디렉토리는 UKSDT 애플리케이션에서 사용하는 모든 외부 리소스를 체계적으로 관리하기 위한 곳입니다.

## 디렉토리 구조

```
src/resources/
├── README.md              # 이 파일
├── __init__.py            # 리소스 로딩 유틸리티
├── images/                # 이미지 파일들
│   ├── logos/            # 로고, 브랜딩 이미지
│   ├── backgrounds/      # 배경 이미지
│   ├── ui_elements/      # UI 요소 이미지 (버튼, 프레임 등)
│   └── screenshots/      # 스크린샷, 예시 이미지
├── icons/                 # 아이콘 파일들
│   ├── toolbar/          # 툴바 아이콘
│   ├── menu/             # 메뉴 아이콘
│   ├── status/           # 상태 표시 아이콘
│   └── system/           # 시스템 아이콘
├── fonts/                 # 폰트 파일들 (.ttf, .otf, .woff)
├── styles/                # 스타일시트 파일들 (.qss, .css)
├── templates/             # 템플릿 파일들
│   ├── reports/          # 리포트 템플릿
│   ├── excel/            # Excel 템플릿
│   └── pdf/              # PDF 템플릿
├── data/                  # 데이터 파일들 (.json, .xml, .csv)
└── sounds/                # 사운드 파일들 (.wav, .mp3)
```

## 지원되는 파일 형식

### 이미지
- PNG (권장 - 투명도 지원)
- JPG/JPEG (사진, 배경)
- SVG (벡터 이미지, 확대/축소 시 품질 유지)
- ICO (아이콘 전용)

### 폰트
- TTF (TrueType Font)
- OTF (OpenType Font)
- WOFF (Web Open Font Format)

### 스타일
- QSS (Qt Style Sheet - PyQt5/6 전용)
- CSS (웹 스타일용)

### 템플릿
- DOCX (Word 문서)
- XLSX (Excel 스프레드시트)
- PDF (PDF 문서)
- HTML (웹 템플릿)

### 데이터
- JSON (구조화된 데이터)
- XML (마크업 데이터)
- CSV (표 형태 데이터)
- YAML (설정 파일)

### 사운드
- WAV (무손실 오디오)
- MP3 (압축 오디오)
- OGG (오픈소스 오디오)

## 사용 방법

### Python 코드에서 리소스 사용

```python
from resources import get_resource_path, resource_exists

# 이미지 로딩
logo_path = get_resource_path('logos', 'company_logo.png')
if resource_exists('logos', 'company_logo.png'):
    # PyQt5에서 이미지 사용
    from PyQt5.QtGui import QPixmap
    pixmap = QPixmap(str(logo_path))

# 아이콘 로딩
icon_path = get_resource_path('toolbar_icons', 'save.svg')

# 스타일시트 로딩
style_path = get_resource_path('styles', 'dark_theme.qss')
with open(style_path, 'r', encoding='utf-8') as f:
    stylesheet = f.read()

# 템플릿 로딩
template_path = get_resource_path('excel_templates', 'report_template.xlsx')
```

### 리소스 추가 시 권장사항

1. **파일 명명 규칙**
   - 소문자와 언더스코어 사용 (`my_image.png`)
   - 공백이나 특수문자 피하기
   - 의미있는 이름 사용

2. **이미지 최적화**
   - PNG: UI 요소, 투명도가 필요한 이미지
   - JPG: 사진, 복잡한 색상의 배경
   - SVG: 아이콘, 로고 (확대/축소 시 선명)

3. **파일 크기 최적화**
   - 불필요한 메타데이터 제거
   - 적절한 해상도 사용 (UI용은 72-96 DPI)
   - 압축률과 품질의 균형

4. **저작권 준수**
   - 라이선스 확인된 리소스만 사용
   - 자체 제작 리소스 권장
   - 오픈소스 리소스 사용 시 출처 명시

## 기존 QSS 리소스와의 관계

현재 `src/QSS/` 디렉토리에 있는 스타일시트들은 점진적으로 `src/resources/styles/`로 통합될 예정입니다.

## 버전 관리 주의사항

- 대용량 파일은 Git LFS 사용 고려
- 임시 파일이나 캐시 파일은 `.gitignore`에 추가
- 민감한 데이터는 별도 관리 (환경변수, 설정 파일 등)