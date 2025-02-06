***

# STOP AND READ

***

## This will be the source code for training our model. You will need the following to get started.

unsloth: https://github.com/unslothai/unsloth

CUDA (if you have a GPU): https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_network

ollama: https://ollama.com/

***

Windows setup:
##### 1. Setup WSL for Windows    

Open Powershell

`wsl --install`

##### 2. install VsCode in WSL

Go to VsCode website download the linux version of VsCode.

Put this version inside linux distro

inside WSL shell...

    sudo dpkg -i code_1.96.4-1736991114_amd64.deb

    sudo apt update
    sudo apt install -f

Open VsCode

    Code


##### 3. Install MiniConda on WSL

    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3/
    ~/miniconda3/bin/conda init bash

Close and re-open shell 

***

Setup Enviroment 

### Create Conda Enviroment (This takes a while)
    
    conda create --name unsloth_env python=3.11 pytorch-cuda=12.1 pytorch cudatoolkit xformers -c pytorch -c nvidia -c xformers -y
