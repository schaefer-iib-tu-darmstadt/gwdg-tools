"""Build an OpenAI-compatible client for the GWDG Chat-AI API from env vars."""
import os

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_BASE_URL = "https://chat-ai.academiccloud.de/v1"


def create_client() -> OpenAI:
    """Create a GWDG client. Reads GWDG_API_KEY (required) and GWDG_BASE_URL (optional)."""
    load_dotenv()
    api_key = os.environ.get("GWDG_API_KEY") or os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError(
            "GWDG_API_KEY not set. Export it or put it in a .env file (see .env.example)."
        )
    base_url = os.environ.get("GWDG_BASE_URL", DEFAULT_BASE_URL)
    return OpenAI(api_key=api_key, base_url=base_url)
