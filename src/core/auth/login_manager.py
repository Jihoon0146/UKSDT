import os
import json
import getpass
import subprocess
import base64
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal


class LoginManager(QObject):
    """로그인 관리 클래스"""
    
    # 시그널
    login_successful = pyqtSignal(str)  # 로그인 성공 (user_id)
    login_failed = pyqtSignal(str)      # 로그인 실패 (error_message)
    logout_completed = pyqtSignal()     # 로그아웃 완료
    
    def __init__(self, resource_path: str = "./resources"):
        super().__init__()
        self.resource_path = Path(resource_path)
        self.data_path = self.resource_path / "data"
        self.credentials_file = self.data_path / "user_credentials.json"
        
        # SVN 설정 (기본값, 나중에 변경 가능)
        self.svn_url = str(self.data_path / "svn_repo")  # 로컬 테스트용
        self.auto_list_path = "auto_list.txt"
        
        # 현재 로그인 상태
        self._current_user = None
        self._authenticated = False
        self._last_login_time = None
        
        # 초기화
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        """데이터 디렉토리 확인 및 생성"""
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # auto_list.txt 파일이 없으면 생성 (테스트용)
        auto_list_file = self.data_path / self.auto_list_path
        if not auto_list_file.exists():
            with open(auto_list_file, 'w', encoding='utf-8') as f:
                # 현재 OS 사용자를 기본으로 추가
                current_os_user = getpass.getuser()
                f.write(f"{current_os_user}\n")
                f.write("admin\n")
                f.write("developer\n")
        
    def _encrypt_password(self, password: str) -> str:
        """간단한 비밀번호 암호화 (Base64 + 간단한 XOR)"""
        key = "UKSDT_KEY_2025"
        encrypted = ""
        for i, char in enumerate(password):
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            encrypted += encrypted_char
        
        return base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
    
    def _decrypt_password(self, encrypted_password: str) -> str:
        """비밀번호 복호화"""
        try:
            key = "UKSDT_KEY_2025"
            decoded = base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8')
            decrypted = ""
            for i, char in enumerate(decoded):
                key_char = key[i % len(key)]
                decrypted_char = chr(ord(char) ^ ord(key_char))
                decrypted += decrypted_char
            return decrypted
        except Exception:
            return ""
    
    def _check_os_user_match(self, user_id: str) -> bool:
        """1단계: OS 계정과 ID 일치 확인"""
        current_os_user = getpass.getuser()
        return current_os_user.lower() == user_id.lower()
    
    def _check_svn_access(self, user_id: str, password: str) -> bool:
        """2단계: SVN 접근 가능 확인"""
        try:
            # 로컬 디렉토리 확인
            if os.path.exists(self.svn_url) and os.path.isdir(self.svn_url):
                # 로컬 SVN 디렉토리인지 확인
                svn_dir = os.path.join(self.svn_url, '.svn')
                if os.path.exists(svn_dir):
                    return True
            
            # 원격 SVN 서버 확인
            return self._test_svn_connection(self.svn_url, user_id, password)
            
        except Exception as e:
            print(f"SVN 접근 확인 오류: {e}")
            return False
    
    def _test_svn_connection(self, svn_url: str, username: str, password: str) -> bool:
        """SVN 서버 연결 테스트"""
        try:
            cmd = [
                "svn", "info", svn_url,
                "--username", username,
                "--password", password,
                "--non-interactive",
                "--trust-server-cert",
                "--no-auth-cache"
            ]
            
            # Windows 환경에서 창이 뜨지 않도록 설정
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                return True
            else:
                # 상세한 에러 정보 로깅
                print(f"SVN 연결 실패 (코드: {result.returncode})")
                if result.stderr:
                    print(f"SVN 에러: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("SVN 서버 연결 시간 초과")
            return False
        except FileNotFoundError:
            print("SVN 클라이언트가 설치되지 않았거나 PATH에 없습니다")
            return False
        except Exception as e:
            print(f"SVN 연결 테스트 오류: {e}")
            return False
    
    def _check_auto_list(self, user_id: str) -> bool:
        """3단계: auto_list에 사용자 ID 존재 확인"""
        try:
            auto_list_file = self.data_path / self.auto_list_path
            if not auto_list_file.exists():
                return False
                
            with open(auto_list_file, 'r', encoding='utf-8') as f:
                authorized_users = [line.strip().lower() for line in f.readlines() if line.strip()]
                
            return user_id.lower() in authorized_users
        except Exception as e:
            print(f"auto_list 확인 오류: {e}")
            return False
    
    def login(self, user_id: str, password: str, auto_login: bool = False) -> bool:
        """로그인 수행"""
        try:
            # 1단계: OS 계정 확인
            if not self._check_os_user_match(user_id):
                self.login_failed.emit("운영체제 계정과 사용자 ID가 일치하지 않습니다.")
                return False
            
            # 2단계: SVN 접근 확인
            if not self._check_svn_access(user_id, password):
                self.login_failed.emit("SVN 서버에 접근할 수 없습니다. ID나 비밀번호를 확인해주세요.")
                return False
            
            # 3단계: auto_list 확인
            if not self._check_auto_list(user_id):
                self.login_failed.emit("인증된 사용자 목록에 없습니다. 관리자에게 문의하세요.")
                return False
            
            # 모든 단계 통과 - 로그인 성공
            self._current_user = user_id
            self._authenticated = True
            self._last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 자동 로그인 옵션이 활성화되면 인증 정보 저장
            if auto_login:
                self.save_credentials(user_id, password, auto_login)
            
            self.login_successful.emit(user_id)
            return True
            
        except Exception as e:
            self.login_failed.emit(f"로그인 중 오류가 발생했습니다: {str(e)}")
            return False
    
    def logout(self):
        """로그아웃"""
        self._current_user = None
        self._authenticated = False
        self._last_login_time = None
        self.logout_completed.emit()
    
    def auto_login(self) -> bool:
        """저장된 인증 정보로 자동 로그인 시도"""
        try:
            credentials = self.get_saved_credentials()
            if not credentials or not credentials.get('auto_login', False):
                return False
            
            user_id = credentials.get('user_id', '')
            password = self._decrypt_password(credentials.get('password', ''))
            
            if user_id and password:
                return self.login(user_id, password, False)  # auto_login=False로 중복 저장 방지
                
        except Exception as e:
            print(f"자동 로그인 오류: {e}")
        
        return False
    
    def save_credentials(self, user_id: str, password: str, auto_login: bool):
        """인증 정보 저장"""
        try:
            credentials = {
                'user_id': user_id,
                'password': self._encrypt_password(password),
                'auto_login': auto_login,
                'saved_at': datetime.now().isoformat()
            }
            
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"인증 정보 저장 오류: {e}")
    
    def get_saved_credentials(self) -> Optional[Dict[str, Any]]:
        """저장된 인증 정보 불러오기"""
        try:
            if self.credentials_file.exists():
                with open(self.credentials_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"인증 정보 불러오기 오류: {e}")
        
        return None
    
    def clear_credentials(self):
        """저장된 인증 정보 삭제"""
        try:
            if self.credentials_file.exists():
                self.credentials_file.unlink()
        except Exception as e:
            print(f"인증 정보 삭제 오류: {e}")
    
    def is_authenticated(self) -> bool:
        """인증 상태 확인"""
        return self._authenticated
    
    def get_current_user(self) -> Optional[str]:
        """현재 로그인된 사용자 ID 반환"""
        return self._current_user
    
    def get_last_login_time(self) -> Optional[str]:
        """마지막 로그인 시간 반환"""
        return self._last_login_time
    
    def set_svn_config(self, svn_url: str, auto_list_path: str = "auto_list.txt"):
        """SVN 설정 변경"""
        self.svn_url = svn_url
        self.auto_list_path = auto_list_path
    
    def svn_checkout(self, local_path: str, username: str = None, password: str = None) -> bool:
        """SVN 체크아웃"""
        try:
            if not username and self._current_user:
                username = self._current_user
            
            if not username:
                print("SVN 체크아웃을 위한 사용자 인증 정보가 없습니다")
                return False
            
            cmd = [
                "svn", "checkout", self.svn_url, local_path,
                "--username", username,
                "--non-interactive",
                "--trust-server-cert"
            ]
            
            if password:
                cmd.extend(["--password", password])
            
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                print(f"SVN 체크아웃 성공: {local_path}")
                return True
            else:
                print(f"SVN 체크아웃 실패 (코드: {result.returncode})")
                if result.stderr:
                    print(f"에러: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("SVN 체크아웃 시간 초과")
            return False
        except Exception as e:
            print(f"SVN 체크아웃 오류: {e}")
            return False
    
    def svn_update(self, local_path: str, username: str = None, password: str = None) -> bool:
        """SVN 업데이트"""
        try:
            if not username and self._current_user:
                username = self._current_user
                
            if not os.path.exists(local_path):
                print(f"경로가 존재하지 않습니다: {local_path}")
                return False
            
            cmd = ["svn", "update", local_path, "--non-interactive"]
            
            if username:
                cmd.extend(["--username", username])
            if password:
                cmd.extend(["--password", password])
            
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                print(f"SVN 업데이트 성공: {local_path}")
                return True
            else:
                print(f"SVN 업데이트 실패 (코드: {result.returncode})")
                if result.stderr:
                    print(f"에러: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("SVN 업데이트 시간 초과")
            return False
        except Exception as e:
            print(f"SVN 업데이트 오류: {e}")
            return False
    
    def get_svn_info(self, path: str = None) -> dict:
        """SVN 정보 조회"""
        try:
            target_path = path or self.svn_url
            
            cmd = ["svn", "info", target_path, "--xml", "--non-interactive"]
            
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                # XML 파싱 없이 간단한 정보 추출
                info = {"success": True, "output": result.stdout}
                return info
            else:
                return {"success": False, "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "SVN info 조회 시간 초과"}
        except Exception as e:
            return {"success": False, "error": f"SVN info 조회 오류: {e}"}