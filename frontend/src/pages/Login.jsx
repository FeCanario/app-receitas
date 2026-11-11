import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { estaLogado, login, registrar } from "../api.js";

export default function Login() {
  const navigate = useNavigate();
  const [modo, setModo] = useState("entrar"); // "entrar" ou "criar"
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  if (estaLogado()) return <Navigate to="/explorar" replace />;

  async function enviar(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      if (modo === "entrar") await login(email, senha);
      else await registrar(nome, email, senha);
      navigate("/explorar");
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="login-pagina">
      <form className="card login-card" onSubmit={enviar}>
        <h1>🍳 Receitas</h1>
        <p className="dica">{modo === "entrar" ? "Entre na sua conta" : "Crie sua conta"}</p>

        {modo === "criar" && (
          <label>
            Nome
            <input value={nome} onChange={(e) => setNome(e.target.value)} required />
          </label>
        )}
        <label>
          E-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Senha
          <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required minLength={8} />
        </label>

        {erro && <p className="erro">{erro}</p>}

        <button className="btn" disabled={carregando}>
          {carregando ? "Aguarde..." : modo === "entrar" ? "Entrar" : "Criar conta"}
        </button>

        <button
          type="button"
          className="btn-link"
          onClick={() => { setModo(modo === "entrar" ? "criar" : "entrar"); setErro(""); }}
        >
          {modo === "entrar" ? "Não tem conta? Cadastre-se" : "Já tem conta? Entrar"}
        </button>
      </form>
    </div>
  );
}
