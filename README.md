```
git clone --recursive https://github.com/nathan-ha/cs179j-drone
cd cs179j-drone

git submodule add https://github.com/ArduPilot/ardupilot.git ardupilot
git submodule update --init --recursive

cd ardupilot
sudo apt update
sudo apt install -y build-essential g++ clang ccache gawk python3-dev python3-pip python3-numpy python3-scipy python3-matplotlib python3-opencv python3-pexpect python3-lxml


python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r ~/cs179j-drone/requirements.txt
```
