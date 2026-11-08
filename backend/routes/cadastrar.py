"""Stub — será implementado na branch feature/cadastrar."""
from flask import Blueprint, jsonify

bp = Blueprint("cadastrar", __name__)


@bp.post("")
def em_construcao():
    return jsonify({"erro": "Funcionalidade em desenvolvimento (feature/cadastrar)"}), 501
