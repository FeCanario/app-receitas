# 🍳 App de Receitas

Projeto em grupo: app de receitas com **React (HTML + JS)** no frontend e **Python (Flask + SQLite)** no backend, versionado com **Gitflow**.

## Telas

| Tela | Descrição | Branch |
|---|---|---|
| Login | Entrar / criar conta | `feature/login` |
| Explorar | Lista de receitas com busca por nome | `feature/explorar` |
| Cadastrar | Formulário: nome, ingredientes e modo de preparo | `feature/cadastrar` |
| Favoritos | Receitas marcadas com estrela | `feature/favoritos` |
| Lista de compras | Checklist de ingredientes | `feature/lista-compras` |

## Como rodar

Precisa de **Python 3.10+** e **Node 18+**. Use dois terminais:

```bash
# Terminal 1 — backend (porta 5000)
cd backend
pip install -r requirements.txt
python app.py
```

```bash
# Terminal 2 — frontend (porta 5173)
cd frontend
npm install
npm run dev
```

Abra http://localhost:5173, crie uma conta e pronto. O banco (`backend/receitas.db`) é criado sozinho com 3 receitas de exemplo.

## Estrutura

```
backend/
  app.py              # cria o Flask e registra as rotas
  db.py               # SQLite: tabelas e receitas de exemplo
  auth_utils.py       # @login_obrigatorio (token no header Authorization)
  routes/             # uma rota (blueprint) por tela
    auth.py  explorar.py  cadastrar.py  favoritos.py  lista_compras.py
frontend/
  src/
    api.js            # todas as chamadas ao backend
    App.jsx           # rotas das telas
    components/       # Navbar, EmConstrucao
    pages/            # uma página por tela
```

Cada tela mexe **só nos próprios arquivos** (`backend/routes/<tela>.py` e `frontend/src/pages/<Tela>.jsx`), então ninguém dá conflito com ninguém.

## Gitflow do grupo

- `main` → versão estável (entrega final)
- `develop` → integração; toda feature sai daqui e volta pra cá
- `feature/<tela>` → uma branch por tela

```bash
git clone <url-do-repo>
cd <repo>
git checkout develop
git pull
git checkout -b feature/<tela>
# ...copie/edite seus arquivos...
git add .
git commit -m "feat(<tela>): implementa tela <Tela>"
git push -u origin feature/<tela>
```

Depois abra um **Pull Request de `feature/<tela>` → `develop`** no GitHub. Quando todas as telas estiverem em `develop`, faz o PR `develop` → `main`.

## API

| Método | Rota | Corpo | Tela |
|---|---|---|---|
| POST | `/api/auth/registrar` | `{nome, email, senha}` | Login |
| POST | `/api/auth/login` | `{email, senha}` | Login |
| POST | `/api/auth/logout` | — | Login |
| GET | `/api/receitas?busca=` | — | Explorar |
| GET | `/api/receitas/<id>` | — | Explorar |
| POST | `/api/receitas` | `{nome, ingredientes: [], modo_preparo}` | Cadastrar |
| GET | `/api/favoritos` | — | Favoritos |
| POST / DELETE | `/api/favoritos/<id>` | — | Favoritos |
| GET | `/api/lista-compras` | — | Lista |
| POST | `/api/lista-compras` | `{item}` ou `{receita_id}` | Lista |
| PATCH | `/api/lista-compras/<id>` | `{comprado}` | Lista |
| DELETE | `/api/lista-compras/<id>` | — | Lista |
| DELETE | `/api/lista-compras/comprados` | — | Lista |

Todas as rotas (menos registrar/login) exigem o header `Authorization: Bearer <token>`, que o `api.js` já manda sozinho.
