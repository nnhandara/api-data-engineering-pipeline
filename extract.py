
import os
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_data(url):
    """Fetch data from an API and return JSON records."""

    if not url:
        logging.error("API URL is missing.")
        raise ValueError("API URL is missing. Check your .env file.")

    try:
        logging.info(f"Starting extraction: {url}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Expected a list of records from the API.")

        logging.info(f"Extracted {len(data)} records.")
        return data

    except (requests.RequestException, ValueError) as error:
        logging.error(f"Extraction failed: {error}")
        raise


def save_json(data, filename):
    """Save extracted records to a JSON file."""

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logging.info(f"Saved {len(data)} records to {filename}")


def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    sources = {
        "users": os.getenv("USERS_API"),
        "posts": os.getenv("POSTS_API"),
        "comments": os.getenv("COMMENTS_API"),
    }

    for name, url in sources.items():
        records = extract_data(url)
        save_json(records, f"data/{name}.json")
        print(f"{name}: extracted and saved {len(records)} records.")


if __name__ == "__main__":
    main()
