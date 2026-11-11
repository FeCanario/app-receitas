import sqlite3

import db as db_module

REGISTRAR = "/api/auth/registrar"
LOGIN = "/api/auth/login"


def test_t1_cadastro_valido_grava_senha_com_hash(client):
    resp = client.post(REGISTRAR, json={"nome": "Ana", "email": "ana@exemplo.com", "senha": "senha1234"})
    assert resp.status_code == 201

    conn = sqlite3.connect(db_module.DB_PATH)
    (senha_gravada,) = conn.execute("SELECT senha_hash FROM usuarios WHERE email = ?", ("ana@exemplo.com",)).fetchone()
    conn.close()
    assert senha_gravada != "senha1234"


def test_t2_login_correto_retorna_sucesso(client, usuario):
    resp = client.post(LOGIN, json={"email": usuario["email"], "senha": usuario["senha"]})
    assert resp.status_code == 200
    corpo = resp.get_json()
    assert corpo["token"]
    assert corpo["usuario"]["email"] == usuario["email"]


def test_t3_senha_errada_retorna_erro_generico(client, usuario):
    errada = client.post(LOGIN, json={"email": usuario["email"], "senha": "outra-senha"})
    inexistente = client.post(LOGIN, json={"email": "naoexiste@exemplo.com", "senha": "outra-senha"})

    assert errada.status_code == 401
    # a mensagem é a mesma para e-mail inexistente e senha errada
    assert errada.get_json() == inexistente.get_json()


def test_t4_email_invalido_e_rejeitado(client):
    for email in ["", "semarroba.com"]:
        assert client.post(REGISTRAR, json={"nome": "Ana", "email": email, "senha": "senha1234"}).status_code == 400
        assert client.post(LOGIN, json={"email": email, "senha": "senha1234"}).status_code == 400


def test_t5_quarta_tentativa_apos_3_erros_e_recusada(client, usuario):
    for _ in range(3):
        assert client.post(LOGIN, json={"email": usuario["email"], "senha": "errada123"}).status_code == 401

    resp = client.post(LOGIN, json={"email": usuario["email"], "senha": usuario["senha"]})
    assert resp.status_code == 423
    assert "token" not in resp.get_json()


def test_t6_senha_curta_e_rejeitada(client):
    resp = client.post(REGISTRAR, json={"nome": "Ana", "email": "ana@exemplo.com", "senha": "1234567"})
    assert resp.status_code == 400
