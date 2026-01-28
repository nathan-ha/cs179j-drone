```
git clone --recursive https://github.com/nathan-ha/cs179j-drone
cd cs179j-drone

git submodule update --init --recursive

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r ~/cs179j-drone/requirements.txt

cd ardupilot
sudo apt update
sudo apt install -y build-essential g++ clang ccache gawk python3-dev python3-pip python3-numpy python3-scipy python3-matplotlib python3-opencv python3-pexpect python3-lxml




export PATH=$HOME/cs179j-drone/ardupilot/Tools/autotest:$PATH
source ~/.bashrc

```

```

sudo apt update
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl



export GAZEBO_MODEL_PATH=$HOME/cs179j-drone/ardupilot_gazebo/models
export GZ_SIM_RESOURCE_PATH=$HOME/cs179j-drone/ardupilot_gazebo/worlds:$GAZEBO_MODEL_PATH
source ~/.bashrc

cd ardupilot_gazebo
mkdir build && cd build
cmake .. 
make -j4
sudo make install

```