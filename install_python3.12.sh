#!/bin/bash
# chmod +x install_python3.12.sh && ./install_python3.12.sh

# 스크립트 시작 시간 기록
start_time=$SECONDS

# 필요한 패키지 설치
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl software-properties-common

# Python 소스 코드 다운로드 및 압축 해제
wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tar.xz 
tar -xf Python-3.12.4.tar.xz
cd Python-3.12.4

# Python 빌드 및 설치
./configure 
sudo make altinstall

# Python 소스 및 압축 파일 삭제
cd ..
rm -rf Python-3.12.4 Python-3.12.4.tar.xz

# Python 3.12를 사용하여 pip 업그레이드
python3.12 -m pip install --upgrade pip

# 파이썬 패키지 설치
python3.12 -m pip install --force-reinstall retry==0.9.2
python3.12 -m pip install --force-reinstall openai==1.37.1
python3.12 -m pip install --force-reinstall Flask==3.0.3
python3.12 -m pip install --force-reinstall pytz==2024.1
python3.12 -m pip install --force-reinstall tavily-python==0.3.5
python3.12 -m pip install --force-reinstall pymongo==4.8.0
python3.12 -m pip install --force-reinstall scipy==1.14.0
python3.12 -m pip install --force-reinstall "pinecone-client[grpc]==5.0.0"
python3.12 -m pip install --force-reinstall requests==2.32.3
python3.12 -m pip install --force-reinstall tiktoken==0.7.0

# Python 및 pip alias 설정
echo "alias python3='python3.12'" >> ~/.bashrc
echo "alias pip='python3.12 -m pip'" >> ~/.bashrc

# 스크립트 종료 시간과 소요 시간 계산 및 출력
end_time=$SECONDS
elapsed=$(( end_time - start_time ))
echo "스크립트 실행 시간: $(( elapsed / 60 ))분 $(( elapsed % 60 ))초"