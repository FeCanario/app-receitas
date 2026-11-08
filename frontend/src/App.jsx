import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import { estaLogado } from "./api.js";
import Login from "./pages/Login.jsx";
import Explorar from "./pages/Explorar.jsx";
import Cadastrar from "./pages/Cadastrar.jsx";
import Favoritos from "./pages/Favoritos.jsx";
import ListaCompras from "./pages/ListaCompras.jsx";

// Só deixa entrar nas telas internas quem fez login.
function Protegida({ children }) {
  if (!estaLogado()) return <Navigate to="/login" replace />;
  return (
    <>
      <Navbar />
      <main className="container">{children}</main>
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/explorar" element={<Protegida><Explorar /></Protegida>} />
      <Route path="/cadastrar" element={<Protegida><Cadastrar /></Protegida>} />
      <Route path="/favoritos" element={<Protegida><Favoritos /></Protegida>} />
      <Route path="/lista-compras" element={<Protegida><ListaCompras /></Protegida>} />
      <Route path="*" element={<Navigate to="/explorar" replace />} />
    </Routes>
  );
}
