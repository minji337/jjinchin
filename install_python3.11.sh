#!/bin/bash
# chmod +x install_python3.11.sh && ./install_python3.11.sh

# 스크립트 시작 시간 기록
start_time=$SECONDS

# 필요한 패키지 설치
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl software-properties-common

# Python 소스 코드 다운로드 및 압축 해제
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz 
tar -xf Python-3.11.0.tar.xz
cd Python-3.11.0

# Python 빌드 및 설치
./configure 
sudo make altinstall

# Python 소스 및 압축 파일 삭제
cd ..
rm -rf Python-3.11.0 Python-3.11.0.tar.xz

# Python 3.11을 사용하여 pip 업그레이드
python3.11 -m pip install --upgrade pip

# 파이썬 패키지 설치
python3.11 -m pip install --force-reinstall retry==0.9.2
python3.11 -m pip install --force-reinstall openai==1.3.7
python3.11 -m pip install --force-reinstall Flask==3.0.0
python3.11 -m pip install --force-reinstall pytz==2023.3.post1
python3.11 -m pip install --force-reinstall tavily-python==0.2.8
python3.11 -m pip install --force-reinstall pymongo==4.6.1
python3.11 -m pip install --force-reinstall scipy==1.11.4
python3.11 -m pip install --force-reinstall pinecone-client==2.2.4
python3.11 -m pip install --force-reinstall requests==2.31.0

# Python 및 pip alias 설정
echo "alias python3='python3.11'" >> ~/.bashrc
echo "alias pip='python3.11 -m pip'" >> ~/.bashrc

# 스크립트 종료 시간과 소요 시간 계산 및 출력
end_time=$SECONDS
elapsed=$(( end_time - start_time ))
echo "스크립트 실행 시간: $(( elapsed / 60 ))분 $(( elapsed % 60 ))초"