// Todas as chamadas ao backend ficam aqui. Cada tela usa só as funções dela.

function token() {
  return localStorage.getItem("token");
}

async function req(metodo, url, corpo) {
  const resp = await fetch(url, {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      ...(token() ? { Authorization: `Bearer ${token()}` } : {}),
    },
    body: corpo ? JSON.stringify(corpo) : undefined,
  });
  const dados = await resp.json().catch(() => ({}));
  if (resp.status === 401 && token()) {
    sairLocal();
    window.location.href = "/login";
  }
  if (!resp.ok) throw new Error(dados.erro || `Erro ${resp.status}`);
  return dados;
}

// ---------- Sessão ----------
export function estaLogado() {
  return Boolean(token());
}

export function usuarioAtual() {
  return JSON.parse(localStorage.getItem("usuario") || "null");
}

function salvarSessao({ token, usuario }) {
  localStorage.setItem("token", token);
  localStorage.setItem("usuario", JSON.stringify(usuario));
}

function sairLocal() {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
}

// ---------- Login ----------
export async function login(email, senha) {
  salvarSessao(await req("POST", "/api/auth/login", { email, senha }));
}

export async function registrar(nome, email, senha) {
  salvarSessao(await req("POST", "/api/auth/registrar", { nome, email, senha }));
}

export async function logout() {
  try {
    await req("POST", "/api/auth/logout");
  } finally {
    sairLocal();
  }
}

// ---------- Explorar ----------
export const listarReceitas = (busca = "") =>
  req("GET", `/api/receitas?busca=${encodeURIComponent(busca)}`);
export const buscarReceita = (id) => req("GET", `/api/receitas/${id}`);

// ---------- Cadastrar ----------
// receita = { nome, ingredientes: ["..."], modo_preparo }
export const cadastrarReceita = (receita) => req("POST", "/api/receitas", receita);

// ---------- Favoritos ----------
export const listarFavoritos = () => req("GET", "/api/favoritos");
export const favoritar = (id) => req("POST", `/api/favoritos/${id}`);
export const desfavoritar = (id) => req("DELETE", `/api/favoritos/${id}`);

// ---------- Lista de compras ----------
export const listarCompras = () => req("GET", "/api/lista-compras");
export const adicionarItem = (item) => req("POST", "/api/lista-compras", { item });
export const adicionarReceitaNaLista = (receitaId) =>
  req("POST", "/api/lista-compras", { receita_id: receitaId });
export const marcarItem = (id, comprado) =>
  req("PATCH", `/api/lista-compras/${id}`, { comprado });
export const removerItem = (id) => req("DELETE", `/api/lista-compras/${id}`);
export const limparComprados = () => req("DELETE", "/api/lista-compras/comprados");
