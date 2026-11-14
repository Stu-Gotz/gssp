import functools
import json
import logging
import time
import traceback

import bcrypt
import jwt
import psycopg2

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .db import mongo_users, query_sql

logger = logging.getLogger(__name__)


# Helpers


class BadRequest(Exception):
    pass


def json_errors(view):
    """Log unexpected errors and return a JSON 500.

    The Express routes caught errors and only logged them, which left the
    request hanging with no response. This always answers.
    """

    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except BadRequest as exc:
            return JsonResponse({"message": str(exc)}, status=400)
        except Exception as exc:
            logger.exception("Error handling %s %s", request.method, request.path)
            traceback.print_exc()
            body = {"message": "Internal server error."}
            if settings.DEBUG:
                body["error"] = f"{type(exc).__name__}: {exc}"
            return JsonResponse(body, status=500)

    return wrapper


def read_json(request):
    """Equivalent of express.json() => req.body."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        raise BadRequest("Request body must be valid JSON.")
    if not isinstance(data, dict):
        raise BadRequest("Request body must be a JSON object.")
    return data


# Leaderboards


@require_GET
@json_errors
def leaderboard(request, table, tier):
    # `table` comes from urls.py, never from the request, so it is safe to format in.
    rows = query_sql(
        f"SELECT * FROM {table} WHERE tier = %s ORDER BY rank ASC LIMIT 25",
        [tier],
    )
    return JsonResponse({"data": rows})


# Users


@csrf_exempt
@require_POST
@json_errors
def login(request):
    body = read_json(request)
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        raise BadRequest("Please provide username and password.")

    rows = query_sql(
        "SELECT id, role, password FROM users WHERE username = %s",
        [username],
    )
    user = rows[0] if rows else None
    if (
        not user
        or not bcrypt.checkpw(password.encode(), user["password"].encode())
        or len(password.encode()) > 72
    ):
        return JsonResponse({"message": "Invalid login credentials."}, status=401)

    rows = query_sql("SELECT get_user_profile(%s)", [username])
    user_profile = rows[0]["profile"]
    now = int(time.time())
    token = jwt.encode(
        {
            "sub": str(user["id"]),
            "username": username,
            "role": user["role"],
            "iat": now,
            "exp": now + 7 * 24 * 60 * 60,
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    return JsonResponse(
        {
            "id": user["id"],
            "username": username,
            "role": user["role"],
            "profileInfo": {**user_profile["profile"], "teams": user_profile["teams"]},
            "token": token,
        }
    )


@csrf_exempt
@require_POST
@json_errors
def register(request):
    body = read_json(request)
    username = body.get("username")
    password = body.get("password")
    email = body.get("email")

    if not username or not password:
        raise BadRequest("Please provide username and password.")

    if query_sql("SELECT 1 FROM users WHERE username = %s;", [username]):
        return JsonResponse(
            {"message": "Username already in use, please choose another username."},
            status=409,
        )

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10)).decode()

    # Create the Mongo profile first to get its id

    query_sql("INSERT INTO users (%s, %s, %s);", [username, hashed, email])

    return JsonResponse({"message": f"Successfully registered {username}"}, status=201)


# Team management


@csrf_exempt
@require_POST
@json_errors
def save_team(request):
    body = read_json(request)

    auth_chk = request.headers.get("Authorization", "")
    if not auth_chk:
        return JsonResponse({"error": "Missing authorization."}, status=401)
    try:
        if auth_chk.startswith("Bearer"):
            jwt.decode(body.get("token"), settings.JWT_SECRET, algoriths=["HS256"])

            user_id = body.get("id")
            username = body.get("username")
            team = body.get("team")

            # $push creates the teams array if it doesn't exist yet.
            result = query_sql("INSERT INTO ")
            if result.matched_count == 0:
                return JsonResponse({"message": "User not found."}, status=404)

            return JsonResponse(
                {"message": f"Successfully updated {username}'s teams."}
            )
    except jwt.InvalidTokenError as e:
        return JsonResponse({"message": f"Invalid token {str(e)}"}, status=401)

    print("If you see this it means auth is never checked.")
