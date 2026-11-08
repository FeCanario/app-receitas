// Placeholder usado pelas telas que ainda não foram implementadas.
export default function EmConstrucao({ tela, branch }) {
  return (
    <div className="card vazio">
      <h2>{tela}</h2>
      <p>Tela em construção 🚧</p>
      <p className="dica">Será implementada na branch <code>{branch}</code>.</p>
    </div>
  );
}
