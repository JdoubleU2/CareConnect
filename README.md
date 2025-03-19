# CareConnect
Developer Repository for the Software Surgeons 'CareConnect' project 


<a href="https://github.com/JdoubleU2/CareConnect/actions">
    <img alt="Tests Passing" src="https://github.com/JdoubleU2/CareConnect/workflows/Snowflake%20Snowpark%20CI/CD%20Prod/badge.svg" />
</a>
<a href="https://github.com/JdoubleU2/CareConnect/graphs/contributors">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/JdoubleU2/CareConnect" />
</a>


# Hugging Face repository for latest CareConnect model

Hugging Face: https://huggingface.co/JdoubleU/careconnect-llama3.2-3b

run the model with ollama 
    
    ollama run hf.co/JdoubleU/careconnect-llama3.2-3b

# How to pull and sync updates to this repostiory 
    git clone https://github.com/JdoubleU2/CareConnect.git

    git fetch -p
    git merge origin/main
    git submodule sync
    git submodule update --init --recursive

