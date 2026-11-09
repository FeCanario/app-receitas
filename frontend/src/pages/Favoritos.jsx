import { useEffect, useState } from "react";
import { desfavoritar, listarFavoritos } from "../api.js";

export default function Favoritos() {
  const [favoritos, setFavoritos] = useState([]);
  const [aberta, setAberta] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    listarFavoritos().then(setFavoritos).catch((e) => setErro(e.message));
  }, []);

  async function remover(id) {
    try {
      await desfavoritar(id);
      setFavoritos((lista) => lista.filter((r) => r.id !== id));
    } catch (e) {
      setErro(e.message);
    }
  }

  return (
    <section>
      <h2>Favoritos ★</h2>
      {erro && <p className="erro">{erro}</p>}

      {favoritos.length === 0 && !erro && (
        <p className="card vazio">Você ainda não favoritou nenhuma receita. Marque a ☆ na tela Explorar.</p>
      )}

      <ul className="lista-receitas">
        {favoritos.map((r) => (
          <li key={r.id} className="card receita">
            <div className="receita-topo">
              <button className="titulo" onClick={() => setAberta(aberta === r.id ? null : r.id)}>
                {r.nome}
              </button>
              <button className="estrela ativa" title="Remover dos favoritos" onClick={() => remover(r.id)}>
                ★
              </button>
            </div>
            {aberta === r.id && (
              <div className="receita-detalhe">
                <h4>Ingredientes</h4>
                <ul>{r.ingredientes.map((i, idx) => <li key={idx}>{i}</li>)}</ul>
                <h4>Modo de preparo</h4>
                <p>{r.modo_preparo}</p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
