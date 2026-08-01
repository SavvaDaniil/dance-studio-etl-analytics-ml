import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.environ["CRM_BASE_URL"]
CRM_API_KEY: str = os.environ["CRM_API_KEY"]

HEADERS = {
    "Authorization": f"Basic {CRM_API_KEY}"
}