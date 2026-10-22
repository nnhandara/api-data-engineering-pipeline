
import logging
import subprocess
import sys
from pathlib import Path

# Use the directory containing this script as the project directory
PROJECT_DIR = Path(__file__).resolve().parent

# Store pipeline logs in the logs folder
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def run_step(script_name):
    """Run one pipeline script and stop if it fails."""
    script_path = PROJECT_DIR / script_name

    logging.info("Starting step: %s", script_name)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_DIR,
        check=True
    )

    logging.info("Completed step: %s", script_name)


def main():
    logging.info("========== PIPELINE STARTED ==========")

    try:
        run_step("extract.py")
        run_step("clean.py")
        run_step("load.py")

        logging.info("========== PIPELINE COMPLETED SUCCESSFULLY ==========")

    except subprocess.CalledProcessError as error:
        logging.error(
            "Pipeline stopped: %s failed with exit code %s",
            error.cmd[-1],
            error.returncode
        )
        sys.exit(error.returncode)

    except Exception:
        logging.exception("Unexpected pipeline error")
        sys.exit(1)


if __name__ == "__main__":
    main()
