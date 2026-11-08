"""Tela Cadastrar: adicionar receita (nome, ingredientes, modo de preparo)."""
from flask import Blueprint, g, jsonify, request

from auth_utils import login_obrigatorio
from db import get_db, receita_para_dict

bp = Blueprint("cadastrar", __name__)


@bp.post("")
@login_obrigatorio
def cadastrar():
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    modo_preparo = (dados.get("modo_preparo") or "").strip()

    ingredientes = dados.get("ingredientes") or []
    if isinstance(ingredientes, str):
        ingredientes = ingredientes.split("\n")
    ingredientes = [i.strip() for i in ingredientes if i and i.strip()]

    if not nome or not ingredientes or not modo_preparo:
        return jsonify({"erro": "Preencha nome, ao menos um ingrediente e o modo de preparo"}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO receitas (nome, ingredientes, modo_preparo, usuario_id) VALUES (?, ?, ?, ?)",
        (nome, "\n".join(ingredientes), modo_preparo, g.usuario_id),
    )
    db.commit()
    row = db.execute("SELECT * FROM receitas WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(receita_para_dict(row)), 201
