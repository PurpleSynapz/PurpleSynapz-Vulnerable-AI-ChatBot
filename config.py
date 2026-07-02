import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def _get_env(name, default):
    return os.getenv(name, default)


def _get_int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _load_users():
    users_json = os.getenv("APP_USERS_JSON")
    if users_json:
        return json.loads(users_json)

    return {
        "admin": {
            "password": _get_env("APP_ADMIN_PASSWORD", "admin@123"),
            "role": "admin",
        },
    }


users = _load_users()
secret_key = _get_env("APP_SECRET_KEY", "1122334455")
host = _get_env("APP_HOST", "127.0.0.1")
port = _get_int_env("APP_PORT", 7000)

login_page = "frontend/login.html"
registration_page = "frontend/registration.html"
dashboard_page = "frontend/header.html"
body_page = "frontend/body.html"
test_page = "frontend/test.html"
static_dir = "static"
users_file = "users/users.json"

llm_base_url = _get_env("LLM_BASE_URL", "http://127.0.0.1:11434")
rag_base_url = _get_env("RAG_BASE_URL", llm_base_url)
llm_model = _get_env("LLM_MODEL", "llama3.2:3b")
emb_model_name = _get_env("EMBED_MODEL_NAME", "nomic-embed-text")
chroma_persist_directory = str(BASE_DIR / _get_env("CHROMA_PERSIST_DIRECTORY", "chromadb_data"))

chunk_size = _get_int_env("CHUNK_SIZE", 500)
chunk_overlap = _get_int_env("CHUNK_OVERLAP", 100)
