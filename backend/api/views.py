import functools
import json
import logging
import time
import traceback

import bcrypt
import jwt
import re

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db import IntegrityError

from .db import query_sql

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
    if request.content_type != "application/json":
        return JsonResponse({"message": "Invalid content type"}, status=415)
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
        f"SELECT * FROM {table} WHERE tier = %s ORDER BY rank ASC LIMIT 25;",
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
        "SELECT id, role, password FROM users WHERE username = %s;",
        [username],
    )
    user = rows[0] if rows else None
    if (
        not user
        or not bcrypt.checkpw(password.encode(), user["password"].encode())
        or len(password.encode()) > 72
    ):
        return JsonResponse({"message": "Invalid login credentials."}, status=401)

    rows = query_sql("SELECT get_user_profile(%s) AS profile;", [username])
    user_profile = rows[0]["profile"]
    now = int(time.time())

    token = jwt.encode(
        {
            "sub": str(user["id"]),
            "username": user_profile["username"],
            "role": user_profile["role"],
            "iat": now,
            "exp": now + 7 * 24 * 60 * 60,
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    return JsonResponse(
        {
            "id": user["id"],
            "username": user_profile["username"],
            "role": user_profile["role"],
            "profileInfo": {**user_profile["profile"], "teams": user_profile["teams"]},
            "token": token,
            "join_date": user_profile["created_at"],
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
    if not username.isalnum() or len(username) < 5:
        raise BadRequest("Invalid username.")
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if (
        not re.search(pattern, password)
        or len(password) < 8
        or len(password.encode("utf-8")) > 72
    ):
        raise BadRequest("Password is invalid.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10)).decode()

    try:
        query_sql(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s);",
            [username, hashed, email],
        )
    except IntegrityError:
        return JsonResponse({"message": "Username already in use."}, status=409)
    return JsonResponse({"message": f"Successfully registered {username}"}, status=201)


# Team management


@csrf_exempt
@require_POST
@json_errors
def save_team(request):
    auth_chk = request.headers.get("Authorization", "")
    if not auth_chk:
        return JsonResponse({"message": "Missing authorization."}, status=401)
    try:
        if auth_chk.startswith("Bearer"):
            payload = jwt.decode(
                auth_chk.removeprefix("Bearer ").strip(),
                settings.JWT_SECRET,
                algorithms=["HS256"],
            )
    except jwt.InvalidTokenError as e:
        return JsonResponse({"message": f"Invalid token {str(e)}"}, status=401)

    body = read_json(request)
    user_id = payload.get("sub")
    team = body.get("team")
    tier = team["gen"] + team["tier"]

    if not isinstance(team, dict) or "gen" not in team or "tier" not in team:
        raise BadRequest("Request must include a team with a gen and tier.")

    try:
        query_sql(
            "INSERT INTO teams (user_id, tier, data) VALUES (%s, %s, %s::jsonb) RETURNING id;",
            [user_id, tier, json.dumps(team)],
        )
    except IntegrityError:
        return JsonResponse({"message": "User not found."}, status=401)

    return JsonResponse(
        {"message": f"Successfully updated {payload['username']}'s teams."}
    )


# Pokedex


@require_GET
@json_errors
def dex(request, name):
    res = query_sql("SELECT * FROM pokedex WHERE pokeapi_slug LIKE %s;", [name])
    if not res:
        return JsonResponse({"message": f"No Pokémon called {name}."}, status=404)
    return JsonResponse({"data": res[0]})


@require_GET
@json_errors
def compare(request, tier):
    rows = query_sql("SELECT * FROM compare_ranks(%s)", [tier])
    print(rows)
    return JsonResponse({"data": rows})
