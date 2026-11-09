"""Tela Favoritos: receitas marcadas com estrela."""
from flask import Blueprint, g, jsonify

from auth_utils import login_obrigatorio
from db import get_db, receita_para_dict

bp = Blueprint("favoritos", __name__)


@bp.get("")
@login_obrigatorio
def listar():
    rows = get_db().execute(
        """SELECT r.* FROM receitas r
           JOIN favoritos f ON f.receita_id = r.id
           WHERE f.usuario_id = ?
           ORDER BY r.nome COLLATE NOCASE""",
        (g.usuario_id,),
    ).fetchall()
    return jsonify([receita_para_dict(r, favorito=True) for r in rows])


@bp.post("/<int:receita_id>")
@login_obrigatorio
def favoritar(receita_id):
    db = get_db()
    if db.execute("SELECT 1 FROM receitas WHERE id = ?", (receita_id,)).fetchone() is None:
        return jsonify({"erro": "Receita não encontrada"}), 404
    db.execute(
        "INSERT OR IGNORE INTO favoritos (usuario_id, receita_id) VALUES (?, ?)",
        (g.usuario_id, receita_id),
    )
    db.commit()
    return jsonify({"favorito": True})


@bp.delete("/<int:receita_id>")
@login_obrigatorio
def desfavoritar(receita_id):
    db = get_db()
    db.execute(
        "DELETE FROM favoritos WHERE usuario_id = ? AND receita_id = ?",
        (g.usuario_id, receita_id),
    )
    db.commit()
    return jsonify({"favorito": False})
