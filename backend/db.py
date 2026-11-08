"""Conexão com o banco SQLite e criação das tabelas."""
import os
import sqlite3

from flask import g

DB_PATH = os.path.join(os.path.dirname(__file__), "receitas.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tokens (
    token TEXT PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ingredientes TEXT NOT NULL,      -- um ingrediente por linha
    modo_preparo TEXT NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS favoritos (
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    receita_id INTEGER NOT NULL REFERENCES receitas(id),
    PRIMARY KEY (usuario_id, receita_id)
);

CREATE TABLE IF NOT EXISTS lista_compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    item TEXT NOT NULL,
    comprado INTEGER NOT NULL DEFAULT 0
);
"""

RECEITAS_EXEMPLO = [
    ("Bolo de cenoura",
     "3 cenouras\n4 ovos\n1 xícara de óleo\n2 xícaras de açúcar\n2 xícaras de farinha de trigo\n1 colher de fermento",
     "Bata no liquidificador a cenoura, os ovos e o óleo. Misture com o açúcar e a farinha, "
     "adicione o fermento e asse em forno a 180 °C por 40 minutos."),
    ("Panqueca simples",
     "1 xícara de farinha de trigo\n1 xícara de leite\n1 ovo\n1 pitada de sal",
     "Bata tudo no liquidificador, despeje uma concha na frigideira untada e doure dos dois lados."),
    ("Arroz branco",
     "2 xícaras de arroz\n4 xícaras de água quente\n1 dente de alho\n1 colher de óleo\nSal a gosto",
     "Refogue o alho no óleo, junte o arroz e o sal, adicione a água quente e cozinhe em fogo baixo até secar."),
]


def get_db():
    """Retorna a conexão do request atual (cria se não existir)."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas e insere receitas de exemplo na primeira execução."""
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    if conn.execute("SELECT COUNT(*) FROM receitas").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO receitas (nome, ingredientes, modo_preparo) VALUES (?, ?, ?)",
            RECEITAS_EXEMPLO,
        )
    conn.commit()
    conn.close()


def receita_para_dict(row, favorito=False):
    """Converte uma linha da tabela receitas no formato da API."""
    return {
        "id": row["id"],
        "nome": row["nome"],
        "ingredientes": [i for i in row["ingredientes"].split("\n") if i.strip()],
        "modo_preparo": row["modo_preparo"],
        "favorito": bool(favorito),
    }
