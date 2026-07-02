import json
import re
from pathlib import Path

from flask import jsonify, redirect, render_template_string, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent
TEST_TASKS_DIR = BASE_DIR / "test_tasks"
TEST_STORAGE_DIR = BASE_DIR / "storage"


def _safe_test_name(raw_name):
    cleaned = "".join(character.lower() if character.isalnum() else "_" for character in raw_name.strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_")


def _test_file_path(test_name):
    safe_name = _safe_test_name(test_name)
    if not safe_name:
        raise ValueError("Test name is required.")
    return TEST_TASKS_DIR / f"{safe_name}.json"


def _answer_storage_path(username, test_slug):
    safe_username = _safe_test_name(username)
    safe_test_slug = _safe_test_name(test_slug)
    if not safe_username:
        raise ValueError("Username is required for answer storage.")
    if not safe_test_slug:
        raise ValueError("Test slug is required for answer storage.")
    return TEST_STORAGE_DIR / safe_username / f"{safe_test_slug}.json"


def _load_user_submission_summary(username, test_data):
    try:
        storage_path = _answer_storage_path(username, test_data["slug"])
    except ValueError:
        return None
    if not storage_path.exists():
        return None

    try:
        stored_data = json.loads(storage_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(stored_data, dict):
        return None

    answers_by_id = {}
    for stored_answer in stored_data.get("answers", []):
        if isinstance(stored_answer, dict):
            answers_by_id[str(stored_answer.get("question_id", "")).strip()] = stored_answer

    score = 0
    total_points = sum(question["points"] for question in test_data["questions"])
    for question in test_data["questions"]:
        stored_answer = answers_by_id.get(question["id"], {})
        user_answer = str(stored_answer.get("user_answer", "")).strip()
        if question["question_type"] == "rag":
            is_correct = validate_rag_response(question["answer"], user_answer)
        else:
            is_correct = validate_direct_response(question["answer"], user_answer)
        if is_correct:
            score += question["points"]

    return {
        "has_submission": True,
        "score": score,
        "total_points": total_points,
    }


def store_user_test_answers(username, test_data, answers):
    storage_path = _answer_storage_path(username, test_data["slug"])
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    stored_answers = []
    for question in test_data["questions"]:
        answer_payload = answers.get(question["id"], {})
        if isinstance(answer_payload, dict):
            user_answer = str(answer_payload.get("answer", "")).strip()
            query_attempts = answer_payload.get("query_attempts", [])
            time_taken_seconds = int(answer_payload.get("time_taken_seconds", 0) or 0)
        else:
            user_answer = str(answer_payload).strip()
            query_attempts = []
            time_taken_seconds = 0
        stored_answers.append(
            {
                "question_id": question["id"],
                "question": question["question"],
                "question_type": question["question_type"],
                "expected_answer": question["answer"],
                "user_answer": user_answer,
                "query_attempts": query_attempts,
                "time_taken_seconds": max(0, time_taken_seconds),
            }
        )

    storage_payload = {
        "username": username,
        "test_name": test_data["test_name"],
        "test_slug": test_data["slug"],
        "answers": stored_answers,
    }
    storage_path.write_text(json.dumps(storage_payload, indent=2), encoding="utf-8")
    return storage_payload


def validate_user_answer(test_data, question, submitted_answer):
    expected_answer = question["answer"]
    user_answer = str(submitted_answer).strip()
    return {
        "test_name": test_data["test_name"],
        "test_slug": test_data["slug"],
        "question_id": question["id"],
        "question": question["question"],
        "expected_answer": expected_answer,
        "user_answer": user_answer,
    }


def validate_rag_response(expected_answer, rag_response):
    normalized_expected = str(expected_answer).strip().casefold()
    normalized_response = str(rag_response).strip().casefold()
    if not normalized_expected or not normalized_response:
        return False
    if normalized_expected in normalized_response:
        return True
    return validate_direct_response(expected_answer, rag_response)


def _tokenize_answer_parts(value):
    normalized_value = str(value).casefold()
    parts = re.split(r"[,\n;/|]+", normalized_value)
    cleaned_parts = []
    for part in parts:
        normalized_part = " ".join(part.split()).strip()
        if normalized_part:
            cleaned_parts.append(normalized_part)
    return cleaned_parts


def validate_direct_response(expected_answer, user_answer):
    normalized_expected = str(expected_answer).strip().casefold()
    normalized_user = str(user_answer).strip().casefold()
    if not normalized_expected or not normalized_user:
        return False
    if normalized_expected == normalized_user:
        return True

    expected_parts = _tokenize_answer_parts(expected_answer)
    user_parts = _tokenize_answer_parts(user_answer)
    if not expected_parts or not user_parts:
        return False

    return any(user_part in expected_parts for user_part in user_parts)


def normalize_question_type(question_type):
    normalized_type = str(question_type or "direct").strip().lower().replace("-", "_").replace(" ", "_")
    if normalized_type in {"direct"}:
        return "direct"
    if normalized_type in {"rag", "bot_query", "botquery"}:
        return "rag"
    raise ValueError("Invalid question type.")


def _find_question_by_id(test_data, question_id):
    for question in test_data["questions"]:
        if question["id"] == question_id:
            return question
    raise FileNotFoundError("Question not found.")


def _load_test_definition(file_path: Path):
    test_data = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(test_data, dict):
        raise ValueError(f"Invalid test format in {file_path.name}.")

    title = str(test_data.get("test_name", file_path.stem)).strip()
    questions = test_data.get("questions", [])
    duration_minutes = test_data.get("duration_minutes", 10)
    if not title:
        raise ValueError(f"Test name missing in {file_path.name}.")
    if not isinstance(questions, list) or not questions:
        raise ValueError(f"Questions missing in {file_path.name}.")
    try:
        duration_minutes = int(duration_minutes)
    except (TypeError, ValueError):
        raise ValueError(f"Duration in {file_path.name} must be a whole number of minutes.")
    if duration_minutes < 1:
        raise ValueError(f"Duration in {file_path.name} must be at least 1 minute.")

    normalized_questions = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question {index} in {file_path.name} is invalid.")

        prompt = str(question.get("question", "")).strip()
        answer = str(question.get("answer", "")).strip()
        points = question.get("points", 1)
        try:
            question_type = normalize_question_type(question.get("question_type", "direct"))
        except ValueError:
            raise ValueError(f"Question {index} in {file_path.name} has an invalid question type.")

        if not prompt or not answer:
            raise ValueError(f"Question {index} in {file_path.name} must include question and answer.")
        try:
            points = int(points)
        except (TypeError, ValueError):
            raise ValueError(f"Question {index} in {file_path.name} must include a whole-number score.")
        if points < 1:
            raise ValueError(f"Question {index} in {file_path.name} must have at least 1 point.")
        normalized_questions.append(
            {
                "id": f"q{index}",
                "question": prompt,
                "answer": answer,
                "points": points,
                "question_type": question_type,
            }
        )

    if not 5 <= len(normalized_questions) <= 10:
        raise ValueError(f"{file_path.name} must contain between 5 and 10 questions.")

    return {
        "test_name": title,
        "file_name": file_path.name,
        "slug": file_path.stem,
        "duration_minutes": duration_minutes,
        "questions": normalized_questions,
    }


def list_tests(username=""):
    tests = []
    TEST_TASKS_DIR.mkdir(parents=True, exist_ok=True)
    for file_path in sorted(TEST_TASKS_DIR.glob("*.json")):
        try:
            test_data = _load_test_definition(file_path)
            submission_summary = _load_user_submission_summary(username, test_data) if username else None
            question_types = {question["question_type"] for question in test_data["questions"]}
            if question_types == {"rag"}:
                test_mode = "rag"
            elif question_types == {"direct"}:
                test_mode = "direct"
            else:
                test_mode = "mixed"
            tests.append(
                {
                    "test_name": test_data["test_name"],
                    "file_name": test_data["file_name"],
                    "slug": test_data["slug"],
                    "duration_minutes": test_data["duration_minutes"],
                    "question_count": len(test_data["questions"]),
                    "total_points": sum(question["points"] for question in test_data["questions"]),
                    "test_mode": test_mode,
                    "has_submission": bool(submission_summary),
                    "submission_score": submission_summary["score"] if submission_summary else None,
                }
            )
        except Exception:
            continue
    return tests


def _load_test_by_slug(test_slug):
    file_path = _test_file_path(test_slug)
    if not file_path.exists():
        raise FileNotFoundError("Test not found.")
    return _load_test_definition(file_path)


def list_user_performances():
    performance_rows = []
    available_tests = {test["slug"]: test for test in list_tests()}

    TEST_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    for user_dir in sorted(path for path in TEST_STORAGE_DIR.iterdir() if path.is_dir()):
        username = user_dir.name
        user_tests = []
        for submission_file in sorted(user_dir.glob("*.json")):
            try:
                stored_data = json.loads(submission_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue

            if not isinstance(stored_data, dict):
                continue

            answers = stored_data.get("answers", [])
            if not isinstance(answers, list):
                answers = []

            test_slug = str(stored_data.get("test_slug", submission_file.stem)).strip() or submission_file.stem
            test_name = str(stored_data.get("test_name", test_slug)).strip() or test_slug
            test_data = available_tests.get(test_slug)

            if test_data:
                canonical_test = _load_test_by_slug(test_slug)
                total_points = test_data["total_points"]
                score = 0
                correct_answers = 0
                for question in canonical_test["questions"]:
                    matched_answer = next(
                        (
                            answer for answer in answers
                            if str(answer.get("question_id", "")).strip() == question["id"]
                        ),
                        {},
                    )
                    user_answer = str(matched_answer.get("user_answer", "")).strip()
                    is_correct = validate_rag_response(question["answer"], user_answer) if question["question_type"] == "rag" else validate_direct_response(question["answer"], user_answer)
                    if is_correct:
                        score += question["points"]
                        correct_answers += 1
                question_count = test_data["question_count"]
            else:
                score = 0
                total_points = 0
                correct_answers = 0
                question_count = len(answers)

            total_time_seconds = sum(
                max(0, int(answer.get("time_taken_seconds", 0) or 0))
                for answer in answers
                if isinstance(answer, dict)
            )

            percentage = (score / total_points * 100) if total_points else 0
            if percentage >= 85:
                performance_status = "Excellent"
            elif percentage >= 70:
                performance_status = "Good"
            elif percentage >= 50:
                performance_status = "Average"
            else:
                performance_status = "Poor"

            user_tests.append(
                {
                    "test_name": test_name,
                    "test_slug": test_slug,
                    "score": score,
                    "total_points": total_points,
                    "question_count": question_count,
                    "correct_answers": correct_answers,
                    "total_time_seconds": total_time_seconds,
                    "performance_status": performance_status,
                }
            )

        if user_tests:
            performance_rows.append(
                {
                    "username": username,
                    "tests": user_tests,
                }
            )

    return performance_rows


def register_test_routes(app, is_authenticated, is_admin, is_user, json_auth_error, chat_handler=None, test_page_path=None):
    @app.get("/test")
    def test_page():
        if not is_authenticated():
            return redirect(url_for("login"))
        if not is_user():
            return redirect(url_for("dashboard"))
        
        if test_page_path and test_page_path.exists():
            test_html = test_page_path.read_text(encoding="utf-8")
            return render_template_string(
                test_html,
                username=session.get("username", ""),
                can_create_test=is_admin(),
                available_tests=list_tests(session.get("username", "")),
            )
        return redirect(url_for("dashboard", view="take-test"))

    @app.get("/create-test")
    def create_test_page():
        if not is_authenticated():
            return redirect(url_for("login"))
        if not is_admin():
            return redirect(url_for("dashboard"))
        
        if test_page_path and test_page_path.exists():
            test_html = test_page_path.read_text(encoding="utf-8")
            return render_template_string(
                test_html,
                username=session.get("username", ""),
                can_create_test=is_admin(),
                available_tests=list_tests(session.get("username", "")),
            )
        return redirect(url_for("dashboard", view="create-test"))

    @app.get("/performance")
    def performance_page():
        if not is_authenticated():
            return redirect(url_for("login"))
        if not is_admin():
            return redirect(url_for("dashboard"))

        if test_page_path and test_page_path.exists():
            test_html = test_page_path.read_text(encoding="utf-8")
            return render_template_string(
                test_html,
                username=session.get("username", ""),
                can_create_test=is_admin(),
                available_tests=list_tests(session.get("username", "")),
                performance_view=True,
                performance_rows=list_user_performances(),
            )
        return redirect(url_for("dashboard"))

    @app.post("/api/tests")
    def create_test():
        if not is_authenticated():
            return json_auth_error()
        if not is_admin():
            return jsonify({"error": "Only admin can create tests."}), 403

        try:
            payload = request.get_json(silent=False)
            test_name = payload.get("test_name", "").strip()
            questions = payload.get("questions", [])
            duration_minutes = payload.get("duration_minutes", 10)
            default_question_type = "rag"
        except (json.JSONDecodeError, AttributeError):
            return jsonify({"error": "Invalid request body."}), 400

        if not test_name:
            return jsonify({"error": "Test name is required."}), 400
        if not isinstance(questions, list):
            return jsonify({"error": "Questions must be a list."}), 400
        try:
            duration_minutes = int(duration_minutes)
        except (TypeError, ValueError):
            return jsonify({"error": "Timer must be a whole number of minutes."}), 400
        if duration_minutes < 1:
            return jsonify({"error": "Timer must be at least 1 minute."}), 400
        if not 5 <= len(questions) <= 10:
            return jsonify({"error": "Each test must contain between 5 and 10 questions."}), 400

        normalized_questions = []
        for index, question in enumerate(questions, start=1):
            if not isinstance(question, dict):
                return jsonify({"error": f"Question {index} is invalid."}), 400

            prompt = str(question.get("question", "")).strip()
            answer = str(question.get("answer", "")).strip()
            points = question.get("points", 1)
            question_type = default_question_type

            if not prompt or not answer:
                return jsonify({"error": f"Question {index} must include a question and answer."}), 400
            try:
                points = int(points)
            except (TypeError, ValueError):
                return jsonify({"error": f"Question {index} must include a whole-number score."}), 400
            if points < 1:
                return jsonify({"error": f"Question {index} must have at least 1 point."}), 400
            normalized_questions.append(
                {
                    "question": prompt,
                    "answer": answer,
                    "points": points,
                    "question_type": question_type,
                }
            )

        file_path = _test_file_path(test_name)
        test_payload = {
            "test_name": test_name,
            "duration_minutes": duration_minutes,
            "questions": normalized_questions,
        }
        TEST_TASKS_DIR.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(test_payload, indent=2), encoding="utf-8")

        return jsonify(
            {
                "message": f"Saved test '{test_name}' to {file_path.name}.",
                "test": {
                    "test_name": test_name,
                    "file_name": file_path.name,
                    "slug": file_path.stem,
                    "duration_minutes": duration_minutes,
                    "question_count": len(normalized_questions),
                    "total_points": sum(question["points"] for question in normalized_questions),
                },
            }
        )

    @app.get("/api/tests")
    def get_tests():
        if not is_authenticated():
            return json_auth_error()
        return jsonify({"tests": list_tests(session.get("username", ""))})

    @app.get("/api/tests/<test_slug>")
    def get_test(test_slug):
        if not is_authenticated():
            return json_auth_error()
        if not (is_user() or is_admin()):
            return jsonify({"error": "Only authorized accounts can view tests."}), 403

        try:
            test_data = _load_test_by_slug(test_slug)
        except FileNotFoundError:
            return jsonify({"error": "Test not found."}), 404
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        return jsonify(
            {
                "test_name": test_data["test_name"],
                "slug": test_data["slug"],
                "duration_minutes": test_data["duration_minutes"],
                "total_points": sum(question["points"] for question in test_data["questions"]),
                "questions": [
                    {
                        "id": question["id"],
                        "question": question["question"],
                        "points": question["points"],
                        "question_type": question["question_type"],
                    }
                    for question in test_data["questions"]
                ],
            }
        )

    @app.post("/api/tests/<test_slug>/questions/<question_id>/query")
    def query_test_question(test_slug, question_id):
        if not is_authenticated():
            return json_auth_error()
        if not (is_user() or is_admin()):
            return jsonify({"error": "Only authorized accounts can query test questions."}), 403

        try:
            payload = request.get_json(silent=False)
            query = str(payload.get("query", "")).strip()
            attempts_used = int(payload.get("attempts_used", 0))
        except (json.JSONDecodeError, AttributeError, TypeError, ValueError):
            return jsonify({"error": "Invalid request body."}), 400

        if not query:
            return jsonify({"error": "Query is required."}), 400

        try:
            test_data = _load_test_by_slug(test_slug)
            question = _find_question_by_id(test_data, question_id)
        except FileNotFoundError as error:
            return jsonify({"error": str(error)}), 404
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        if question["question_type"] != "rag":
            return jsonify({"error": "This question does not use RAG mode."}), 400
        if chat_handler is None:
            return jsonify({"error": "Chat handler is not configured."}), 500
        if attempts_used < 0 or attempts_used >= 3:
            return jsonify({"error": "No attempts remaining for this question."}), 400

        try:
            chat_result = chat_handler(query)
            rag_response = str(chat_result.get("reply", "")).strip()
        except Exception as error:
            return jsonify({"error": str(error)}), 500

        is_correct = validate_rag_response(question["answer"], rag_response)
        attempts_used += 1
        return jsonify(
            {
                "reply": rag_response,
                "is_correct": is_correct,
                "attempts_used": attempts_used,
                "attempts_left": max(0, 3 - attempts_used),
            }
        )

    @app.post("/api/tests/<test_slug>/submit")
    def submit_test(test_slug):
        if not is_authenticated():
            return json_auth_error()
        if not (is_user() or is_admin()):
            return jsonify({"error": "Only authorized accounts can submit tests."}), 403

        try:
            payload = request.get_json(silent=False)
            answers = payload.get("answers", {})
        except (json.JSONDecodeError, AttributeError):
            return jsonify({"error": "Invalid request body."}), 400

        try:
            test_data = _load_test_by_slug(test_slug)
        except FileNotFoundError:
            return jsonify({"error": "Test not found."}), 404
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        username = session.get("username", "")
        try:
            store_user_test_answers(username, test_data, answers)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        score = 0
        total_points = sum(question["points"] for question in test_data["questions"])
        results = []
        for question in test_data["questions"]:
            answer_payload = answers.get(question["id"], {})
            if isinstance(answer_payload, dict):
                submitted_answer = str(answer_payload.get("answer", "")).strip()
                time_taken_seconds = int(answer_payload.get("time_taken_seconds", 0) or 0)
            else:
                submitted_answer = str(answer_payload).strip()
                time_taken_seconds = 0
            validation_data = validate_user_answer(test_data, question, submitted_answer)
            if question["question_type"] == "rag":
                is_correct = validate_rag_response(validation_data["expected_answer"], validation_data["user_answer"])
            else:
                is_correct = validate_direct_response(validation_data["expected_answer"], validation_data["user_answer"])
            if is_correct:
                score += question["points"]
            results.append(
                {
                    "id": question["id"],
                    "question": question["question"],
                    "points": question["points"],
                    "question_type": question["question_type"],
                    "selected": validation_data["user_answer"],
                    "correct_answer": validation_data["expected_answer"],
                    "is_correct": is_correct,
                    "time_taken_seconds": max(0, time_taken_seconds),
                }
            )

        return jsonify(
            {
                "test_name": test_data["test_name"],
                "score": score,
                "total": total_points,
                "results": results,
            }
        )
