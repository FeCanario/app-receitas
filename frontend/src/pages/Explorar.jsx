import { useEffect, useState } from "react";
import { adicionarReceitaNaLista, desfavoritar, favoritar, listarReceitas } from "../api.js";

export default function Explorar() {
  const [busca, setBusca] = useState("");
  const [receitas, setReceitas] = useState([]);
  const [aberta, setAberta] = useState(null); // id da receita expandida
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  // Busca no backend toda vez que o texto muda (com um pequeno atraso).
  useEffect(() => {
    const t = setTimeout(() => {
      listarReceitas(busca).then(setReceitas).catch((e) => setErro(e.message));
    }, 250);
    return () => clearTimeout(t);
  }, [busca]);

  function avisar(texto) {
    setMensagem(texto);
    setTimeout(() => setMensagem(""), 2500);
  }

  async function alternarFavorito(receita) {
    try {
      if (receita.favorito) await desfavoritar(receita.id);
      else await favoritar(receita.id);
      setReceitas((lista) =>
        lista.map((r) => (r.id === receita.id ? { ...r, favorito: !r.favorito } : r))
      );
    } catch (e) {
      setErro(e.message);
    }
  }

  async function mandarParaLista(receita) {
    try {
      await adicionarReceitaNaLista(receita.id);
      avisar(`Ingredientes de "${receita.nome}" adicionados à lista de compras`);
    } catch (e) {
      setErro(e.message);
    }
  }

  return (
    <section>
      <h2>Explorar receitas</h2>
      <input
        className="busca"
        placeholder="🔍 Buscar receita pelo nome..."
        value={busca}
        onChange={(e) => setBusca(e.target.value)}
      />

      {mensagem && <p className="sucesso">{mensagem}</p>}
      {erro && <p className="erro">{erro}</p>}

      {receitas.length === 0 && <p className="card vazio">Nenhuma receita encontrada.</p>}

      <ul className="lista-receitas">
        {receitas.map((r) => (
          <li key={r.id} className="card receita">
            <div className="receita-topo">
              <button className="titulo" onClick={() => setAberta(aberta === r.id ? null : r.id)}>
                {r.nome}
                <span className="dica"> · {r.ingredientes.length} ingredientes</span>
              </button>
              <button
                className={`estrela ${r.favorito ? "ativa" : ""}`}
                title={r.favorito ? "Remover dos favoritos" : "Favoritar"}
                onClick={() => alternarFavorito(r)}
              >
                {r.favorito ? "★" : "☆"}
              </button>
            </div>

            {aberta === r.id && (
              <div className="receita-detalhe">
                <h4>Ingredientes</h4>
                <ul>{r.ingredientes.map((i, idx) => <li key={idx}>{i}</li>)}</ul>
                <h4>Modo de preparo</h4>
                <p>{r.modo_preparo}</p>
                <button className="btn btn-secundario" onClick={() => mandarParaLista(r)}>
                  🛒 Adicionar ingredientes à lista de compras
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
