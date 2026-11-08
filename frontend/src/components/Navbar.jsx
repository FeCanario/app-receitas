import { NavLink, useNavigate } from "react-router-dom";
import { logout, usuarioAtual } from "../api.js";

export default function Navbar() {
  const navigate = useNavigate();
  const usuario = usuarioAtual();

  async function sair() {
    await logout();
    navigate("/login");
  }

  return (
    <header className="navbar">
      <span className="logo">🍳 Receitas</span>
      <nav>
        <NavLink to="/explorar">Explorar</NavLink>
        <NavLink to="/cadastrar">Cadastrar</NavLink>
        <NavLink to="/favoritos">Favoritos</NavLink>
        <NavLink to="/lista-compras">Lista de compras</NavLink>
      </nav>
      <div className="usuario">
        {usuario && <span>Olá, {usuario.nome.split(" ")[0]}</span>}
        <button className="btn-link" onClick={sair}>Sair</button>
      </div>
    </header>
  );
}
