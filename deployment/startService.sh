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

function createEnvironmentVariableFile {
    if [[ ! -f "/home/pi/SumpPumpOverflow/serviceEnvVariables" ]]; then
        echo -e "${YELLOW}---------------Creating Environment Variable File---------------${WHITE}"
        createFile
    else
        echo -e "${YELLOW}---------------Environment Variable File Already Exists---------------${WHITE}"
        echo 'Would you like to recreate serviceEnvVariables file? (y/n)'
        read USER_RESPONSE
        if [[ ${USER_RESPONSE} == "y" ]]; then
            createFile
        fi
    fi
    echo -e "${YELLOW}---------------Exporting Environment Variables---------------${WHITE}"
    set -o allexport; source serviceEnvVariables; set +o allexport
}

function createFile {
    echo -e "Enter HUB_BASE_URL:${WHITE}"
    read HUB_BASE_URL

    echo "TEMP_FILE_NAME=/home/pi/temperature_settings.json" > serviceEnvVariables
    echo "HUB_BASE_URL=${HUB_BASE_URL}" >> serviceEnvVariables
}


stopService
cloneServiceFiles
startVirtualEnv
installDependencies
createEnvironmentVariableFile
copyServiceFile
configureSystemD
restartDevice