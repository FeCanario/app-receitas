"""Tela de Login: cadastro de usuário, login e logout."""
import secrets
import time

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from auth_utils import login_obrigatorio
from db import get_db

bp = Blueprint("auth", __name__)

SENHA_MINIMA = 8
MAX_FALHAS = 3
BLOQUEIO_SEGUNDOS = 10 * 60


def _email_valido(email):
    """Validação simples, feita antes de qualquer consulta ao banco."""
    return bool(email) and "@" in email and not email.startswith("@") and not email.endswith("@")


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

    if not nome:
        return jsonify({"erro": "Informe seu nome"}), 400
    if not _email_valido(email):
        return jsonify({"erro": "Informe um e-mail válido"}), 400
    if len(senha) < SENHA_MINIMA:
        return jsonify({"erro": f"A senha deve ter pelo menos {SENHA_MINIMA} caracteres"}), 400

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

    if not _email_valido(email):
        return jsonify({"erro": "Informe um e-mail válido"}), 400

    db = get_db()
    row = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    if row is None:
        return jsonify({"erro": "E-mail ou senha incorretos"}), 401

    controle = db.execute(
        "SELECT falhas, bloqueado_ate FROM tentativas_login WHERE usuario_id = ?", (row["id"],)
    ).fetchone()
    falhas = controle["falhas"] if controle else 0
    bloqueado_ate = controle["bloqueado_ate"] if controle else 0

    if bloqueado_ate > time.time():
        return jsonify({"erro": "Conta bloqueada temporariamente. Tente novamente em alguns minutos"}), 423

    if not check_password_hash(row["senha_hash"], senha):
        falhas += 1
        bloqueio = time.time() + BLOQUEIO_SEGUNDOS if falhas >= MAX_FALHAS else 0
        db.execute(
            "INSERT OR REPLACE INTO tentativas_login (usuario_id, falhas, bloqueado_ate) VALUES (?, ?, ?)",
            (row["id"], 0 if bloqueio else falhas, bloqueio),
        )
        db.commit()
        return jsonify({"erro": "E-mail ou senha incorretos"}), 401

    db.execute("DELETE FROM tentativas_login WHERE usuario_id = ?", (row["id"],))
    db.commit()
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
