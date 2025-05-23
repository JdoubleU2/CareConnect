# CareConnect
Developer Repository for the Software Surgeons' 'CareConnect' project

[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/JdoubleU2/CareConnect)](https://github.com/JdoubleU2/CareConnect/pulls)
[![Tests Passing](https://github.com/JdoubleU2/CareConnect/workflows/Snowflake%20Snowpark%20CI/CD%20Prod/badge.svg)](https://github.com/JdoubleU2/CareConnect/actions)
[![GitHub Contributors](https://img.shields.io/github/contributors/JdoubleU2/CareConnect)](https://github.com/JdoubleU2/CareConnect/graphs/contributors)
[![GitHub Stars](https://img.shields.io/github/stars/JdoubleU2/CareConnect?style=social)](https://github.com/JdoubleU2/CareConnect/stargazers)

## 📌 Table of Contents  
- [Overview](#overview)  
- [Model Information](#model-information)  
- [Web Application](#web-application)
- [Installation & Usage](#installation--usage)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)  

## 🚀 Overview  
CareConnect is an AI-powered health chatbot developed by The Software Surgeons and sponsored by Google. It provides **general health advice, treatment suggestions, and medical facility recommendations**. The chatbot leverages **LLM-based medical insights** while ensuring responsible AI usage.

## 🤖 CareConnect Model on Hugging Face  
The latest CareConnect model is hosted on **Hugging Face**. You can pull and run it using `ollama`.  

🔗 **Hugging Face Repository:** 
[careconnect-llama3.2-3b](https://huggingface.co/JdoubleU/careconnect-llama3.2-3b)  
careconnect-gemma3-4b coming soon....

### Run the Model Locally  
To run the model with `ollama`, use:  
```sh
ollama run hf.co/JdoubleU/careconnect-llama3.2-3b
```

## 🌐 Web Application
CareConnect is available as a web application with the following architecture:

### Frontend
- Hosted on Firebase at [https://softwaresurgeons.web.app/](https://softwaresurgeons.web.app/)
- Modern, responsive web interface
- Built with React and Firebase Hosting

### Backend
- Located in the `/app` directory
- Python-based server application
- Hosted on Google Cloud Run
- Docker containerized for easy deployment
- Includes comprehensive testing suite (`test_server.py`)

### Local Development
To run the web application locally:
1. Navigate to the `/app` directory
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```sh
   python main.py
   ```

## 🔄 Pulling and Syncing the Repository  

Clone the repository:  
```sh
git clone https://github.com/JdoubleU2/CareConnect.git
```

Update and sync the latest changes:  
```sh
git fetch -p
git merge origin/main
git submodule sync
git submodule update --init --recursive
```

## 🤝 Contributing  
We welcome contributions! To contribute:  

1. Fork the repository  
2. Create a new branch (`git checkout -b feature-branch`)  
3. Commit your changes (`git commit -m "Added feature XYZ"`)  
4. Push the branch (`git push origin feature-branch`)  
5. Open a Pull Request  

## 📜 License  
This project is licensed under [MIT License](LICENSE).  

## 📞 Contact  
For questions or collaborations, reach out:  
📧 Email: Team Lead & LLM Training Lead: Jabin Wade [jwade23@pvamu.edu](mailto:Jwade23@pvamu.edu)

📧 Email: Lead Data Engineer: Zero Nelson [jnelson50@pvamu.edu](mailto:jnelson50@pvamu.edu) 

📧 Email: Lead Web Developer: Aubrey Lister [alister3@pvamu.edu](mailto:alister3@pvamu.edu)  

📧 Email: Lindsey Littlejohn [llittlejohn@pvamu.EDU](mailto:llittlejohn@PVAMU.EDU)  
