"""handler.py

Deploys a specified DeepSeek R1 model via Modal, mounting a volume for storing model files.
Runs both Ollama and Open-WebUI in the background.
"""

import time
import subprocess
from pathlib import Path
import logging

import modal
import modal.gpu

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

#: Maps DeepSeek R1 models to corresponding GPU configurations.
DEEPSEEK_R1_MODELS = {
    "deepseek-r1:1.5b": "T4",  # ~1.1GB model
    "deepseek-r1:7b": "T4",    # ~4.7GB model
    "deepseek-r1:8b": "T4",    # ~4.9GB model
    "deepseek-r1:14b": "T4",   # ~9GB  model
    "deepseek-r1:32b": "T4",   # ~20GB model
    "deepseek-r1:70b": modal.gpu.A100(count=2, size="80GB"),  # ~43GB model
    "deepseek-r1:671b": "T4"   # ~404GB model
}

#: Name of the Modal app/deployment.
DEPLOYMENT_NAME = "deepseekr1-openwebui"

#: Path where models will be downloaded and stored.
MODELS_DOWNLOAD_PATH = "/root/models/"

#: Model to deploy (ensure it's present in DEEPSEEK_R1_MODELS).
MODEL = "deepseek-r1:14b"

if MODEL not in DEEPSEEK_R1_MODELS:
    raise ValueError(f"Model '{MODEL}' not found in DEEPSEEK_R1_MODELS.")

# ------------------------------------------------------------------------------
# Modal Volume & Image Definitions
# ------------------------------------------------------------------------------

#: Persistent volume for storing model files.
volume = modal.Volume.from_name(f"{DEPLOYMENT_NAME}-volume", create_if_missing=True)

#: Defines the container image used by the Modal app.
image = (
    modal.Image.debian_slim(python_version="3.11.5")
    .pip_install_from_requirements(Path(__file__).parent / "requirements.txt")
    .apt_install("curl")
    .run_commands(["curl -fsSL https://ollama.com/install.sh | sh"])
    # Clear existing /root/models and remove the directory itself.
    .run_commands(["rm -rf /root/models/*", "rm -rf /root/models"])
    .env({"OLLAMA_MODELS": MODELS_DOWNLOAD_PATH})
)

#: Modal App configuration.
app = modal.App(
    image=image,
    name=f"{DEPLOYMENT_NAME}-app",
    secrets=[modal.Secret.from_name("open-webui-secrets")],
    volumes={MODELS_DOWNLOAD_PATH: volume},
)

# ------------------------------------------------------------------------------
# Serving Function
# ------------------------------------------------------------------------------

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@app.function(
    allow_concurrent_inputs=100,
    gpu=DEEPSEEK_R1_MODELS[MODEL],
    concurrency_limit=1,
    keep_warm=1,
    timeout=60 * 60 * 24
)
@modal.web_server(port=8080, startup_timeout=1200)
def openwebui() -> None:
    """Orchestrate Ollama and Open-WebUI services with error handling."""
    try:
        logger.info("Starting Ollama server...")
        subprocess.run("ollama serve &", shell=True, check=True)
        
        logger.info(f"Waiting for Ollama initialization...")
        time.sleep(5)
        
        logger.info(f"Pulling model: {MODEL}")
        pull_result = subprocess.run(
            f"ollama pull {MODEL}", 
            shell=True, 
            check=True,
            capture_output=True,
            text=True
        )
        logger.debug(f"Model pull output:\n{pull_result.stdout}")
        
        logger.info("Starting Open-WebUI...")
        subprocess.run("open-webui serve &", shell=True, check=True)
        logger.info("Services started successfully")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Service failed: {e.stderr}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        raise
