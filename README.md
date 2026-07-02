PurpleSynapz Vulnerable AI ChatBot 

# Overview : 
    PurpleSynapz Vulnerable AI ChatBot is a Flask based web application designed for AI security learning and security awareness training. 
    The application intentionally contains vulnerable AI chatbot behaviors that can be used to understand prompt injection attacks, 
    data leakage risks, insecure AI implementations, and other AI security concepts.
    The chatbot uses local Large Language Models (LLMs or SLMs) through Ollama and implements a Retrieval Augmented Generation (RAG) pipeline containing simulated sensitive information for educational demonstrations.

# Important Warning:
    ⚠️ Educational Purpose Only
    This project is intentionally designed for training and learning purposes.
    DO NOT use this application in production environments.
    The application may contain intentionally vulnerable configurations, insecure logic, and demonstration code that could expose sensitive information if deployed in a real world environment.

# Getting Started with the Vulnerable AI ChatBot
    Follow the installation steps given in Requirements and ensure all required services are running. Once the setup is complete, open the web application in your browser. You will now have access to the chatbot, which is connected to a Retrieval-Augmented Generation (RAG) knowledge base containing sample documents, including general information, company related data, and intentionally sensitive information

    # What to Explore
        Use the Chat page to interact with the AI assistant and explore the knowledge base. and observe how the chatbot responds.
        The sample RAG database contains information such as:
        - Login credentials
        - General company information
        - Employee details
        - Internal company documents
        - Customer information
        - Financial records
        - Other confidential information intentionally included for security testing.
        
# Objective
    Your goal is to interact with the chatbot using different types of query and determine whether the AI reveals confidential information stored in the RAG database. 
    You can experiment with:
    - Direct questions about company data (note: simple direct questions like asking for annual income may not return answers)
    - Use Prompt injection attempts
    - Use Indirect or role playing queries
    - Other different techniques to gradually extract restricted information.
    - Attempts to retrieve sensitive company details such as employee phone numbers, salary information, PAN number, registration number, login credentials, profit information, what are servers are being used and other confidential data using any possible technique.

# Test Feature:
    After using different techniques to identify and extract sensitive information from the chatbot, you can use the Take Test feature to verify whether the collected information is accurate.
      
    Answer via Bot Query:
        - Users can interact with the chatbot directly within the test interface.
        - For each question, users are provided up to 3 chatbot queries (attempts) to retrieve the required information before submitting their answer.
        - This mode evaluates whether the chatbot reveals confidential information when users actively attempt different querying techniques during the test.
    
    Note: The purpose of the Take Test feature is to verify whether the information collected from the chatbot is correct or not after attempting to retrieve it using different querying techniques.

# Features:
    *AI Chat Interface
        Interactive AI chatbot powered by local LLMs.
        Uses Ollama for model execution.
        Supports conversational interactions through a web interface.
    *Retrieval Augmented Generation (RAG)
        Document based knowledge retrieval.
        Embedding generation using local embedding models.
        Context aware responses.

# Technology Stack:
    Component	                                        -- Technology
    Backend	                                            -- Python
    Framework	                                        -- Flask
    LLM Runtime	                                        -- Ollama
    Language Model	                                    -- Llama 3.2
    Embedding Model	                                    -- Nomic Embed Text
    Retrieval System	                                -- RAG
    Frontend	                                        -- HTML, CSS, etc.

# Project Architecture:

    User → Flask Application → RAG Pipeline → Ollama LLM
    User submits a query.
    Relevant documents are retrieved from the knowledge base.
    Context is appended to the prompt.
    Prompt is sent to the local LLM.
    Response is returned to the user.

# Requirements:
    1. Hardwares:
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

    2.Python 3.12+
    3.Ollama 0.30+ 

    # Installation of Python and Ollama for (Windows 10/11)
            execute below commands in Terminal/Command Prompt

    
        - Python Installation:
            if already python is installed verify python:
                python --version                 -- Verify that Python 3.12 or later is installed.

            if not installed follow the step to install python:

                1. Download Python from:
                https://www.python.org/downloads/
                    Download Python Install Manager

                2. Run the installer.

                3. During installation, enable:
                    Add Python to PATH

                4. Verify the installation:
                    python --version            -- Verify that Python 3.12 or later is installed.

        - ollama Installation:
            1. Download Ollama from:
                https://ollama.com/download

            2. Run the installer and complete the installation.

            3. Open Command Prompt and verify the installation:
                ollama --version                -- Verify that Ollama v0.30.0 or later is installed.

            4. Verify Ollama Service:
                Ensure that the Ollama service is running.

                    Open a web browser and navigate to:
                        http://127.0.0.1:11434/

                    If Ollama is running successfully, you should see a response similar to:
                        Ollama is running

            5. open command prompt and download the models:
                ollama pull llama3.2:3b
               	ollama pull nomic-embed-text:latest

            6. Verify the downloaded models:
                ollama list                 -- you should see the download models

    # Project Installation in (Windows 10/11)
        Repository URL:
            https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot   

        Choose any one way to install github Repository:
            1: Clone Using Git:
                git clone https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot.git

            2: Download ZIP:
                1. Open the repository URL in your browser.
                2. Click **Code**.
                3. Select **Download ZIP**.
                4. Extract the downloaded ZIP file (the extracted folder may be named   PurpleSynapz-Vulnerable-Ai-ChatBot-main replace that to PurpleSynapz-Vulnerable-Ai-ChatBot).
                5. Open a terminal or command prompt in the extracted project directory.

            3: GitHub Desktop:
                1. Open the repository URL.
                2. Click **Code** → **Open with GitHub Desktop**.
                3. Choose a local directory and clone the repository.

    # Create Virtual Environment by executing the commands in Terminal/Command Prompt

        cd PurpleSynapz-Vulnerable-Ai-ChatBot
        python -m venv myworld
        myworld\Scripts\activate

    # Install Dependencies
        pip install -r requirements.txt

    # Start Application
        python main.py

    # The application will be available at:
        application url: http://127.0.0.1:7000



    # Installation of Python and Ollama for (Ubuntu 22.04+)
        execute below commands in Terminal/Command Prompt

        - Python Installation:
            if already python is installed verify python:
                python3 --version                   -- Verify that Python 3.12 or later is installed.

            if not installed follow the step to install python:
                sudo apt update
                sudo apt install python3 python3-pip python3-venv -y

            Verify the installation:
                python3 --version                   -- Verify that Python 3.12 or later is installed.

        - ollama Installation:
            1. Install Ollama:
                Visit: https://ollama.com/download
            Or install using:
                curl -fsSL https://ollama.com/install.sh | sh

            2. Verify Installation
                ollama --version                    -- Verify that Ollama v0.30.0 or later is installed.

            3. Verify Ollama Service:
                Ensure that the Ollama service is running by performing curl operation.
                curl http://127.0.0.1:11434/

            
            4. Download Required Models
                ollama pull llama3.2:3b
                ollama pull nomic-embed-text:latest
        
            5. Verify Downloaded Models
                ollama list         -- you should see the download models
    
    # Project Installation in (Ubuntu 22.04+)
        Repository URL:
            https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot   

        Choose any one way to install github Repository:
            1: Clone Using Git:
                git clone https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot.git

            2: Download ZIP:
                1. Open the repository URL in your browser.
                2. Click **Code**.
                3. Select **Download ZIP**.
                4. Extract the downloaded ZIP file (the extracted folder may be named   PurpleSynapz-Vulnerable-Ai-ChatBot-main replace that to PurpleSynapz-Vulnerable-Ai-ChatBot).
                5. Open a terminal or command prompt in the extracted project directory.

            3: GitHub Desktop:
                1. Open the repository URL.
                2. Click **Code** → **Open with GitHub Desktop**.
                3. Choose a local directory and clone the repository.

    # Create Virtual Environment by executing the commands in Terminal/Command Prompt

        cd PurpleSynapz-Vulnerable-Ai-ChatBot
        python3 -m venv myworld
        source myworld/bin/activate

    # Install Dependencies
        pip install -r requirements.txt
        or 
        pip3 install -r requirements.txt

    # Start Application
        python3 main.py

    # If the system is running the Linux/Ubuntu desktop version, the application will be available at:
        available url: http://127.0.0.1:7000

    # If it is running on a server, update the application host configuration in config.py with the server/VM IP address.
    - stop the application for command prompt/terminal:
        press: Ctrl + c

    # Steps to update config.py
        - To open the config.py file, open a command prompt/terminal, navigate to the application directory, and open the file using a text editor such as nano, vim, or gedit.
        - run this in project directory PurpleSynapz-Vulnerable-Ai-ChatBot:
            nano config.py
        - Locate the following line:
            host = _get_env("APP_HOST", "127.0.0.1")

        - Replace 127.0.0.1 with the IP address of your server or VM. 
        For example:
            host = _get_env("APP_HOST", "192.168.1.100")
        - Save the changes to config.py:
            press: Ctrl+o     - to write 
            here:File Name to write: config.py - press Enter    - to apply
            press: Ctrl+x      - to exit

        - Start Application:
            python3 main.py

        - The application will be available at:
            application url: http://<sever_or_vm_ip>:7000



    # Installation of Python and Ollama for macOS:
        execute below commands in Terminal/Command Prompt
        -Python Installation:
            If Python is already installed, verify:
                python3 --version                        -- Verify that Python 3.12 or later is installed.

            if not installed follow the step to install python:

                1. Download Python from:
                https://www.python.org/downloads/macos/
                    Download Latest Python 3 Release

                2. Run the installer and follow the installation wizard.

                3. Verify the installation:
                    python3 --version                   -- Verify that Python 3.12 or later is installed.

        - ollama Installation:
            1. Install Ollama:
                Visit: https://ollama.com/download
                - choose Macos and click on the download for macos

            2. Verify Installation use 
                ollama --version                     -- Verify that Ollama v0.30.0 or later is installed.

            3. Verify Ollama Service:
                Ensure that the Ollama service is running performing curl operation.
                curl http://127.0.0.1:11434/
                
                - ollama is not running:
                    ollama serve

                    perform step 3 to Verify Ollama Service 

            4. Download Required Models
                ollama pull llama3.2:3b
                ollama pull nomic-embed-text:latest
        
            5. Verify Downloaded Models
                ollama list         -- you should see the download models

    # Project Installation in Macos:
        Repository URL:
            https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot   

        Choose any one way to install github Repository:
            1: Clone Using Git:
                git clone https://github.com/purpleSynapz/PurpleSynapz-Vulnerable-Ai-ChatBot.git

            2: Download ZIP:
                1. Open the repository URL in your browser.
                2. Click **Code**.
                3. Select **Download ZIP**.
                4. Extract the downloaded ZIP file (the extracted folder may be named   PurpleSynapz-Vulnerable-Ai-ChatBot-main replace that to PurpleSynapz-Vulnerable-Ai-ChatBot).
                5. Open a terminal or command prompt in the extracted project directory.

            3: GitHub Desktop:
                1. Open the repository URL.
                2. Click **Code** → **Open with GitHub Desktop**.
                3. Choose a local directory and clone the repository.

    # Create Virtual Environment by executing the commands in Terminal/Command Prompt

        cd PurpleSynapz-Vulnerable-Ai-ChatBot
        python3 -m venv myworld
        source myworld/bin/activate

    # Install Dependencies
        pip install -r requirements.txt
        or 
        pip3 install -r requirements.txt

    # Start Application
        python3 main.py

    # The application will be available at:
        application url: http://127.0.0.1:7000



# Creating a User Account
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
            4.After attempting to retrieve sensitive information from the chatbot, use the **Test** feature and answer the questions using the **Ask Bot** option, which allows you to query the chatbot directly to retrieve the required information.
    
    admin Role:
        1. Open the application in your browser.
        2. Log in using the admin credentials:
            - **Username:** admin
            - **Password:** admin@123
        3. After logging in, admin can:
            - Interact with the AI chatbot through the **Chat** page.
            - View the documents available in the knowledge base through the **Available Docs** section.
            - Create tests for users.
            - View user performance and test results through the performance dashboard.

# ⚠️ Disclaimer:
    The authors, contributors, and PurpleSynapz are not responsible for any misuse of this project.
    This Application is provided for educational and training purposes only. Users are responsible for ensuring compliance with applicable laws, regulations, and policies.

# Contact
    For any questions, issues, or support requests,
    please contact: info@purplesynapz.com
