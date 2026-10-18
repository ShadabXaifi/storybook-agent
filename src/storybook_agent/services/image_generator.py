
import json
import os
import time
import random
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "sd15_txt2img_api.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")
NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, watermark, text, bad anatomy"
)


def generate_image(
    prompt: str,
    filename: str = "test_image.png",
    timeout: int = 300,
) -> Path:
    """Generate an image through the local ComfyUI API."""

    if not prompt.strip():
        raise ValueError("Image prompt cannot be empty.")

    if not WORKFLOW_PATH.is_file():
        raise FileNotFoundError(
            f"ComfyUI workflow not found: {WORKFLOW_PATH}"
        )

    with WORKFLOW_PATH.open("r", encoding="utf-8") as file:
        workflow = json.load(file)

    # Replace the positive and negative prompts.
    workflow["3"]["inputs"]["text"] = prompt
    workflow["5"]["inputs"]["text"] = NEGATIVE_PROMPT

    # Use a different seed for each generated image.
    workflow["7"]["inputs"]["seed"] = random.randint(
        0, 2**32 - 1
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client_id = f"storybook-{random.randint(1, 10**12)}"

    response = requests.post(
        f"{COMFYUI_URL}/prompt",
        json={
            "prompt": workflow,
            "client_id": client_id,
        },
        timeout=30,
    )
    response.raise_for_status()
    prompt_id = response.json()["prompt_id"]

    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        history_response = requests.get(
            f"{COMFYUI_URL}/history/{prompt_id}",
            timeout=30,
        )
        history_response.raise_for_status()

        history = history_response.json().get(prompt_id)

        if history:
            status = history.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(
                    f"ComfyUI image generation failed: {status}"
                )

            outputs = history.get("outputs", {})

            for node_output in outputs.values():
                for image_info in node_output.get("images", []):
                    image_response = requests.get(
                        f"{COMFYUI_URL}/view",
                        params={
                            "filename": image_info["filename"],
                            "subfolder": image_info.get("subfolder", ""),
                            "type": image_info.get("type", "output"),
                        },
                        timeout=60,
                    )
                    image_response.raise_for_status()

                    output_path = Path(filename)
                    if not output_path.is_absolute():
                        output_path = OUTPUT_DIR / output_path
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(image_response.content)
                    return output_path

        time.sleep(2)

    raise TimeoutError(
        f"ComfyUI did not finish generating the image within {timeout} seconds."
    )
