***

# STOP AND READ

***

## This will be the source code for finetuning our model. You will need the following to get started.

unsloth: https://github.com/unslothai/unsloth

CUDA (if you have a GPU): https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_network

ollama: https://ollama.com/

Hugging Face (account and access token): https://huggingface.co

tutorial: https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.2_(1B_and_3B)-Conversational.ipynb#scrollTo=C_sGp5XlG6dq

***

## Windows setup:
### 1. Setup WSL for Windows    

Open Powershell

`wsl --install`

### 2. install VsCode in WSL

Go to VsCode website download the linux version of VsCode.

Put this version inside linux distro

inside WSL shell...

    sudo dpkg -i code_1.96.4-1736991114_amd64.deb

    sudo apt update
    sudo apt install -f

Open VsCode

    Code


### 3. Install MiniConda on WSL

    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3/
    ~/miniconda3/bin/conda init bash

Close and re-open shell 

***

## Setup Enviroment 

### 1. Create Conda Enviroment (This takes a while)
    
    conda create --name unsloth_env python=3.11 pytorch-cuda=12.1 pytorch cudatoolkit xformers -c pytorch -c nvidia -c xformers -y

Open Enviroment

    conda activate unsloth_env

Install unsloth

    pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

Install other dependencys

    pip install --no-deps trl peft accelerate bitsandbytes


### Oh yea. Now were cooking. 

***

## MAC Setup (ARM)

### 1. Install miniconda

    mkdir -p ~/miniconda3
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh

### 2. Close and reopen terminal 

    source ~/miniconda3/bin/activate

### 3. Close and reopen terminal 

    conda init --all

## Create enviorment 

    conda create --name unsloth_env python=3.11 pytorch torchvision torchaudio -c pytorch -y

### 1. Open Enviroment

    conda activate unsloth_env

### 2. Install Packages to run without GPU 

(If you made it this far and think you plan on training the model on MAC.... i got bad news for ya)

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
    pip install tensorflow-macos tensorflow-metal



You also could just run the finetune.ipynb file in google collab. Sorry ou had to scroll so far to see this lol.

## Training hosted by Google Colab

### 1. Clone repository into Google Colab or Export finetune.ipynb to Google Colab Notebook 

### 2. Use Google hosted GPU
    Runtime -> Change Runtime Type -> Select GPU

### 3. Import training data into Google Colab

### 4. Add your huggingface token to save your created model to huggingface  

#### 4.1 Go to hugging face huggingface.co generate a Access Token https://huggingface.co/settings/tokens 

#### 4.2 In finetune.ipynb scroll down to the "Local Saving" Section and paste your generated write token 
    from huggingface_hub import login
    #put your login stuff here
    #login("Your token here")
    
Your Model will be saved at https://huggingface.co/<YourUserName>/careconnect-llama3.2-3b. From here, you can obtain the ollama command to run the model with ollama 



