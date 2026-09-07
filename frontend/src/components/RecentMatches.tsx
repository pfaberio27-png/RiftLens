import {
  useEffect,
  useState,
} from "react";

import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearRol,
} from "../utils/formatters";


type PartidasRecientes =
  AnalisisResponse["analisis"]["partidas_recientes"];


interface RecentMatchesProps {
  partidas: PartidasRecientes;
}


function RecentMatches({
  partidas,
}: RecentMatchesProps) {

  const PARTIDAS_POR_PAGINA = 10;

  const [
    paginaActual,
    setPaginaActual,
  ] = useState(0);


  useEffect(() => {

    setPaginaActual(0);

  }, [partidas]);


  const totalPartidas =
    partidas.length;


  const totalPaginas =
    Math.ceil(
      totalPartidas /
      PARTIDAS_POR_PAGINA
    );


  const inicio =
    paginaActual *
    PARTIDAS_POR_PAGINA;


  const fin =
    Math.min(
      inicio +
        PARTIDAS_POR_PAGINA,
      totalPartidas
    );


  const partidasVisibles =
    partidas.slice(
      inicio,
      fin
    );


  const irAnterior = () => {

    setPaginaActual(
      (pagina) =>
        Math.max(
          pagina - 1,
          0
        )
    );

  };


  const irSiguiente = () => {

    setPaginaActual(
      (pagina) =>
        Math.min(
          pagina + 1,
          totalPaginas - 1
        )
    );

  };


  return (

    <section className="recent-section">


      <div className="section-head">

        <div>

          <h2>
            Actividad reciente en la Grieta
          </h2>

        </div>

        <p>
          Últimas partidas clasificatorias,
          ordenadas de la más reciente
          a la más antigua.
        </p>

      </div>


      <div className="match-strip">

        {
          partidasVisibles.map(
            (
              partida,
              index
            ) => (

              <article
                key={
                  partida.match_id ??
                  `${paginaActual}-${index}`
                }
                className={
                  partida.victoria
                    ? "match-card win"
                    : "match-card loss"
                }
              >

                {
                  partida
                    .campeon
                    .imagen_icono && (

                    <img
                      className="champ-icon"
                      src={
                        partida
                          .campeon
                          .imagen_icono
                      }
                      alt={
                        partida
                          .campeon
                          .nombre
                      }
                      onError={(event) => {

                        event
                          .currentTarget
                          .style
                          .display =
                          "none";

                      }}
                    />

                  )
                }


                <div className="match-kda">

                  {
                    partida
                      .combate
                      .kills
                  }

                  /

                  {
                    partida
                      .combate
                      .muertes
                  }

                  /

                  {
                    partida
                      .combate
                      .asistencias
                  }

                </div>


                <div className="match-meta">

                  {
                    partida
                      .campeon
                      .nombre
                  }

                  {" · "}

                  {
                    formatearRol(
                      partida.rol
                    )
                  }

                  {" · "}

                  {
                    Math.round(
                      partida
                        .duracion_minutos
                    )
                  }

                  {" min"}

                </div>


                <div className="match-result">

                  {
                    partida.victoria
                      ? "Victoria"
                      : "Derrota"
                  }

                </div>

              </article>

            )
          )
        }

      </div>


      {
        totalPartidas > 0 && (

          <div className="matches-pagination">

            {
              totalPaginas > 1 && (

                <div className="matches-pagination-buttons">

                  <button
                    type="button"
                    className="pagination-button"
                    onClick={
                      irAnterior
                    }
                    disabled={
                      paginaActual === 0
                    }
                  >
                    ← Anterior
                  </button>


                  <span className="pagination-page">

                    Página{" "}

                    <strong>
                      {paginaActual + 1}
                    </strong>

                    {" de "}

                    <strong>
                      {totalPaginas}
                    </strong>

                  </span>


                  <button
                    type="button"
                    className="pagination-button"
                    onClick={
                      irSiguiente
                    }
                    disabled={
                      paginaActual >=
                      totalPaginas - 1
                    }
                  >
                    Siguiente →
                  </button>

                </div>

              )
            }

          </div>

        )
      }


    </section>

  );
}


export default RecentMatches;