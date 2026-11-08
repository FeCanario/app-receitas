"""Tela Explorar: lista de receitas com busca por nome."""
from flask import Blueprint, g, jsonify, request

from auth_utils import login_obrigatorio
from db import get_db, receita_para_dict

bp = Blueprint("explorar", __name__)

_SELECT = """
    SELECT r.*, f.receita_id IS NOT NULL AS favorito
    FROM receitas r
    LEFT JOIN favoritos f ON f.receita_id = r.id AND f.usuario_id = ?
"""


@bp.get("")
@login_obrigatorio
def listar():
    busca = (request.args.get("busca") or "").strip()
    rows = get_db().execute(
        _SELECT + " WHERE r.nome LIKE ? ORDER BY r.nome COLLATE NOCASE",
        (g.usuario_id, f"%{busca}%"),
    ).fetchall()
    return jsonify([receita_para_dict(r, r["favorito"]) for r in rows])


@bp.get("/<int:receita_id>")
@login_obrigatorio
def detalhe(receita_id):
    row = get_db().execute(_SELECT + " WHERE r.id = ?", (g.usuario_id, receita_id)).fetchone()
    if row is None:
        return jsonify({"erro": "Receita não encontrada"}), 404
    return jsonify(receita_para_dict(row, row["favorito"]))
