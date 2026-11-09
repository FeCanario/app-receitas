"""Tela Lista de compras: checklist de ingredientes."""
from flask import Blueprint, g, jsonify, request

from auth_utils import login_obrigatorio
from db import get_db

bp = Blueprint("lista_compras", __name__)


def _item_para_dict(row):
    return {"id": row["id"], "item": row["item"], "comprado": bool(row["comprado"])}


def _listar_itens():
    rows = get_db().execute(
        "SELECT * FROM lista_compras WHERE usuario_id = ? ORDER BY comprado, id",
        (g.usuario_id,),
    ).fetchall()
    return [_item_para_dict(r) for r in rows]


@bp.get("")
@login_obrigatorio
def listar():
    return jsonify(_listar_itens())


@bp.post("")
@login_obrigatorio
def adicionar():
    """Aceita {"item": "..."} para um item avulso ou {"receita_id": N} para
    adicionar todos os ingredientes de uma receita."""
    dados = request.get_json(silent=True) or {}
    db = get_db()

    if dados.get("receita_id"):
        row = db.execute(
            "SELECT ingredientes FROM receitas WHERE id = ?", (dados["receita_id"],)
        ).fetchone()
        if row is None:
            return jsonify({"erro": "Receita não encontrada"}), 404
        itens = [i.strip() for i in row["ingredientes"].split("\n") if i.strip()]
    else:
        item = (dados.get("item") or "").strip()
        if not item:
            return jsonify({"erro": "Digite o nome do item"}), 400
        itens = [item]

    db.executemany(
        "INSERT INTO lista_compras (usuario_id, item) VALUES (?, ?)",
        [(g.usuario_id, i) for i in itens],
    )
    db.commit()
    return jsonify(_listar_itens()), 201


@bp.patch("/<int:item_id>")
@login_obrigatorio
def marcar(item_id):
    dados = request.get_json(silent=True) or {}
    db = get_db()
    db.execute(
        "UPDATE lista_compras SET comprado = ? WHERE id = ? AND usuario_id = ?",
        (1 if dados.get("comprado") else 0, item_id, g.usuario_id),
    )
    db.commit()
    return jsonify(_listar_itens())


@bp.delete("/<int:item_id>")
@login_obrigatorio
def remover(item_id):
    db = get_db()
    db.execute(
        "DELETE FROM lista_compras WHERE id = ? AND usuario_id = ?", (item_id, g.usuario_id)
    )
    db.commit()
    return jsonify(_listar_itens())


@bp.delete("/comprados")
@login_obrigatorio
def limpar_comprados():
    db = get_db()
    db.execute("DELETE FROM lista_compras WHERE usuario_id = ? AND comprado = 1", (g.usuario_id,))
    db.commit()
    return jsonify(_listar_itens())
