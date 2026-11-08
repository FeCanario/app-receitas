import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { cadastrarReceita } from "../api.js";

export default function Cadastrar() {
  const navigate = useNavigate();
  const [nome, setNome] = useState("");
  const [ingredientes, setIngredientes] = useState("");
  const [modoPreparo, setModoPreparo] = useState("");
  const [erro, setErro] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function salvar(e) {
    e.preventDefault();
    setErro("");
    const lista = ingredientes.split("\n").map((i) => i.trim()).filter(Boolean);
    if (lista.length === 0) {
      setErro("Adicione pelo menos um ingrediente");
      return;
    }
    setSalvando(true);
    try {
      await cadastrarReceita({ nome, ingredientes: lista, modo_preparo: modoPreparo });
      navigate("/explorar");
    } catch (err) {
      setErro(err.message);
    } finally {
      setSalvando(false);
    }
  }

  return (
    <section>
      <h2>Cadastrar receita</h2>
      <form className="card formulario" onSubmit={salvar}>
        <label>
          Nome da receita
          <input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Ex.: Bolo de chocolate" required />
        </label>
        <label>
          Ingredientes <span className="dica">(um por linha)</span>
          <textarea
            rows={6}
            value={ingredientes}
            onChange={(e) => setIngredientes(e.target.value)}
            placeholder={"2 ovos\n1 xícara de leite\n..."}
            required
          />
        </label>
        <label>
          Modo de preparo
          <textarea rows={6} value={modoPreparo} onChange={(e) => setModoPreparo(e.target.value)} required />
        </label>

        {erro && <p className="erro">{erro}</p>}

        <button className="btn" disabled={salvando}>{salvando ? "Salvando..." : "Salvar receita"}</button>
      </form>
    </section>
  );
}
