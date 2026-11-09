import { useEffect, useState } from "react";
import { adicionarItem, limparComprados, listarCompras, marcarItem, removerItem } from "../api.js";

export default function ListaCompras() {
  const [itens, setItens] = useState([]);
  const [novo, setNovo] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    listarCompras().then(setItens).catch((e) => setErro(e.message));
  }, []);

  // Todas as rotas da lista devolvem a lista atualizada.
  async function executar(acao) {
    try {
      setErro("");
      setItens(await acao());
    } catch (e) {
      setErro(e.message);
    }
  }

  async function adicionar(e) {
    e.preventDefault();
    if (!novo.trim()) return;
    await executar(() => adicionarItem(novo));
    setNovo("");
  }

  const comprados = itens.filter((i) => i.comprado).length;

  return (
    <section>
      <h2>Lista de compras 🛒</h2>

      <form className="linha" onSubmit={adicionar}>
        <input value={novo} onChange={(e) => setNovo(e.target.value)} placeholder="Adicionar item..." />
        <button className="btn">Adicionar</button>
      </form>

      {erro && <p className="erro">{erro}</p>}

      {itens.length === 0 && !erro ? (
        <p className="card vazio">
          Sua lista está vazia. Adicione itens acima ou use o botão 🛒 em uma receita no Explorar.
        </p>
      ) : (
        <div className="card">
          <p className="dica">{comprados} de {itens.length} itens comprados</p>
          <ul className="checklist">
            {itens.map((i) => (
              <li key={i.id} className={i.comprado ? "feito" : ""}>
                <label>
                  <input
                    type="checkbox"
                    checked={i.comprado}
                    onChange={() => executar(() => marcarItem(i.id, !i.comprado))}
                  />
                  {i.item}
                </label>
                <button className="btn-link" title="Remover" onClick={() => executar(() => removerItem(i.id))}>
                  ✕
                </button>
              </li>
            ))}
          </ul>
          {comprados > 0 && (
            <button className="btn btn-secundario" onClick={() => executar(limparComprados)}>
              Limpar itens comprados
            </button>
          )}
        </div>
      )}
    </section>
  );
}
