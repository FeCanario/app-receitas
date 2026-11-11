# 🍳 App de Receitas

Projeto em grupo: app de receitas com **React (HTML + JS)** no frontend e **Python (Flask + SQLite)** no backend, versionado com **Gitflow**.

## 👥 Equipe

| Nome | GitHub | Papel |
|---|---|---|
| Fernando Canario | [@FeCanario](https://github.com/FeCanario) | _PO / SM (preencher)_ |
| Gabriel Frigo | [@gfrigo](https://github.com/gfrigo) | Developer |
| _Nome (preencher)_ | [@userbrun1n](https://github.com/userbrun1n) | _Papel (preencher)_ |
| _Nome (preencher)_ | _@usuario_ | _Papel (preencher)_ |

## 🔐 Regras do login

- **L1** Cadastro com e-mail e senha válidos; a senha é gravada com hash.
- **L2** Login correto retorna um token e os dados do usuário.
- **L3** Senha errada retorna erro genérico ("E-mail ou senha incorretos"), sem dizer qual dos dois falhou.
- **L4** E-mail vazio ou sem `@` é rejeitado (400) antes de consultar o banco.
- **L5** Após 3 senhas erradas seguidas a conta é bloqueada por 10 minutos (423), mesmo com a senha certa.
- **L6** Senha com menos de 8 caracteres é rejeitada no cadastro (400).

## 📚 Documentação

A documentação completa está na pasta [`docs/`](docs/README.md):
[como rodar](docs/como-rodar.md) · [arquitetura](docs/arquitetura.md) · [telas](docs/telas.md) · [API](docs/api.md) · [banco de dados](docs/banco-de-dados.md) · [Gitflow e organização](docs/gitflow.md)

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

## Como rodar os testes

Os testes automatizados (T1 a T6, um para cada regra do login) usam `pytest` e um banco temporário, sem mexer no `receitas.db`:

```bash
cd backend
pip install -r requirements.txt
pytest
```

| Teste | O que verifica |
|---|---|
| T1 | Cadastro válido grava a senha com hash (diferente da digitada) |
| T2 | Login correto retorna sucesso e identifica o usuário |
| T3 | Senha errada retorna erro genérico |
| T4 | E-mail vazio ou sem `@` é rejeitado |
| T5 | Quarta tentativa após 3 erros é recusada, mesmo com a senha certa |
| T6 | Senha com menos de 8 caracteres é rejeitada |

## Estrutura

```
backend/
  app.py              # cria o Flask e registra as rotas
  db.py               # SQLite: tabelas e receitas de exemplo
  auth_utils.py       # @login_obrigatorio (token no header Authorization)
  routes/             # uma rota (blueprint) por tela
    auth.py  explorar.py  cadastrar.py  favoritos.py  lista_compras.py
  tests/              # testes automatizados do login (pytest)
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
