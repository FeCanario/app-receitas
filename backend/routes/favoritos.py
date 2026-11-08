"""Stub — será implementado na branch feature/favoritos."""
from flask import Blueprint, jsonify

bp = Blueprint("favoritos", __name__)


@bp.route("", methods=["GET", "POST"])
@bp.route("/<path:_resto>", methods=["GET", "POST", "PATCH", "DELETE"])
def em_construcao(_resto=None):
    return jsonify({"erro": "Funcionalidade em desenvolvimento (feature/favoritos)"}), 501
