"""Stub — será implementado na branch feature/login."""
from flask import Blueprint, jsonify

bp = Blueprint("auth", __name__)


@bp.route("", methods=["GET", "POST"])
@bp.route("/<path:_resto>", methods=["GET", "POST", "PATCH", "DELETE"])
def em_construcao(_resto=None):
    return jsonify({"erro": "Funcionalidade em desenvolvimento (feature/login)"}), 501
