# Como rodar

## Pré-requisitos

| Ferramenta | Versão | Para quê |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.10 ou superior | Backend (Flask) |
| [Node.js](https://nodejs.org/) | 18 ou superior | Frontend (React + Vite) |
| [Git](https://git-scm.com/downloads) | qualquer recente | Clonar e versionar |

> Confira com `python --version`, `node --version` e `git --version`.

## 1. Clonar

```bash
git clone https://github.com/FeCanario/app-receitas.git
cd app-receitas
git checkout develop
```

## 2. Backend (terminal 1)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

O servidor sobe em **http://127.0.0.1:5000**. Na primeira execução o arquivo `backend/receitas.db` é criado sozinho, com as tabelas e 3 receitas de exemplo.

> Opcional (recomendado): use um ambiente virtual antes do `pip install`:
> ```bash
> python -m venv .venv
> # Windows: .venv\Scripts\activate    |   Linux/Mac: source .venv/bin/activate
> ```

## 3. Frontend (terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Abra **http://localhost:5173**. O Vite redireciona tudo que começa com `/api` para o Flask (configurado em `frontend/vite.config.js`), então os dois precisam estar rodando ao mesmo tempo.

## 4. Usar

1. Na tela de login, clique em **"Não tem conta? Cadastre-se"**.
2. Crie uma conta (senha com pelo menos 4 caracteres).
3. Navegue pelas telas pelo menu do topo.

## Zerar o banco

Pare o backend, apague `backend/receitas.db` e rode `python app.py` de novo. O banco é recriado com as receitas de exemplo.

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| Telas mostram "Erro 500" ou "Failed to fetch" | Backend não está rodando | Suba o `python app.py` no terminal 1 |
| Tela aparece como "em construção 🚧" | A branch daquela tela ainda não entrou na `develop` | Normal durante o desenvolvimento; aguarde o merge do PR |
| `pip` não encontrado | Python sem pip no PATH | Use `python -m pip install -r requirements.txt` |
| `npm` não encontrado | Node não instalado | Instale o Node.js 18+ |
| Porta 5000 ocupada (comum no macOS por causa do AirPlay) | Outro programa usando a porta | Troque a porta em `app.py` **e** em `vite.config.js` |
| Volto para o login toda hora | O token salvo ficou inválido (ex.: apagou o banco) | Faça login de novo |
