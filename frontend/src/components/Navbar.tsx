import type {
  Dispatch,
  FormEvent,
  SetStateAction,
} from "react";


interface NavbarProps {

  riotId: string;

  setRiotId:
    Dispatch<SetStateAction<string>>;

  cargando: boolean;

  onAnalizar:
    (event?: FormEvent) => void;
}


function Navbar({
  riotId,
  setRiotId,
  cargando,
  onAnalizar,
}: NavbarProps) {

  return (

    <header className="header">

      <div className="logo">

        <span className="logo-icon">
          ◆
        </span>

        <div>

          <h1>
            RiftLens
          </h1>

          <p>
            Análisis competitivo
          </p>

        </div>

      </div>


      <form
        className="header-search"
        onSubmit={onAnalizar}
      >

        <input
          type="text"
          placeholder="Nombre#Tag"
          value={riotId}
          onChange={(event) =>
            setRiotId(
              event.target.value
            )
          }
          disabled={cargando}
        />

        <button
          type="submit"
          disabled={cargando}
        >

          {
            cargando
              ? "Analizando..."
              : "Analizar"
          }

        </button>

      </form>

    </header>

  );
}


export default Navbar;