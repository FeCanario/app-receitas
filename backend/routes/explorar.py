"""Stub — será implementado na branch feature/explorar."""
from flask import Blueprint, jsonify

bp = Blueprint("explorar", __name__)


@bp.get("")
@bp.get("/<int:_id>")
def em_construcao(_id=None):
    return jsonify({"erro": "Funcionalidade em desenvolvimento (feature/explorar)"}), 501
