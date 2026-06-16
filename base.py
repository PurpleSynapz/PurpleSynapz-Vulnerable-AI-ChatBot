import base64
import json
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template_string, request, session, url_for

from config import (body_page,dashboard_page,host,login_page,port,registration_page,secret_key,
static_dir,users,users_file,)


BASE_DIR = Path(__file__).resolve().parent
LOGIN_PAGE = BASE_DIR / login_page
REGISTRATION_PAGE = BASE_DIR / registration_page
HEADER_PAGE = BASE_DIR / dashboard_page
BODY_PAGE = BASE_DIR / body_page
STATIC_DIR = BASE_DIR / static_dir
USERS_FILE = BASE_DIR / users_file
CHAT_HANDLER = None
UPLOAD_HANDLER = None
DOCUMENTS_HANDLER = None
RUNTIME_USERS = {}

# configure_handlers allows the main application to set the chat, upload, and documents handlers 
def configure_handlers(chat_handler, upload_handler, documents_handler):
    global CHAT_HANDLER, UPLOAD_HANDLER, DOCUMENTS_HANDLER
    CHAT_HANDLER = chat_handler
    UPLOAD_HANDLER = upload_handler
    DOCUMENTS_HANDLER = documents_handler

# checking all the files required for the runtime env
def validate_runtime_files():
    if not LOGIN_PAGE.exists():
        raise FileNotFoundError(f"Login page not found: {LOGIN_PAGE}")
    if not REGISTRATION_PAGE.exists():
        raise FileNotFoundError(f"Registration page not found: {REGISTRATION_PAGE}")
    if not HEADER_PAGE.exists():
        raise FileNotFoundError(f"Header file not found: {HEADER_PAGE}")
    if not BODY_PAGE.exists():
        raise FileNotFoundError(f"Body file not found: {BODY_PAGE}")

def _read_file(file_path: Path):
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path.read_text(encoding="utf-8")

# Load users from the JSON file, merging with the default users defined in config.py.
def _load_runtime_users():
    runtime_users = dict(users)

    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        USERS_FILE.write_text("{}", encoding="utf-8")
        return runtime_users

    try:
        saved_users = json.loads(USERS_FILE.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        saved_users = {}

    if isinstance(saved_users, dict):
        for username, account in saved_users.items():
            if isinstance(account, dict):
                runtime_users[username] = account

    return runtime_users

# Save any new users created during runtime back to the JSON file
def _save_runtime_users():
    persisted_users = {
        username: {
            "password": account.get("password", ""),
            "role": account.get("role", "user"),
        }
        for username, account in RUNTIME_USERS.items()
        if username not in users
    }
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(persisted_users, indent=2), encoding="utf-8")

# Helper functions for authentication and role management
def _is_authenticated():
    return bool(session.get("authenticated"))

# Return a standardized JSON response for authentication errors
def _json_auth_error():
    return jsonify({"error": "Authentication required."}), 401

# Get the current user's role from the session
def _current_role():
    return session.get("role", "")

# Check if the current user has the admin role
def _is_admin():
    return _current_role() == "admin"

# create_app sets up the Flask application with all the necessary routes and handlers for authentication
def create_app():
    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
    app.secret_key = secret_key

    @app.get("/")
    def index():
        if _is_authenticated():
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            if _is_authenticated():
                return redirect(url_for("dashboard"))
            success_message = ""
            if request.args.get("registered") == "1":
                success_message = "Registration successful. Please log in."
            return render_template_string(_read_file(LOGIN_PAGE), error_message="", success_message=success_message)

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template_string(
                _read_file(LOGIN_PAGE),
                error_message="Please enter both username and password.",
                success_message="",
            ), 400

        account = RUNTIME_USERS.get(username)
        if account is None or password != account.get("password"):
            return render_template_string(
                _read_file(LOGIN_PAGE),
                error_message="Invalid username or password.",
                success_message="",
            ), 401

        session.clear()
        session["authenticated"] = True
        session["username"] = username
        session["role"] = account.get("role", "")
        return redirect(url_for("dashboard"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            if _is_authenticated():
                return redirect(url_for("dashboard"))
            return render_template_string(_read_file(REGISTRATION_PAGE), error_message="", success_message="")

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not password or not confirm_password:
            return render_template_string(
                _read_file(REGISTRATION_PAGE),
                error_message="Please fill in all fields.",
                success_message="",
            ), 400

        if len(username) < 3:
            return render_template_string(
                _read_file(REGISTRATION_PAGE),
                error_message="Username must be at least 3 characters.",
                success_message="",
            ), 400

        if password != confirm_password:
            return render_template_string(
                _read_file(REGISTRATION_PAGE),
                error_message="Passwords do not match.",
                success_message="",
            ), 400

        if username in RUNTIME_USERS:
            return render_template_string(
                _read_file(REGISTRATION_PAGE),
                error_message="Username already exists.",
                success_message="",
            ), 409

        RUNTIME_USERS[username] = {
            "password": password,
            "role": "user",
        }
        _save_runtime_users()

        return redirect(url_for("login", registered="1"))

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/dashboard")
    def dashboard():
        if not _is_authenticated():
            return redirect(url_for("login"))

        header_html = _read_file(HEADER_PAGE)
        body_html = _read_file(BODY_PAGE)
        dashboard_html = header_html.replace("</body>", f"{body_html}\n</body>")
        return render_template_string(
            dashboard_html,
            username=session.get("username", ""),
            role=_current_role(),
            can_upload=_is_admin(),
        )

    @app.post("/api/chat")
    def chat():
        if not _is_authenticated():
            return _json_auth_error()

        try:
            payload = request.get_json(silent=False)
            message = payload.get("message", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return jsonify({"error": "Invalid request body."}), 400

        if not message:
            return jsonify({"error": "Message is required."}), 400

        try:
            if CHAT_HANDLER is None:
                raise RuntimeError("Chat handler is not configured.")
            return jsonify(CHAT_HANDLER(message))
        except Exception as error:
            return jsonify({"error": str(error)}), 500

    @app.post("/api/upload")
    def upload():
        if not _is_authenticated():
            return _json_auth_error()
        if not _is_admin():
            return jsonify({"error": "Only admin can upload knowledge files."}), 403

        try:
            payload = request.get_json(silent=False)
            filename = payload.get("filename", "").strip()
            content = payload.get("content", "")
            content_b64 = payload.get("content_b64", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return jsonify({"error": "Invalid request body."}), 400

        if not filename:
            return jsonify({"error": "Filename is required."}), 400
        if not content and not content_b64:
            return jsonify({"error": "File content is required."}), 400

        try:
            if UPLOAD_HANDLER is None:
                raise RuntimeError("Upload handler is not configured.")

            if content_b64:
                file_bytes = base64.b64decode(content_b64)
                result = UPLOAD_HANDLER(filename, content=None, file_bytes=file_bytes)
            else:
                result = UPLOAD_HANDLER(filename, content=content, file_bytes=None)

            return jsonify(result)
        except Exception as error:
            return jsonify({"error": str(error)}), 500

    @app.get("/api/documents")
    def documents():
        if not _is_authenticated():
            return _json_auth_error()
        if not _is_admin():
            return jsonify({"error": "Only admin can view uploaded knowledge files."}), 403

        try:
            if DOCUMENTS_HANDLER is None:
                raise RuntimeError("Documents handler is not configured.")
            return jsonify(DOCUMENTS_HANDLER())
        except Exception as error:
            return jsonify({"error": str(error)}), 500

    return app


def run(chat_handler, upload_handler, documents_handler):
    global RUNTIME_USERS
    print("Starting server...")

    # verify that the handlers are properly configured before starting the server
    configure_handlers(chat_handler, upload_handler, documents_handler)
    validate_runtime_files()
    RUNTIME_USERS = _load_runtime_users()

    # Start the Flask development server
    url = f"http://{host}:{port}/"
    app = create_app()
    
    print(f"Serving login page at {url}")
    print("Press Ctrl+C to stop the server.")
    app.run(host=host, port=port, debug=False)
