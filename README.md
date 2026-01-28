## Installation
This will be running on an Ubuntu/Linux device. WSL can be used on a Windows device.

### WSL
Installing WSL
```
wsl --install
```
Start WSL by typing ```wsl``` in the terminal or by using opening a **remote window in VSCode**.    <img width="30" height="23" alt="image" src="https://github.com/user-attachments/assets/fa9ee392-9032-4177-92d6-c438d29deca2" />

## Clone repository
```
git clone --recursive https://github.com/nathan-ha/cs179j-drone
cd cs179j-drone
```

Updates the submodules that are being used. 
```
git submodule update --init --recursive
```
## Virtual Environment
Some dependencies for **ArduPilot** are safer to install and use inside a virtual environment compared to system-wide. 
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r ~/cs179j-drone/requirements.txt
```
```deactivate``` to exit the virtual environment and ```source venv/bin/activate``` to enter it.

## ArduPilot
Install ArduPilot dependencies.
```
cd ardupilot
sudo apt update
sudo apt install -y build-essential g++ clang ccache gawk python3-dev python3-pip python3-numpy python3-scipy python3-matplotlib python3-opencv python3-pexpect python3-lxml
```

Add to bashrc to make running commands easier
```
echo 'export PATH=$HOME/cs179j-drone/ardupilot/Tools/autotest:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Running the test simulation.
```
sim_vehicle.py -v ArduCopter
```

## Gazebo Harmonics
Install Gazebo dependencies. 
```
sudo apt update
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl
```

Add to bashrc to make running commands easier
```
export GAZEBO_MODEL_PATH=$HOME/cs179j-drone/ardupilot_gazebo/models
export GZ_SIM_RESOURCE_PATH=$HOME/cs179j-drone/ardupilot_gazebo/worlds:$GAZEBO_MODEL_PATH
source ~/.bashrc
```

Build Gazebo
```
cd ardupilot_gazebo
mkdir build && cd build
cmake .. 
make -j4
sudo make install
```

To run Gazebo with ArduPilot, in one terminal, run this command:  
```
gz sim -v4 -r iris_runway.sdf
```
Open up another terminal and run 
```
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console```
```

NOTE: **Only ArduPilot needs a virtual environment.**
