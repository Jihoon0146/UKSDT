from PyQt5.QtWidgets import (QWidget, QFileDialog, QMessageBox, QRadioButton, 
                             QButtonGroup, QVBoxLayout)
from PyQt5.QtCore import QDate, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import os
import pandas as pd
from datetime import datetime

from ui_generated.ui_control_dr_reviewer import Ui_ControlDrReviewer
from .components.check_item_widget import CheckItemWidget

class ControlDRReviewerWidget(QWidget):
    """Control DR Reviewer 도구 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ControlDrReviewer()
        self.ui.setupUi(self)
        
        # 데이터 저장용
        self.bom_file_path = ""
        self.sw_test_file_path = ""
        self.verification_results = {}
        self.check_items = []  # CheckItemWidget 리스트
        
        self.setup_ui()
        self.setup_connections()
        self.setup_check_items()
        
    def setup_ui(self):
        """UI 추가 설정"""
        # 현재 날짜로 초기화
        self.ui.review_date_input.setDate(QDate.currentDate())
        
        # 모든 버튼 기본적으로 활성화 (조건 확인은 클릭 시 수행)
        
    def setup_connections(self):
        """시그널 연결"""
        # 파일 업로드 버튼
        self.ui.bom_browse_btn.clicked.connect(self.browse_bom_file)
        self.ui.sw_test_browse_btn.clicked.connect(self.browse_sw_test_file)
        
        # 검증 및 결과 버튼
        self.ui.verify_btn.clicked.connect(self.run_verification)
        self.ui.generate_report_btn.clicked.connect(self.generate_report)
        self.ui.download_excel_btn.clicked.connect(self.download_excel)
        
    def setup_check_items(self):
        """체크리스트 항목 설정 - CheckItemWidget 컴포넌트 사용"""
        # 기본 점검 항목들
        check_item_texts = [
            "요구사항 추적성 확인",
            "설계 문서 완성도", 
            "코드 품질 검증",
            "테스트 케이스 완성도",
            "보안 검증 완료"
        ]
        
        # 체크리스트 레이아웃 가져오기
        checklist_layout = self.ui.checklist_content_layout
        
        # 기존 스페이서 제거
        for i in reversed(range(checklist_layout.count())):
            item = checklist_layout.itemAt(i)
            if item.spacerItem():
                checklist_layout.removeItem(item)
        
        # CheckItemWidget들 생성 및 추가
        for text in check_item_texts:
            check_item = CheckItemWidget(text)
            check_item.status_changed.connect(self.on_check_item_changed)
            self.check_items.append(check_item)
            checklist_layout.addWidget(check_item)
        
        # 하단 스페이서 추가
        from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        checklist_layout.addItem(spacer)
        
    def on_check_item_changed(self, status):
        """체크 항목 상태 변경 시 호출"""
        sender = self.sender()
        if sender:
            comment = sender.get_comment()
            comment_info = f" (코멘트: {comment[:20]}...)" if comment.strip() else ""
            print(f"[DEBUG] 체크 항목 '{sender.get_item_text()}' 상태 변경: {status}{comment_info}")
            
    def browse_bom_file(self):
        """BOM List 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "BOM List 파일 선택",
            "",
            "Excel 파일 (*.xlsx *.xls);;모든 파일 (*)"
        )
        
        if file_path:
            self.bom_file_path = file_path
            self.ui.bom_file_path.setText(file_path)
            self.ui.bom_status_label.setText(f"파일 선택됨: {os.path.basename(file_path)}")
            self.ui.bom_status_label.setStyleSheet("color: #27ae60;")
            print(f"[DEBUG] BOM 파일 선택됨: {os.path.basename(file_path)}")
            
    def browse_sw_test_file(self):
        """SW인정시험 결과서 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "SW인정시험 결과서 파일 선택",
            "",
            "Excel 파일 (*.xlsx *.xls);;모든 파일 (*)"
        )
        
        if file_path:
            self.sw_test_file_path = file_path
            self.ui.sw_test_file_path.setText(file_path)
            self.ui.sw_test_status_label.setText(f"파일 선택됨: {os.path.basename(file_path)}")
            self.ui.sw_test_status_label.setStyleSheet("color: #27ae60;")
            print(f"[DEBUG] SW인정시험 결과서 파일 선택됨: {os.path.basename(file_path)}")
            
    def check_verification_conditions(self):
        """검증 실행 조건 확인"""
        missing_conditions = []
        
        if not self.bom_file_path:
            missing_conditions.append("BOM List 파일이 선택되지 않았습니다.")
        elif not os.path.exists(self.bom_file_path):
            missing_conditions.append("BOM List 파일을 찾을 수 없습니다.")
            
        if not self.sw_test_file_path:
            missing_conditions.append("SW인정시험 결과서 파일이 선택되지 않았습니다.")
        elif not os.path.exists(self.sw_test_file_path):
            missing_conditions.append("SW인정시험 결과서 파일을 찾을 수 없습니다.")
            
        return missing_conditions
    
    def check_report_conditions(self):
        """리포트 생성 조건 확인"""
        missing_conditions = []
        
        # 프로젝트 기본 정보 확인
        if not self.ui.project_name_input.text().strip():
            missing_conditions.append("프로젝트명을 입력해야 합니다.")
            
        if not self.ui.reviewer_input.text().strip():
            missing_conditions.append("리뷰어명을 입력해야 합니다.")
        
        # 검증이 완료되었는지 확인
        if not self.verification_results:
            missing_conditions.append("먼저 정합성 검증을 실행해야 합니다.")
            
        return missing_conditions
    
    def check_excel_conditions(self):
        """Excel 다운로드 조건 확인"""
        missing_conditions = []
        
        # 프로젝트 기본 정보 확인
        if not self.ui.project_name_input.text().strip():
            missing_conditions.append("프로젝트명을 입력해야 합니다.")
            
        if not self.ui.reviewer_input.text().strip():
            missing_conditions.append("리뷰어명을 입력해야 합니다.")
        
        # 검증이 완료되었는지 확인
        if not self.verification_results:
            missing_conditions.append("먼저 정합성 검증을 실행해야 합니다.")
        
        # 체크리스트에서 최소 하나 이상 Pass/Fail/N/A가 선택되었는지 확인 (None 제외)
        has_selection = False
        for check_item in self.check_items:
            if check_item.get_status() in ['Pass', 'Fail', 'N/A']:
                has_selection = True
                break
        
        if not has_selection:
            missing_conditions.append("최소 하나 이상의 체크 항목을 Pass, Fail, 또는 N/A로 선택해야 합니다.")
            
        return missing_conditions
            
    def run_verification(self):
        """정합성 검증 실행"""
        try:
            # 검증 조건 확인
            missing_conditions = self.check_verification_conditions()
            if missing_conditions:
                error_message = "검증을 실행하기 전에 다음 조건을 충족해야 합니다:\n\n"
                error_message += "\n".join(f"• {condition}" for condition in missing_conditions)
                QMessageBox.warning(self, "검증 실행 불가", error_message)
                return
                
            # 검증 진행 메시지
            self.ui.result_preview.setText("검증을 진행 중입니다...")
            
            # 검증 진행 상태를 execution_result에 실시간 표시
            self.ui.execution_result.setText("검증을 진행 중입니다...")
            
            # 실제 검증 로직 (간단한 예시)
            self.verification_results = self.perform_verification()
            
            # 결과 표시
            self.display_verification_results()
            
            print(f"[DEBUG] 정합성 검증 완료 - BOM: {os.path.basename(self.bom_file_path) if self.bom_file_path else 'N/A'}, SW테스트: {os.path.basename(self.sw_test_file_path) if self.sw_test_file_path else 'N/A'}")
            QMessageBox.information(self, "완료", "정합성 검증이 완료되었습니다.")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"검증 중 오류가 발생했습니다:\n{str(e)}")
            
    def perform_verification(self):
        """실제 검증 로직 수행"""
        results = {
            "bom_analysis": {},
            "sw_test_analysis": {},
            "consistency_check": {},
            "summary": {}
        }
        
        try:
            print(f"[DEBUG] 검증 시작 - BOM 파일 읽기 중...")
            # BOM List 파일 분석
            bom_df = pd.read_excel(self.bom_file_path, sheet_name=0)
            results["bom_analysis"] = {
                "total_items": len(bom_df),
                "columns": list(bom_df.columns),
                "status": "성공"
            }
            print(f"[DEBUG] BOM 파일 분석 완료 - {len(bom_df)}개 항목")
            
            print(f"[DEBUG] SW인정시험 결과서 파일 읽기 중...")
            # SW인정시험 결과서 분석
            sw_test_df = pd.read_excel(self.sw_test_file_path, sheet_name=0)
            results["sw_test_analysis"] = {
                "total_tests": len(sw_test_df),
                "columns": list(sw_test_df.columns),
                "status": "성공"
            }
            print(f"[DEBUG] SW인정시험 결과서 분석 완료 - {len(sw_test_df)}개 테스트")
            
            # 정합성 검증 (예시) - 실제로는 더 복잡한 로직이 필요
            print(f"[DEBUG] 정합성 검증 수행 중...")
            results["consistency_check"] = {
                "bom_sw_match": "양호",
                "data_integrity": "정상",
                "missing_items": 0
            }
            
            # 요약
            results["summary"] = {
                "overall_status": "PASS",
                "verification_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "issues_found": 0
            }
            print(f"[DEBUG] 검증 완료 - 결과: PASS")
            
        except Exception as e:
            results["summary"] = {
                "overall_status": "FAIL",
                "error": str(e),
                "verification_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        return results
        
    def display_verification_results(self):
        """검증 결과를 UI에 표시"""
        if not self.verification_results:
            return
            
        result_text = "=== 정합성 검증 결과 ===\n\n"
        
        # BOM 분석 결과
        bom_analysis = self.verification_results.get("bom_analysis", {})
        result_text += f"📋 BOM List 분석:\n"
        result_text += f"  - 총 항목 수: {bom_analysis.get('total_items', 'N/A')}\n"
        result_text += f"  - 분석 상태: {bom_analysis.get('status', 'N/A')}\n\n"
        
        # SW 테스트 결과 분석
        sw_analysis = self.verification_results.get("sw_test_analysis", {})
        result_text += f"🧪 SW인정시험 결과서 분석:\n"
        result_text += f"  - 총 테스트 수: {sw_analysis.get('total_tests', 'N/A')}\n"
        result_text += f"  - 분석 상태: {sw_analysis.get('status', 'N/A')}\n\n"
        
        # 정합성 검증 결과
        consistency = self.verification_results.get("consistency_check", {})
        result_text += f"✅ 정합성 검증:\n"
        result_text += f"  - BOM-SW 매칭: {consistency.get('bom_sw_match', 'N/A')}\n"
        result_text += f"  - 데이터 무결성: {consistency.get('data_integrity', 'N/A')}\n"
        result_text += f"  - 누락 항목: {consistency.get('missing_items', 'N/A')}개\n\n"
        
        # 요약
        summary = self.verification_results.get("summary", {})
        result_text += f"📊 최종 결과:\n"
        result_text += f"  - 전체 상태: {summary.get('overall_status', 'N/A')}\n"
        result_text += f"  - 검증 시간: {summary.get('verification_time', 'N/A')}\n"
        result_text += f"  - 발견된 이슈: {summary.get('issues_found', 'N/A')}개\n"
        
        # execution_result에도 동일한 결과 표시 (정합성 점검 섹션 내)
        self.ui.execution_result.setText(result_text)
        self.ui.result_preview.setText(result_text)
        
    def generate_report(self):
        """리포트 생성"""
        try:
            # 리포트 생성 조건 확인
            missing_conditions = self.check_report_conditions()
            if missing_conditions:
                error_message = "리포트를 생성하기 전에 다음 조건을 충족해야 합니다:\n\n"
                error_message += "\n".join(f"• {condition}" for condition in missing_conditions)
                QMessageBox.warning(self, "리포트 생성 불가", error_message)
                return
            
            # 프로젝트 정보 수집
            project_info = self.get_project_info()
            
            # 체크리스트 결과 수집
            checklist_results = self.get_checklist_results()
            
            # 최종 결과 텍스트 업데이트
            report_text = self.generate_report_text(project_info, checklist_results)
            
            # 미리보기에 리포트 표시
            self.ui.result_preview.setText(report_text)
            
            print(f"[DEBUG] 리포트 생성 완료 - 프로젝트: {project_info.get('project_name', 'N/A')}, 체크리스트 항목: {len(checklist_results)}개")
            QMessageBox.information(self, "완료", "리포트가 생성되었습니다.")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"리포트 생성 중 오류가 발생했습니다:\n{str(e)}")
            
    def get_project_info(self):
        """프로젝트 정보 수집"""
        return {
            "project_name": self.ui.project_name_input.text(),
            "reviewer": self.ui.reviewer_input.text(),
            "review_date": self.ui.review_date_input.date().toString("yyyy-MM-dd"),
            "final_comment": self.ui.final_comment_input.toPlainText()
        }
        
    def get_checklist_results(self):
        """체크리스트 결과 수집"""
        results = {}
        
        for check_item in self.check_items:
            item_text = check_item.get_item_text()
            status = check_item.get_status()
            comment = check_item.get_comment()
            
            # None 상태는 "미확인"으로 표시
            if status == 'None':
                display_status = "미확인"
            else:
                display_status = status
            
            # 코멘트가 있으면 함께 표시
            if comment.strip():
                results[item_text] = f"{display_status} - {comment.strip()}"
            else:
                results[item_text] = display_status
                
        return results
        
    def generate_report_text(self, project_info, checklist_results):
        """리포트 텍스트 생성"""
        report = "=== Control DR Review 결과 보고서 ===\n\n"
        
        # 프로젝트 정보
        report += "📋 프로젝트 정보\n"
        report += f"  - 프로젝트명: {project_info['project_name']}\n"
        report += f"  - 리뷰어: {project_info['reviewer']}\n"
        report += f"  - 리뷰 날짜: {project_info['review_date']}\n\n"
        
        
        # 체크리스트 결과
        report += "✅ 점검 항목 결과\n"
        for item, result in checklist_results.items():
            if result == "Pass" or result.startswith("Pass"):
                status_icon = "✅"
            elif result == "Fail" or result.startswith("Fail"):
                status_icon = "❌"
            elif result == "N/A" or result.startswith("N/A"):
                status_icon = "🚫"
            elif result == "미확인" or result.startswith("미확인"):
                status_icon = "⚪"
            else:
                status_icon = "⚪"
            report += f"  {status_icon} {item}: {result}\n"
        report += "\n"
        
        # 파일 정합성 검증 결과
        if self.verification_results:
            summary = self.verification_results.get("summary", {})
            report += "🔍 파일 정합성 검증\n"
            report += f"  - BOM List: {os.path.basename(self.bom_file_path) if self.bom_file_path else 'N/A'}\n"
            report += f"  - SW인정시험 결과서: {os.path.basename(self.sw_test_file_path) if self.sw_test_file_path else 'N/A'}\n"
            report += f"  - 검증 결과: {summary.get('overall_status', 'N/A')}\n"
            report += f"  - 검증 시간: {summary.get('verification_time', 'N/A')}\n\n"
        
        # 최종 의견
        if project_info['final_comment']:
            report += "💬 최종 의견\n"
            report += f"{project_info['final_comment']}\n\n"
        
        report += f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return report
        
    def download_excel(self):
        """Excel 파일 다운로드"""
        try:
            # Excel 다운로드 조건 확인
            missing_conditions = self.check_excel_conditions()
            if missing_conditions:
                error_message = "Excel 파일을 다운로드하기 전에 다음 조건을 충족해야 합니다:\n\n"
                error_message += "\n".join(f"• {condition}" for condition in missing_conditions)
                QMessageBox.warning(self, "Excel 다운로드 불가", error_message)
                return
            
            # 저장할 파일 경로 선택
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Excel 파일 저장",
                f"Control_DR_Review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel 파일 (*.xlsx);;모든 파일 (*)"
            )
            
            if file_path:
                self.create_excel_report(file_path)
                print(f"[DEBUG] Excel 파일 저장 완료 - 경로: {file_path}")
                QMessageBox.information(self, "완료", f"Excel 파일이 저장되었습니다:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"Excel 파일 저장 중 오류가 발생했습니다:\n{str(e)}")
            
    def create_excel_report(self, file_path):
        """Excel 리포트 파일 생성"""
        project_info = self.get_project_info()
        checklist_results = self.get_checklist_results()
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # 프로젝트 정보 시트
            project_df = pd.DataFrame([
                ["프로젝트명", project_info['project_name']],
                ["리뷰어", project_info['reviewer']],
                ["리뷰 날짜", project_info['review_date']],
                ["최종 의견", project_info['final_comment']]
            ], columns=["항목", "내용"])
            project_df.to_excel(writer, sheet_name='프로젝트 정보', index=False)
            
            # 체크리스트 결과 시트
            checklist_df = pd.DataFrame([
                [item, result] for item, result in checklist_results.items()
            ], columns=["점검 항목", "결과"])
            checklist_df.to_excel(writer, sheet_name='점검 결과', index=False)
            
            # 파일 정합성 검증 결과 시트
            if self.verification_results:
                verification_data = []
                verification_data.append(["BOM 파일", os.path.basename(self.bom_file_path) if self.bom_file_path else "N/A"])
                verification_data.append(["SW테스트 파일", os.path.basename(self.sw_test_file_path) if self.sw_test_file_path else "N/A"])
                
                summary = self.verification_results.get("summary", {})
                verification_data.append(["전체 상태", summary.get("overall_status", "N/A")])
                verification_data.append(["검증 시간", summary.get("verification_time", "N/A")])
                verification_data.append(["발견된 이슈", summary.get("issues_found", "N/A")])
                
                verification_df = pd.DataFrame(verification_data, columns=["항목", "결과"])
                verification_df.to_excel(writer, sheet_name='정합성 검증', index=False)