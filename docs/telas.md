# Telas

Cada tela tem um arquivo de backend e um de frontend. A coluna **Endpoints** aponta para a [documentação da API](api.md).

| Tela | Responsável | Branch | Backend | Frontend |
|---|---|---|---|---|
| Login | Fernando | `feature/login` | `routes/auth.py` | `pages/Login.jsx` |
| Explorar | Bruno | `feature/explorar` | `routes/explorar.py` | `pages/Explorar.jsx` |
| Cadastrar | Bruno | `feature/cadastrar` | `routes/cadastrar.py` | `pages/Cadastrar.jsx` |
| Favoritos | Gabriel Frigo | `feature/favoritos` | `routes/favoritos.py` | `pages/Favoritos.jsx` |
| Lista de compras | Gabriel Frigo | `feature/lista-compras` | `routes/lista_compras.py` | `pages/ListaCompras.jsx` |

Elementos comuns a todas as telas internas (feitos na base):

- **Navbar** (`components/Navbar.jsx`): links para as 4 telas (o link da tela atual fica destacado), "Olá, <primeiro nome>" e botão **Sair**.
- **Proteção de login** (`App.jsx`): sem login, qualquer tela interna manda para `/login`.

---

## 1. Login

Tela única com dois modos, alternados pelo link no rodapé do formulário.

| Modo | Campos | Ação |
|---|---|---|
| Entrar | E-mail, Senha | `POST /api/auth/login` |
| Criar conta | Nome, E-mail, Senha | `POST /api/auth/registrar` |

**Regras**
- Senha com no mínimo 4 caracteres.
- E-mail é único e guardado em minúsculas, então `Ana@X.com` e `ana@x.com` são a mesma conta.
- Depois de entrar ou criar a conta, vai direto para **Explorar**.
- Quem já está logado e abre `/login` é mandado para **Explorar**.
- Erros aparecem em vermelho embaixo dos campos (ex.: "E-mail ou senha incorretos", "Este e-mail já está cadastrado").
- O botão mostra "Aguarde..." enquanto a requisição está em andamento.

---

## 2. Explorar

Lista de todas as receitas com busca por nome.

**Funcionalidades**
- **Busca:** filtra pelo nome enquanto o usuário digita, com um atraso de 250 ms para não fazer uma requisição a cada letra. Não diferencia maiúsculas e minúsculas e encontra pedaços do nome ("bol" acha "Bolo de cenoura").
- **Ordem:** alfabética.
- **Card da receita:** mostra o nome e a quantidade de ingredientes. Clicar no nome abre ou fecha o detalhe com os ingredientes e o modo de preparo.
- **Estrela ☆/★:** favorita ou desfavorita na hora (atualiza só aquele card, sem recarregar a lista).
- **🛒 Adicionar ingredientes à lista de compras:** manda todos os ingredientes da receita para a lista do usuário e mostra uma mensagem verde por 2,5 s.
- Sem resultados: "Nenhuma receita encontrada."

**Endpoints:** `GET /api/receitas?busca=`, `POST/DELETE /api/favoritos/<id>`, `POST /api/lista-compras` (com `receita_id`).

---

## 3. Cadastrar

Formulário para adicionar uma receita.

| Campo | Tipo | Observação |
|---|---|---|
| Nome da receita | texto | obrigatório |
| Ingredientes | textarea | **um ingrediente por linha**; linhas vazias são ignoradas |
| Modo de preparo | textarea | obrigatório |

**Regras**
- Precisa de pelo menos 1 ingrediente. Essa validação é feita no front e repetida no back.
- Ao salvar com sucesso, volta para **Explorar**, onde a receita nova já aparece.
- A receita fica visível para **todos** os usuários. Quem cadastrou fica registrado no banco (`receitas.usuario_id`).

**Endpoint:** `POST /api/receitas`.

---

## 4. Favoritos

Receitas que o usuário marcou com estrela.

- Cada usuário tem os **seus** favoritos.
- Clicar no nome abre ou fecha os ingredientes e o modo de preparo.
- Clicar na ★ remove dos favoritos, e o card some da lista na hora.
- Sem favoritos, a tela mostra uma dica: "Marque a ☆ na tela Explorar."

**Endpoints:** `GET /api/favoritos`, `DELETE /api/favoritos/<id>`.

---

## 5. Lista de compras

Checklist de ingredientes do usuário.

**Funcionalidades**
- **Adicionar item avulso:** campo no topo + botão "Adicionar" (ou Enter).
- **Itens vindos de receitas:** entram pelo botão 🛒 da tela Explorar.
- **Marcar como comprado:** checkbox. O item fica riscado e vai para o fim da lista.
- **Contador:** "X de Y itens comprados".
- **✕:** remove um item.
- **Limpar itens comprados:** aparece quando há pelo menos 1 item marcado e apaga todos os marcados.
- Lista vazia: mostra uma dica explicando como adicionar.

**Ordem:** primeiro os não comprados, depois os comprados. Dentro de cada grupo, na ordem em que foram adicionados.

**Endpoints:** `GET/POST /api/lista-compras`, `PATCH/DELETE /api/lista-compras/<id>`, `DELETE /api/lista-compras/comprados`.
