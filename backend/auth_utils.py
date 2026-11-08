"""Decorator que protege rotas: exige o header  Authorization: Bearer <token>."""
from functools import wraps

from flask import g, jsonify, request

from db import get_db


def login_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.removeprefix("Bearer ").strip()
        row = None
        if token:
            row = get_db().execute(
                "SELECT usuario_id FROM tokens WHERE token = ?", (token,)
            ).fetchone()
        if row is None:
            return jsonify({"erro": "Faça login para continuar"}), 401
        g.usuario_id = row["usuario_id"]
        return func(*args, **kwargs)

    return wrapper
