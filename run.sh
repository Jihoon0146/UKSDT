echo \### 가상환경 활성화 \###
source ./venv/Scripts/activate
echo \### 환경변수 활성화 \###
export UKSDT_RESOURCE_PATH="./resources"
echo \### UI 업데이트 진행 \###
./update_ui.sh
echo \### 어플리케이션 실행 \###
./venv/Scripts/python.exe ./src/main.py