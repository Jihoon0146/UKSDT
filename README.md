# UKSDT - Unified Korean Software Development Tools

UKSDT는 소프트웨어 개발 및 검토 프로세스를 통합하고 자동화하는 PyQt5 기반의 데스크톱 애플리케이션입니다. 현재 Control DR(Design Review) Reviewer 도구를 포함하여 다양한 개발 도구들을 하나의 통합 인터페이스에서 제공합니다.

## 주요 기능

### Control DR Reviewer
소프트웨어 설계 검토(Design Review) 프로세스를 자동화하고 관리하는 도구입니다.

**핵심 기능:**
- **프로젝트 정보 관리**: 프로젝트명, 리뷰어, 검토 날짜 등 기본 정보 입력
- **기본 점검 항목**: Pass/Fail/N/A 선택이 가능한 5가지 표준 점검 항목
  - 요구사항 추적성 확인
  - 설계 문서 완성도
  - 코드 품질 검증
  - 테스트 케이스 완성도
  - 보안 검증 완료
- **파일 정합성 검증**: BOM List와 SW인정시험 결과서 간의 정합성 자동 검증
- **리포트 생성**: 검토 결과를 텍스트 및 Excel 형식으로 내보내기
- **실시간 미리보기**: 검토 진행 상황과 결과를 실시간으로 확인

## 기술 스택

- **Frontend**: PyQt5 with Qt Designer
- **Backend**: Python 3.x
- **Data Processing**: pandas, openpyxl
- **UI Theme**: GTRONICK ElegantDark QSS
- **Font**: LGEIHeadlineTTF/LGEITextTTF Custom Font Family

## 프로젝트 구조

```
UKSDT/
├── src/                          # 소스 코드 루트
│   ├── main.py                   # 애플리케이션 진입점
│   ├── core/                     # 핵심 UI 컴포넌트
│   │   ├── main_window_ui.py     # 메인 윈도우 클래스
│   │   ├── sidebar_ui.py         # 접이식 사이드바
│   │   ├── custom_tab_widget.py  # 커스텀 탭 위젯
│   │   └── settings_dialog.py    # 설정 대화상자
│   ├── tools/                    # 개발 도구들
│   │   └── control_dr_reviewer/  # Control DR Reviewer 도구
│   │       ├── control_dr_reviewer.py      # 메인 로직
│   │       └── components/
│   │           └── check_item_widget.py    # 체크 항목 위젯
│   ├── ui/                       # Qt Designer UI 파일
│   │   ├── compile_ui.py         # UI 파일 컴파일 스크립트
│   │   ├── *.ui                  # Qt Designer UI 파일들
│   │   └── components/           # 재사용 가능한 UI 컴포넌트
│   ├── ui_generated/             # 컴파일된 Python UI 파일
│   ├── resources/                # 리소스 파일들
│   │   ├── fonts/                # 커스텀 폰트
│   │   ├── icons/                # 아이콘 리소스
│   │   ├── images/               # 이미지 리소스
│   │   ├── styles/               # QSS 스타일시트
│   │   │   └── ElegantDark.qss   # GTRONICK 다크 테마
│   │   └── templates/            # 문서 템플릿
│   └── utils/                    # 유틸리티 모듈
│       └── resource_loader.py    # 리소스 로더
├── requirements.txt              # Python 의존성
├── CLAUDE.md                     # 개발 가이드라인
└── README.md                     # 프로젝트 문서
```

## 설치 및 실행

### 필수 요구사항
- Python 3.8 이상
- Windows 10/11 (Qt Designer 도구 지원)

### 설치 방법

1. **저장소 클론**
   ```bash
   git clone https://github.com/your-username/UKSDT.git
   cd UKSDT
   ```

2. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **애플리케이션 실행**
   ```bash
   python src/main.py
   ```

## 개발 가이드

### UI 개발 워크플로우

1. **UI 파일 수정** (Qt Designer 사용)
   ```bash
   # Qt Designer 실행 (Windows)
   designer.exe src/ui/main_window.ui
   ```

2. **UI 파일 컴파일**
   ```bash
   cd src/ui
   python compile_ui.py
   ```

### 코드 품질 도구

```bash
# 코드 포맷팅
black src/ tests/

# 코드 린팅
pylint src/
```

### 테스트 실행

```bash
# 모든 테스트 실행
python -m pytest tests/ -v

# 특정 파일 테스트
python -m pytest path/to/test_file.py -v
```

## 사용 방법

### Control DR Reviewer 사용법

1. **애플리케이션 시작**: 사이드바에서 "Control DR Reviewer" 선택
2. **프로젝트 정보 입력**: 프로젝트명, 리뷰어, 검토 날짜 입력
3. **기본 점검 항목 검토**: 각 항목에 대해 Pass/Fail/N/A 선택 및 코멘트 작성
4. **파일 업로드**: BOM List와 SW인정시험 결과서 Excel 파일 업로드
5. **정합성 검증**: "정합성 검증" 버튼 클릭하여 파일 간 정합성 확인
6. **리포트 생성**: "리포트 생성" 버튼으로 검토 결과 미리보기
7. **Excel 다운로드**: "Excel 다운로드"로 최종 보고서 저장

### 검증 조건
- **정합성 검증**: BOM List 및 SW인정시험 결과서 파일이 모두 선택되어야 함
- **리포트 생성**: 프로젝트 정보 입력 및 정합성 검증 완료 필요
- **Excel 다운로드**: 위 조건들과 함께 최소 1개 이상의 점검 항목이 Pass/Fail/N/A로 선택되어야 함

## 아키텍처 특징

### 모듈형 설계
- 각 도구는 독립적인 모듈로 구성
- 플러그인 형태로 새로운 도구 추가 가능
- 재사용 가능한 UI 컴포넌트 구조

### UI/UX 설계
- **접이식 사이드바**: 공간 효율적인 네비게이션
- **탭 기반 인터페이스**: 여러 도구의 동시 사용 지원
- **반응형 레이아웃**: 다양한 화면 크기 지원
- **다크 테마**: GTRONICK ElegantDark 테마 적용

### 데이터 처리
- pandas를 활용한 Excel 파일 분석
- 실시간 데이터 검증 및 피드백
- 구조화된 리포트 생성

## 확장성

### 새로운 도구 추가
1. `src/tools/` 디렉토리에 새 도구 모듈 생성
2. Qt Designer로 UI 파일 작성
3. 사이드바에 도구 등록
4. 메인 윈도우에서 탭으로 통합

### 커스텀 테마
- `src/resources/styles/` 디렉토리에 QSS 파일 추가
- `main.py`에서 테마 로딩 로직 수정

## 라이선스

이 프로젝트는 [적절한 라이선스]에 따라 배포됩니다.

## 기여 가이드

1. 이슈 등록 또는 기존 이슈 확인
2. 브랜치 생성 (`git checkout -b feature/새기능`)
3. 변경사항 커밋 (`git commit -am '새기능 추가'`)
4. 브랜치 푸시 (`git push origin feature/새기능`)
5. Pull Request 생성

## 지원 및 연락처

- **이슈 리포팅**: GitHub Issues 사용
- **문서**: 프로젝트 Wiki 참조
- **개발 가이드**: CLAUDE.md 참조

---

**개발 상태**: 활발히 개발 중  
**최신 업데이트**: 2025년 1월  
**지원 플랫폼**: Windows 10/11 (주), macOS/Linux (실험적)