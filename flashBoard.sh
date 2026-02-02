cd ~/cs179j-drone/ardupilot

source ../venv/bin/activate
./waf distclean
./waf configure --board MatekH743
./waf copter --upload
