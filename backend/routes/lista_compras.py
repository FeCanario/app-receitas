"""Stub — será implementado na branch feature/lista-compras."""
from flask import Blueprint, jsonify

bp = Blueprint("lista_compras", __name__)


@bp.route("", methods=["GET", "POST"])
@bp.route("/<path:_resto>", methods=["GET", "POST", "PATCH", "DELETE"])
def em_construcao(_resto=None):
    return jsonify({"erro": "Funcionalidade em desenvolvimento (feature/lista-compras)"}), 501
