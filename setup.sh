sudo apt-get update -y
sudo apt-get upgrade -y

# checking python version
if ! hash python; then
    echo "python is not installed"
    exit 1
fi

ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "27" ]; then
    echo "This script requires python 2.7 or greater"
    exit 1
fi

# pip packages installation
echo "[INFO] Install for pip packages..."
pip install numpy -y 
pip install opencv-python3 -y
pip install pyserial -y
pip install threaded -y

sudo apt-get install python3-flask -y 
sudo apt-get install fswebcam -y 
