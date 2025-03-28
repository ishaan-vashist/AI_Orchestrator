# AI Task Orchestrator

The AI Task Orchestrator is a modular application that uses LLMs and containerized NLP microservices to automate a sequence of tasks like cleaning text, sentiment analysis, and summarization based on natural language instructions.

---

## Features

- Web UI built with Streamlit
- FastAPI-based backend orchestrator
- Groq LLM (or OpenAI fallback) for parsing task flows from user input
- Dockerized NLP tasks:
  - clean_text
  - sentiment_analysis
  - summarization
- Automatically executes tasks in a pipeline
- Easily extendable with new tasks
- Works cross-platform (Windows-safe paths handled)
- Robust error handling (LLM failure, file I/O, Docker errors)
- Logs important task activity and errors for debugging

---

## Project Structure

```
ai-orchestrator/
│
├── orchestrator/                # FastAPI backend
│   ├── groq_client.py           # Sends prompt to Groq and parses task plan
│   ├── main.py                  # FastAPI server with task runner
│   └── tasks_plan_prompt.txt    # Prompt template for LLM
│
├── streamlit_app/
│   └── app.py                   # Streamlit UI frontend
│
├── tasks/                       # Dockerized NLP microservices
│   ├── clean_text/
│   │   ├── Dockerfile
│   │   └── app.py
│   │
│   ├── sentiment_analysis/
│   │   ├── Dockerfile
│   │   ├── input.txt            # Sample input
│   │   └── app.py
│   │
│   └── summarization/
│       ├── Dockerfile
│       └── app.py
```

---

## System Architecture

```
                  AI Task Orchestrator
                          |
                +----------------------+
                |  Streamlit UI (User) |
                |----------------------|
                | - User inputs task   |
                | - Sends to API       |
                | - Displays results   |
                +----------------------+
                          |
                          v
                +------------------------+
                | FastAPI Orchestrator   |
                |------------------------|
                | - Calls Groq API       |
                | - Parses task plan     |
                | - Runs tasks in order  |
                | - Collects outputs     |
                +------------------------+
                          |
                          v
      +---------------------+     +----------------------+     +---------------------------+
      |  clean_text         |     | summarization         |     | sentiment_analysis         |
      |---------------------|     |----------------------|     |---------------------------|
      | Docker container    |     | Docker container     |     | Docker container          |
      | Reads input.txt     |     | Reads input.txt      |     | Reads input.txt           |
      | Outputs cleaned text|     | Outputs summary      |     | Outputs sentiment string  |
      +---------------------+     +----------------------+     +---------------------------+
                          |
                          v
                +------------------------+
                |     JSON Response      |
                |------------------------|
                | - plan: [tasks...]     |
                | - outputs: {task: out} |
                | - final_result: string |
                +------------------------+
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo>
cd ai-orchestrator
```

### 2. Create `.env` File

Inside `orchestrator/`, create a `.env` file:

```
GROQ_API_KEY=your_actual_key_here
```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate    # macOS/Linux
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Build Docker Containers

```bash
# From project root
docker build -t ai_clean_text ./tasks/clean_text
docker build -t ai_sentiment_analysis ./tasks/sentiment_analysis
docker build -t ai_summarization ./tasks/summarization
```

---

## Running the Application

### 1. Start FastAPI Backend

```bash
uvicorn orchestrator.main:app --reload
```

### 2. Run Streamlit Frontend

```bash
cd streamlit_app
streamlit run app.py
```

---

## How It Works

1. User submits a natural language task through the UI.
2. FastAPI backend sends the instruction to Groq API.
3. Groq returns an ordered list of NLP tasks.
4. Each task is run inside its Docker container.
5. The orchestrator passes outputs between tasks and returns a complete JSON response.

---

## Notes

- Ensure Docker is installed and running.
- Handles Windows paths using pathlib.
- Logs are printed to console for each task and errors.
- Supports Groq API by default, but OpenAI can be used as fallback.

---

## Acknowledgements

Built as a Backend + DevOps Assignment demonstrating practical orchestration using:
- FastAPI
- Docker
- Groq LLM
- Streamlit

---

## Author

Ishaan Vashist – [your GitHub](https://github.com/ishaan-vashist)
