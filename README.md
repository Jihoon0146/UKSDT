# UKSDT 통합 개발 도구

UKSDT (Unified Kitchen Software Development Toolkit)는 PyQt5 기반의 통합 개발 도구입니다. 프로젝트 관리, 품질 검토, 외부 링크 관리 등의 기능을 하나의 통합 환경에서 제공합니다.

## 🚀 주요 기능

### 📋 Projects (프로젝트 관리)
- **계층적 구조**: Wrapper > Project 2단계 구조로 체계적인 프로젝트 관리
- **스마트 완료 시스템**: 프로젝트 완료 시 상위 Wrapper 자동 완료 체크
- **직관적 UI**: 
  - 우클릭 컨텍스트 메뉴로 추가/삭제
  - Project 상세뷰: 표준 폼 + 완료 버튼
  - Wrapper 상세뷰: 진행률 대시보드 + 하위 프로젝트 목록
- **데이터 보존**: JSON 기반 데이터 저장으로 안전한 데이터 관리

### 🔍 Control DR Reviewer (품질 검토)
- BOM 파일과 SW 테스트 파일 업로드 및 검증
- Excel 기반 데이터 처리 및 분석
- 자동화된 리포트 생성 및 Excel 내보내기
- 체크리스트 기반 품질 관리

### 🔗 Externals (외부 링크 관리)
- 프로젝트 관련 외부 링크 중앙 관리
- 그리드 레이아웃으로 시각적 정리
- JSON 설정 파일 기반 링크 관리
- 즐겨찾기 및 카테고리 지원

## 📦 설치 및 실행

### 시스템 요구사항
- Python 3.9+
- Windows 10/11 (Git Bash 환경 권장)

### 설치 방법

```bash
# 1. 저장소 클론
git clone https://github.com/your-org/UKSDT.git
cd UKSDT

# 2. 가상환경 생성 및 활성화
python -m venv venv
source ./venv/Scripts/activate  # Windows Git Bash

# 3. 의존성 설치
pip install -r requirements.txt
```

### 실행 방법

```bash
# 간단 실행
./run.sh

# 또는 수동 실행
source ./venv/Scripts/activate
export UKSDT_RESOURCE_PATH="./resources"
python src/main.py
```

## 🛠️ 개발

### UI 개발 워크플로우

```bash
# 1. Qt Designer로 .ui 파일 편집
# 2. UI 코드 생성
./update_ui.sh

# 3. 애플리케이션 실행
./run.sh
```

### 프로젝트 구조

```
UKSDT/
├── src/                    # 소스 코드
│   ├── main.py            # 메인 엔트리포인트
│   ├── core/              # 핵심 UI 컴포넌트
│   │   ├── main_window.py # 메인 윈도우
│   │   └── components/    # 공통 컴포넌트
│   ├── tools/             # 도구별 모듈
│   │   ├── projects/      # 프로젝트 관리 도구
│   │   ├── control_dr_reviewer/  # 품질 검토 도구
│   │   └── externals/     # 외부 링크 관리
│   └── utils/             # 유틸리티 함수들
├── resources/             # 리소스 파일
│   ├── data/             # 데이터 파일
│   ├── fonts/            # 사용자 정의 폰트
│   ├── icons/            # 아이콘
│   └── styles/           # 스타일시트
├── requirements.txt      # Python 의존성
├── run.sh               # 실행 스크립트
└── update_ui.sh         # UI 컴파일 스크립트
```

## 🎯 사용법

### Projects 도구 사용법

1. **Wrapper 추가**: 상태 루트 우클릭 → "Wrapper 추가" → 이름 입력
2. **Project 추가**: 상태 루트 또는 Wrapper 우클릭 → "Project 추가" → 이름 입력 → 상세 정보 편집 → 저장
3. **Project 완료**: Project 선택 → 상세뷰 → "완료" 버튼 → 확인
4. **Wrapper 완료**: 
   - 자동: 모든 하위 Project 완료 시 자동 제안
   - 수동: Wrapper 선택 → 상세뷰 → "완료 처리" 버튼

### 주요 특징
- **완료된 항목은 자동으로 '완료' 섹션으로 이동**
- **완료 섹션은 기본적으로 접힌 상태로 표시**
- **안전장치: 하위 항목이 있는 Wrapper는 삭제 불가**

## 🔧 기술 스택

- **Frontend**: PyQt5, Qt Designer
- **Data Processing**: pandas, numpy
- **Styling**: QDarkStyle + Custom QSS
- **Data Storage**: JSON
- **Build**: Custom shell scripts

## 📝 개발자 가이드

자세한 개발 가이드는 [CLAUDE.md](CLAUDE.md)를 참조하세요.

### 핵심 개념
- **모듈화된 도구 구조**: 각 도구는 독립적인 모듈로 개발
- **UI/로직 분리**: Qt Designer UI + Python 비즈니스 로직
- **리소스 중앙화**: 모든 리소스는 `resources/` 디렉토리에 중앙 관리
- **설정 기반**: JSON 설정 파일로 유연한 구성

## 📄 라이선스

이 프로젝트는 내부 사용 목적으로 개발되었습니다.

## 🤝 기여

프로젝트에 대한 개선사항이나 버그 리포트는 이슈 트래커를 통해 제출해 주세요.

---

**UKSDT Team** - Unified Kitchen Software Development Toolkit