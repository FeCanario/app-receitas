"""Tela de Login: cadastro de usuário, login e logout."""
import secrets

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from auth_utils import login_obrigatorio
from db import get_db

bp = Blueprint("auth", __name__)


def _criar_token(usuario_id):
    token = secrets.token_hex(24)
    db = get_db()
    db.execute("INSERT INTO tokens (token, usuario_id) VALUES (?, ?)", (token, usuario_id))
    db.commit()
    return token


@bp.post("/registrar")
def registrar():
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not nome or not email or len(senha) < 4:
        return jsonify({"erro": "Preencha nome, e-mail e uma senha com pelo menos 4 caracteres"}), 400

    db = get_db()
    if db.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,)).fetchone():
        return jsonify({"erro": "Este e-mail já está cadastrado"}), 409

    cur = db.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
        (nome, email, generate_password_hash(senha)),
    )
    db.commit()
    usuario_id = cur.lastrowid
    return jsonify({
        "token": _criar_token(usuario_id),
        "usuario": {"id": usuario_id, "nome": nome, "email": email},
    }), 201


@bp.post("/login")
def login():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    row = get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    if row is None or not check_password_hash(row["senha_hash"], senha):
        return jsonify({"erro": "E-mail ou senha incorretos"}), 401

    return jsonify({
        "token": _criar_token(row["id"]),
        "usuario": {"id": row["id"], "nome": row["nome"], "email": row["email"]},
    })


@bp.post("/logout")
@login_obrigatorio
def logout():
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    db = get_db()
    db.execute("DELETE FROM tokens WHERE token = ?", (token,))
    db.commit()
    return jsonify({"ok": True})


@bp.get("/eu")
@login_obrigatorio
def eu():
    row = get_db().execute(
        "SELECT id, nome, email FROM usuarios WHERE id = ?", (g.usuario_id,)
    ).fetchone()
    return jsonify(dict(row))
