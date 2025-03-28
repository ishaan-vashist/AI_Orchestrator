from fastapi import FastAPI
from pydantic import BaseModel
import os
import docker
import tempfile
from pathlib import Path, PureWindowsPath
from orchestrator import groq_client

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
    plan = groq_client.get_task_plan(data.user_request)
    current_text = data.text
    task_outputs = {}  # ✅ Store output per task

    workdir = tempfile.mkdtemp(prefix="orchestrator_")

    for task in plan:
        image = TASK_IMAGE_MAP.get(task)
        if not image:
            return {"error": f"Unknown task: {task}"}

        # Save input for this task
        input_path = os.path.join(workdir, f"input_{task}.txt")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(current_text)

        # Normalize path for Docker
        abs_path = Path(input_path).resolve()
        docker_input_path = str(PureWindowsPath(abs_path))

        print(f"[DEBUG] Running task: {task}")
        print(f"[DEBUG] Mounting: {docker_input_path}")

        try:
            output = docker_client.containers.run(
                image=image,
                volumes={docker_input_path: {"bind": "/data/input.txt", "mode": "ro"}},
                remove=True
            )
            result = output.decode("utf-8").strip()
            task_outputs[task] = result
            current_text = result  # pass to next task

        except Exception as e:
            print(f"[ERROR] Task failed: {task} — {str(e)}")
            return {"error": f"Failed running {task}: {str(e)}"}

    print(f"[DEBUG] Final result: {current_text}")
    return {
        "plan": plan,
        "outputs": task_outputs,
        "final_result": current_text
    }
