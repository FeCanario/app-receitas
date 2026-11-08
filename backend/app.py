"""Ponto de entrada do backend. Rode com:  python app.py"""
from flask import Flask

from db import close_db, init_db
from routes.auth import bp as auth_bp
from routes.cadastrar import bp as cadastrar_bp
from routes.explorar import bp as explorar_bp
from routes.favoritos import bp as favoritos_bp
from routes.lista_compras import bp as lista_compras_bp


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(explorar_bp, url_prefix="/api/receitas")
    app.register_blueprint(cadastrar_bp, url_prefix="/api/receitas")
    app.register_blueprint(favoritos_bp, url_prefix="/api/favoritos")
    app.register_blueprint(lista_compras_bp, url_prefix="/api/lista-compras")

    init_db()
    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
