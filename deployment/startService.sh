#!/usr/bin/env bash

YELLOW='\033[1;33m'
WHITE='\033[0m'
RED='\033[0;31m'

SUMP_SERVICE_FILE=sumpPump.service


function cloneServiceFiles {
    if [[ -d "/home/pi/SumpPumpOverflow" ]]; then
        echo -e "${YELLOW}---------------Service Folder Exists---------------${WHITE}"
        cd /home/pi/SumpPumpOverflow
        git pull
    else
        echo -e "${YELLOW}---------------Cloning Service---------------${WHITE}"
        cd /home/pi/
        git clone https://github.com/jonny561201/SumpPumpOverflow.git
    fi
}

function startVirtualEnv {
    if [[ ! -d "/home/pi/SumpPumpOverflow/venv" ]]; then
      echo -e "${YELLOW}----------Creating VirtualEnv----------${WHITE}"
      pushd "/home/pi/SumpPumpOverflow"
      sudo pip3 install virtualenv
      python3 -m virtualenv venv
      popd
    fi
      echo -e "${YELLOW}---------------starting VirtualEnv---------------${WHITE}"
      source /home/pi/SumpPumpOverflow/venv/bin/activate
}

function installDependencies {
    echo -e "${YELLOW}---------------Installing Dependencies---------------${WHITE}"
    pip3 install -Ur requirements.txt
}

function stopService {
    echo -e "${YELLOW}---------------Stopping Service---------------${WHITE}"
    sudo systemctl stop ${SUMP_SERVICE_FILE}
    sudo rm /lib/systemd/system/${SUMP_SERVICE_FILE}
}

function copyServiceFile {
    echo  -e "${YELLOW}---------------Creating SystemD---------------${WHITE}"
    sudo chmod 666 ./deployment/${SUMP_SERVICE_FILE}
    sudo yes | sudo cp ./deployment/${SUMP_SERVICE_FILE} /lib/systemd/system/${SUMP_SERVICE_FILE}
}

function configureSystemD {
    echo  -e "${YELLOW}---------------Configuring SystemD---------------${WHITE}"
    sudo systemctl daemon-reload
    sudo systemctl enable ${SUMP_SERVICE_FILE}
}

function restartDevice {
    echo  -e "${YELLOW}---------------Rebooting Device---------------${WHITE}"
    sudo reboot
}



stopService
cloneServiceFiles
startVirtualEnv
installDependencies
copyServiceFile
configureSystemD
restartDevice