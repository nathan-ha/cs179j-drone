# Clone repository
```
git clone --depth 1 https://github.com/nathan-ha/cs179j-drone
cd cs179j-drone
```

Updates the submodules if using simulation. 
```
git submodule update --init --recursive
```

# Virtual Environment & Dependencies
Use a python virtual environment to minimize risk of errors. We need the `--system-site-packages` flag because we are using picamera2 and opencv-python system packages, rather than pip ones.
```
python -m venv venv --system-site-packages
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r ~/cs179j-drone/requirements.txt
```
```deactivate``` to exit the virtual environment and ```source venv/bin/activate``` to enter it.

# Installation (Target Tracking)
This project uses OpenCV and the Raspberry Pi Zero specifically uses picamera2. These are best installed as system packages.
```
sudo apt update
sudo apt install picamera2
sudo apt install opencv-python
```

# Running Code
- I recommend running ```python src/preflight.py``` to make sure that the flight controller + motors work properly.
- You may also run ```python test_code/target-tracking/checkCam.py``` to check if the Raspberry Pi detects a camera.
- Run ```python src``` while in the virtual environment to activate the auto tracking and shooting.

# Installation (Simulation)
This will be running on an Ubuntu/Linux device. WSL can be used on a Windows device.

### WSL
Installing WSL
```
wsl --install
```
Start WSL by typing ```wsl``` in the terminal or by using opening a **remote window in VSCode**.    <img width="30" height="23" alt="image" src="https://github.com/user-attachments/assets/fa9ee392-9032-4177-92d6-c438d29deca2" />

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
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
```

**NOTE**: Only ArduPilot needs a virtual environment.


## Configurations
The Gazebo 3D simulation may be really laggy. This is because of WSL. WSL uses a software GPU called llvmpipe instead of using the actual GPU on your device.
Type ```glxinfo -B` into the terminal and check the OpenGL section. If it says llvmpipe, it is using the software GPU.
Adding this will switch to your actual GPU: 
```
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
export GALLIUM_DRIVER=d3d12
export LIBGL_ALWAYS_SOFTWARE=false
```


sim_vehicle.py -v ArduCopter -f quad --console --map --out udp:127.0.0.1:14550
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console quad --map --out udp:127.0.0.1:14550
