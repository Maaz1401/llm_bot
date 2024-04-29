## Installation
1. Install tesseract-ocr for the platform on which the application is being run
-------------------------------------------------------------------------
    First you should install binary:
    On Linux
        sudo apt-get update
        sudo apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
    On Mac
        brew install tesseract
    On Windows
        download binary from https://github.com/UB-Mannheim/tesseract/wiki. then add pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' to your script.

    references: https://pypi.org/project/pytesseract/ (INSTALLATION section) and https://tesseract-ocr.github.io/tessdoc/Installation.html
-------------------------------------------------------------------------
2. pip install -r requirements.txt
3. (Optional) For locally hosted llama gpt, install docker on your system, then run the following commands
    docker pull ollama/ollama
    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    docker exec -it ollama ollama run llama3
    After running the last command, llama3 model will start downloading.     

## Usage
1. Add OpenAI api key in settings file in the variable OPENAI_API_KEY
2. python manage.py makemigrations
3. python manage.py migrate
4. python add_permission.py
5. python populate.py
6. python manage.py runserver


## FOR DOCKER CONTAINER (Run in container)
1. apt-get install libgl1-mesa-glx
2. apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn