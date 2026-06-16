PurpleSynapz Vulnerable AI ChatBot 

Overview : 
    PurpleSynapz Vulnerable AI ChatBot is a Flask based web application designed for AI security learning and security awareness training. 
    The application intentionally contains vulnerable AI chatbot behaviors that can be used to understand prompt injection attacks, 
    data leakage risks, insecure AI implementations, and other AI security concepts.
    The chatbot uses local Large Language Models (LLMs or SLMs) through Ollama and implements a Retrieval Augmented Generation (RAG) pipeline containing simulated sensitive information for educational demonstrations.

Important Warning:
    ⚠️ Educational Purpose Only
    This project is intentionally designed for training and learning purposes.
    DO NOT use this application in production environments.
    The application may contain intentionally vulnerable configurations, insecure logic, and demonstration code that could expose sensitive information if deployed in a real world environment.


Features:
    *AI Chat Interface
        Interactive AI chatbot powered by local LLMs.
        Uses Ollama for model execution.
        Supports conversational interactions through a web interface.
    *Retrieval Augmented Generation (RAG)
        Document based knowledge retrieval.
        Embedding generation using local embedding models.
        Context aware responses.

Technology Stack:
    Component	                                        -- Technology
    Backend	                                            -- Python
    Framework	                                        -- Flask
    LLM Runtime	                                        -- Ollama
    Language Model	                                    -- Llama 3.2
    Embedding Model	                                    -- Nomic Embed Text
    Retrieval System	                                -- RAG
    Frontend	                                        -- HTML, CSS, etc.

Project Architecture:

    User → Flask Application → RAG Pipeline → Ollama LLM

    User submits a query.
    Relevant documents are retrieved from the knowledge base.
    Context is appended to the prompt.
    Prompt is sent to the local LLM.
    Response is returned to the user.

Requirements:
    Hardwares:
        1.Minimum Requirements :
            1.CPU 	            -- Dual-Core Processor
            2.RAM	            -- 8 GB
            3.Storage	        -- 10 GB Free Disk Space
            4.Operating System	-- Windows 10/11, Ubuntu 22.04+, or equivalent Linux distribution
            5.Network	        -- Internet connection required for initial model downloads
        2.Recommended Requirements (for best operation).
            1.CPU               -- Quad-Core Processor or higher.
            2.RAM	            -- 16 GB or more.
            3.Storage	        -- 20 GB+ SSD Free Space.
            4.GPU               -- Optional (NVIDIA GPU with CUDA support for improved performance).
            5.Network           -- Stable broadband connection.

    1.Python 3.13+
        Ensure that Python 3.13 or later is installed on your system.

    Python Installation

        1.Windows:
            if already python is installed verify python:
                python --version

            if not installed follow the step to install python:

            1. Download Python from:
            https://www.python.org/downloads/
		Download Python Install Manager

            2. Run the installer.

            3. During installation, enable:
                Add Python to PATH

            4. Verify the installation:
                python --version

        2.Linux

            if already python is installed verify python:
                python3 --version

            if not installed follow the step to install python:
                sudo apt update
                sudo apt install python3 python3-pip -y

            Verify the installation:
            python3 --version

    2. Ollama Installation

        1. Linux:
            1. Install Ollama:
                Visit: https://ollama.com/download

                Or install using:
                    curl -fsSL https://ollama.com/install.sh | sh

            2. Verify Installation
                ollama --version

            3. Verify Ollama Service

                Ensure that the Ollama service is running.

                    Open a web browser and navigate to:
                        http://127.0.0.1:11434/

                    If Ollama is running successfully, you should see a response similar to:

                        Ollama is running

            4. Download Required Models
                ollama pull llama3.2:3b
                ollama pull nomic-embed-text:latest
        
            5. Verify Downloaded Models
                ollama list


        2. Windows:
            1. Download Ollama from:
                https://ollama.com/download

            2. Run the installer and complete the installation.

            3. Open Command Prompt and verify the installation:
                ollama --version

            4. Verify Ollama Service:
                Ensure that the Ollama service is running.

                    Open a web browser and navigate to:
                        http://127.0.0.1:11434/

                    If Ollama is running successfully, you should see a response similar to:
                        Ollama is running
        

            5. Go to the Cmd Prompt and Download the required models:
		Paste the cmd in the cmd prompt
               	 >ollama pull llama3.2:3b
               	 >ollama pull nomic-embed-text:latest

            6. Verify the downloaded models:
                ollama list

            7. installed models
                NAME                       ID              SIZE      MODIFIED
		nomic-embed-text:latest    0a109f422b47    274 MB    15 seconds ago
		llama3.2:3b                a80c4f17acd5    2.0 GB    35 seconds ago

Installation:
    1. Download the Project

        Repository URL:
            https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot   

        1: Clone Using Git:

            git clone https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot.git

        2: Download ZIP:
            1. Open the repository URL in your browser.
            2. Click **Code**.
            3. Select **Download ZIP**.
            4. Extract the downloaded ZIP file.
            5. Open a terminal or command prompt in the extracted project directory.

        3: GitHub Desktop:
            1. Open the repository URL.
            2. Click **Code** → **Open with GitHub Desktop**.
            3. Choose a local directory and clone the repository.



    2. Create Virtual Environment by executing the commands in Terminal/Command Prompt till step 4

        Linux:
            cd PurpleSynapz-Vulnerable-Ai-ChatBot
            python -m venv myworld
            source myworld/bin/activate

        Windows:
            cd PurpleSynapz-Vulnerable-Ai-ChatBot
            python -m venv myworld
            myworld\Scripts\activate

    3. Install Dependencies
        pip install -r requirements.txt

    4. Start Application
        python main.py

    5. The application will be available at:
        http://127.0.0.1:9000

Creating a User Account

    The application provides a Register option for creating a new user account.

    Steps to Register:
        1.Open the application in your browser.
        2.Click the Register button on the login page.
        3.Enter the required information:
            Username
            Password
        4.Submit the registration form.
        5.After successful registration, log in using your newly created credentials.

    User Role:
        1.When registered through the Register option, the account is assigned the User role.
        2.Users with this role have access only to the chatbot functionality and can:
            1.Log in to the application.
            2.Interact with the AI chatbot.
            3.Submit chat queries and receive responses.

    Note: The User role does not have access to Admin features like updating knowledge base.

Updating the Knowledge Base:
    To update the knowledge base, users must log in with an Admin account.

    1.Open the application in your browser.
    2.Log in using credentials:
        username: admin,
        password:admin@123
    3.Navigate to the Upload Knowledge File section.
    4.Upload the new pdf or txt files.
    5.Click the 'upload to db' to update the knowledge base used by the RAG system.

    Note:Only users with the Admin credentials are authorized to upload knowledge base content.

⚠️ Disclaimer:
    The authors, contributors, and PurpleSynapz are not responsible for any misuse of this project.
    This Application is provided for educational and training purposes only. Users are responsible for ensuring compliance with applicable laws, regulations, and policies.

Contact
    For any questions, issues, or support requests,
    please contact: info@purplesynapz.com