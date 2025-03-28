from fastapi import FastAPI
from pydantic import BaseModel
import os
import docker
import tempfile
import logging
from pathlib import Path, PureWindowsPath
from orchestrator import groq_client
from docker.errors import DockerException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

app = FastAPI()
docker_client = docker.from_env()

TASK_IMAGE_MAP = {
    "clean_text": "ai_clean_text",
    "sentiment_analysis": "ai_sentiment_analysis",
    "summarization": "ai_summarization"
}

class RequestInput(BaseModel):
    user_request: str
    text: str

@app.post("/process_request")
def process_request(data: RequestInput):
    try:
        plan = groq_client.get_task_plan(data.user_request)
    except Exception as e:
        logger.error(f"[LLM ERROR] Failed to get task plan: {e}")
        return {"error": "Failed to generate task plan from LLM."}

    current_text = data.text
    task_outputs = {}

    try:
        workdir = tempfile.mkdtemp(prefix="orchestrator_")
    except Exception as e:
        logger.error(f"[DIR ERROR] Failed to create temp directory: {e}")
        return {"error": "Internal error: Could not create working directory."}

    for task in plan:
        image = TASK_IMAGE_MAP.get(task)
        if not image:
            return {"error": f"Unknown task: {task}"}

        input_path = os.path.join(workdir, f"input_{task}.txt")
        try:
            with open(input_path, "w", encoding="utf-8") as f:
                f.write(current_text)
        except Exception as e:
            logger.error(f"[FILE ERROR] Failed to write input file: {e}")
            return {"error": "Internal error writing input file."}

        abs_path = Path(input_path).resolve()
        docker_input_path = str(PureWindowsPath(abs_path))

        logger.info(f"[TASK] Running: {task}")
        logger.debug(f"[TASK] Mounting: {docker_input_path}")

        try:
            output = docker_client.containers.run(
                image=image,
                volumes={docker_input_path: {"bind": "/data/input.txt", "mode": "ro"}},
                remove=True
            )
            result = output.decode("utf-8").strip()
            logger.info(f"[OUTPUT] {task}: {result[:100]}...")  # limit preview length
            task_outputs[task] = result
            current_text = result

        except DockerException as e:
            logger.error(f"[DOCKER ERROR] Task failed: {task} — {str(e)}")
            return {"error": f"Failed running {task}: Docker error."}

        except Exception as e:
            logger.error(f"[RUNTIME ERROR] Task failed: {task} — {str(e)}")
            return {"error": f"Failed running {task}: Unexpected error."}

    logger.info(f"[RESULT] Final output ready.")
    return {
        "plan": plan,
        "outputs": task_outputs,
        "final_result": current_text
    }
