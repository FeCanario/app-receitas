import pytest

import db as db_module
from app import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Cliente de teste com um banco SQLite temporário (não mexe no receitas.db)."""
    monkeypatch.setattr(db_module, "DB_PATH", str(tmp_path / "teste.db"))
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def usuario(client):
    """Usuário já cadastrado."""
    dados = {"nome": "Ana", "email": "ana@exemplo.com", "senha": "senha1234"}
    assert client.post("/api/auth/registrar", json=dados).status_code == 201
    return dados
