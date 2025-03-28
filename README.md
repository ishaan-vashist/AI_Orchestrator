📘 README.md
markdown
Copy
Edit
#  AI Task Orchestrator

The AI Task Orchestrator is a modular application that uses LLMs and containerized NLP microservices to automate a sequence of tasks like cleaning text, sentiment analysis, and summarization — all based on natural language instructions.

---

## Features

-  Web UI built with Streamlit
-  FastAPI-based backend orchestrator
-  Groq LLM (or OpenAI fallback) for parsing task flows from user input
-  Dockerized NLP tasks:
  - `clean_text`
  - `sentiment_analysis`
  - `summarization`
-  Automatically executes tasks in a pipeline
-  Easily extendable with new tasks
-  Works cross-platform (Windows-safe paths handled)

---

##  Project Structure

ai-orchestrator/ │ ├── orchestrator/ # FastAPI backend │ ├── groq_client.py # Sends prompt to Groq and parses task plan │ ├── main.py # FastAPI server with task runner │ └── tasks_plan_prompt.txt # Prompt template for LLM │ ├── streamlit_app/ │ └── app.py # Streamlit UI frontend │ ├── tasks/ # Dockerized NLP microservices │ ├── clean_text/ │ │ ├── Dockerfile │ │ └── app.py │ │ │ ├── sentiment_analysis/ │ │ ├── Dockerfile │ │ ├── input.txt # Sample input │ │ └── app.py │ │ │ └── summarization/ │ ├── Dockerfile │ └── app.py

yaml
Copy
Edit

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo>
cd ai-orchestrator
2. Create .env File
Inside orchestrator/, create a .env file:

ini
Copy
Edit
GROQ_API_KEY=your_actual_key_here
3. Create and Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate    # macOS/Linux
4. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If no requirements.txt yet, install manually:

bash
Copy
Edit
pip install fastapi uvicorn docker python-dotenv requests streamlit
🐳 Build Docker Containers
bash
Copy
Edit
# From project root
docker build -t ai_clean_text ./tasks/clean_text
docker build -t ai_sentiment_analysis ./tasks/sentiment_analysis
docker build -t ai_summarization ./tasks/summarization
 Running the Application
1. Start FastAPI Backend
bash
Copy
Edit
uvicorn orchestrator.main:app --reload
2. Run Streamlit Frontend
bash
Copy
Edit
cd streamlit_app
streamlit run app.py
 How It Works
Enter a natural language instruction (e.g., Clean the text and analyze sentiment).

The backend uses Groq to infer the required tasks: ["clean_text", "sentiment_analysis"].

Each task runs in its own Docker container.

Results flow through the pipeline and return to the UI.

 Adding New Tasks
Create a new folder in tasks/<your_task_name>/.

Add:

app.py to process /data/input.txt

Dockerfile to containerize it.

Add mapping in TASK_IMAGE_MAP in orchestrator/main.py.

 Notes
Ensure Docker is installed and running.

This app handles Windows paths carefully using pathlib.

Supports Groq API by default, but you can adapt to OpenAI if needed.

 Acknowledgements
Built as a Backend + DevOps Assignment demonstrating real-world orchestration using:

FastAPI

Docker

Groq LLM

Streamlit

 Author
Your Ishaan – your GitHub








