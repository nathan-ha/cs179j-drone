cd ~/cs179j-drone/ardupilot

source ../venv/bin/activate
./waf distclean
./waf configure --board NxtPX4v2
./waf copter --upload
