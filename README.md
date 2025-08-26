# AI-AGENT
This project is a simple **LangChain-powered AI Agent** that connects to OpenAI’s GPT models using your own API key.  
It demonstrates how to set up environment variables securely and run an AI assistant locally. 
It research about the given prompt and creates a text in defined format that is saved in a text file.

---

## 📌 Features
- Uses **LangChain** to manage LLM prompts & responses  
- Integrates **OpenAI GPT models** (`gpt-4o-mini`)  
- Loads API keys securely with `.env`  
- Example chatbot interaction in `main.py`  

---
## Create & activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt


## Add your OpenAI API key inside it:
OPENAI_API_KEY=sk-your-real-api-key

## TO run the main script
python main.py
