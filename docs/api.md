# API

Base: `http://127.0.0.1:5000/api`. No navegador, use só `/api/...`: o proxy do Vite repassa para o Flask.

## Convenções

- Corpo das requisições e respostas em **JSON** (`Content-Type: application/json`).
- **Autenticação:** todas as rotas, menos `registrar` e `login`, exigem o header:
  ```
  Authorization: Bearer <token>
  ```
- **Erros** sempre no formato:
  ```json
  { "erro": "Mensagem explicando o problema" }
  ```

| Status | Quando |
|---|---|
| `200` | OK |
| `201` | Criado |
| `400` | Dados inválidos ou faltando |
| `401` | Sem token, token inválido ou login errado |
| `404` | Recurso não encontrado |
| `409` | Conflito (e-mail já cadastrado) |
| `501` | Rota de uma tela ainda não implementada (stub) |

### Objeto Receita

```json
{
  "id": 1,
  "nome": "Bolo de cenoura",
  "ingredientes": ["3 cenouras", "4 ovos", "1 xícara de óleo"],
  "modo_preparo": "Bata no liquidificador...",
  "favorito": true
}
```
`favorito` indica se o **usuário logado** favoritou a receita.

### Objeto Item da lista

```json
{ "id": 12, "item": "4 ovos", "comprado": false }
```

---

## Autenticação — `routes/auth.py`

### `POST /auth/registrar`
Cria a conta e já devolve um token (o usuário entra direto).

```json
// requisição
{ "nome": "Fernando Canario", "email": "fernando@email.com", "senha": "1234" }
```
```json
// 201
{ "token": "9f1c...e2", "usuario": { "id": 1, "nome": "Fernando Canario", "email": "fernando@email.com" } }
```
Erros: `400` campos vazios ou senha com menos de 4 caracteres · `409` e-mail já cadastrado.

### `POST /auth/login`
```json
// requisição
{ "email": "fernando@email.com", "senha": "1234" }
```
```json
// 200
{ "token": "4ab0...7d", "usuario": { "id": 1, "nome": "Fernando Canario", "email": "fernando@email.com" } }
```
Erro: `401` "E-mail ou senha incorretos".

### `POST /auth/logout` 🔒
Invalida o token enviado. → `200 { "ok": true }`

### `GET /auth/eu` 🔒
Dados do usuário logado. → `200 { "id": 1, "nome": "...", "email": "..." }`

---

## Explorar — `routes/explorar.py`

### `GET /receitas?busca=<texto>` 🔒
Lista as receitas em ordem alfabética. `busca` é opcional, não diferencia maiúsculas e minúsculas e encontra trechos do nome.

```
GET /api/receitas?busca=bol
```
```json
// 200
[ { "id": 1, "nome": "Bolo de cenoura", "ingredientes": [...], "modo_preparo": "...", "favorito": false } ]
```

### `GET /receitas/<id>` 🔒
Uma receita. → `200` Receita · `404` não encontrada.

---

## Cadastrar — `routes/cadastrar.py`

### `POST /receitas` 🔒
```json
// requisição
{
  "nome": "Brigadeiro",
  "ingredientes": ["1 lata de leite condensado", "1 colher de manteiga", "3 colheres de chocolate em pó"],
  "modo_preparo": "Leve ao fogo baixo mexendo até desgrudar da panela..."
}
```
`ingredientes` também aceita uma string com um ingrediente por linha. Itens vazios são ignorados.

→ `201` Receita criada · `400` "Preencha nome, ao menos um ingrediente e o modo de preparo".

---

## Favoritos — `routes/favoritos.py`

### `GET /favoritos` 🔒
Receitas favoritadas pelo usuário (todas com `"favorito": true`), em ordem alfabética.

### `POST /favoritos/<receita_id>` 🔒
Favorita. Repetir não dá erro (idempotente). → `200 { "favorito": true }` · `404` receita não existe.

### `DELETE /favoritos/<receita_id>` 🔒
Remove dos favoritos. → `200 { "favorito": false }`

---

## Lista de compras — `routes/lista_compras.py`

Todas as rotas que alteram a lista **devolvem a lista atualizada** (array de Itens), assim o frontend não precisa fazer outra requisição.

### `GET /lista-compras` 🔒
Itens do usuário: primeiro os não comprados, depois os comprados.

### `POST /lista-compras` 🔒
Aceita **um** destes formatos:
```json
{ "item": "Detergente" }        // item avulso
{ "receita_id": 1 }             // todos os ingredientes da receita
```
→ `201` lista · `400` item vazio · `404` receita não existe.

### `PATCH /lista-compras/<id>` 🔒
```json
{ "comprado": true }
```
→ `200` lista.

### `DELETE /lista-compras/<id>` 🔒
Remove um item. → `200` lista.

### `DELETE /lista-compras/comprados` 🔒
Remove todos os itens marcados como comprados. → `200` lista.

---

## Testando com curl

```bash
# cadastrar e guardar o token
curl -s -X POST http://127.0.0.1:5000/api/auth/registrar \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"t@t.com","senha":"1234"}'

# usar o token
TOKEN=cole_o_token_aqui
curl -s http://127.0.0.1:5000/api/receitas?busca=bolo -H "Authorization: Bearer $TOKEN"
```

## Onde cada função do `api.js` bate

| Função (`frontend/src/api.js`) | Endpoint |
|---|---|
| `registrar(nome, email, senha)` | `POST /auth/registrar` |
| `login(email, senha)` | `POST /auth/login` |
| `logout()` | `POST /auth/logout` |
| `listarReceitas(busca)` | `GET /receitas?busca=` |
| `buscarReceita(id)` | `GET /receitas/<id>` |
| `cadastrarReceita(receita)` | `POST /receitas` |
| `listarFavoritos()` | `GET /favoritos` |
| `favoritar(id)` / `desfavoritar(id)` | `POST` / `DELETE /favoritos/<id>` |
| `listarCompras()` | `GET /lista-compras` |
| `adicionarItem(item)` | `POST /lista-compras` `{item}` |
| `adicionarReceitaNaLista(id)` | `POST /lista-compras` `{receita_id}` |
| `marcarItem(id, comprado)` | `PATCH /lista-compras/<id>` |
| `removerItem(id)` | `DELETE /lista-compras/<id>` |
| `limparComprados()` | `DELETE /lista-compras/comprados` |
