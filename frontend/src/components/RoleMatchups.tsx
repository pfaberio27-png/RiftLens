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


interface RoleMatchupsProps {
  partidas: PartidasRecientes;
}


function RoleMatchups({
  partidas,
}: RoleMatchupsProps) {

  const PARTIDAS_POR_PAGINA = 10;

  const [
    paginaActual,
    setPaginaActual,
  ] = useState(0);


  const partidasConRival =
    partidas.filter(
      (partida) =>
        partida.rival_rol !== null
    );


  useEffect(() => {
    setPaginaActual(0);
  }, [partidas]);


  const totalPartidas =
    partidasConRival.length;


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
    partidasConRival.slice(
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

    <section className="section matchup-section">


      <div className="section-head">

        <div>

          <span className="section-eyebrow">
            ENFRENTAMIENTOS DIRECTOS
          </span>

          <h2>
            Tu campeón frente al rival de rol
          </h2>

        </div>


        <p>
          Comparación de tus partidas recientes
          contra el jugador enemigo que ocupó
          la misma posición.
        </p>

      </div>


      <div className="matchup-list">

        {
          partidasVisibles.map(
            (
              partida,
              index
            ) => {

              const rival =
                partida.rival_rol;


              if (!rival) {
                return null;
              }


              return (

                <article
                  key={
                    partida.match_id ??
                    `${paginaActual}-${index}`
                  }
                  className={
                    partida.victoria
                      ? "matchup-row win"
                      : "matchup-row loss"
                  }
                >


                  <div className="matchup-role">

                    <span>
                      Rol
                    </span>

                    <strong>
                      {
                        formatearRol(
                          partida.rol
                        )
                      }
                    </strong>

                  </div>


                  <div className="matchup-player">

                    {
                      partida
                        .campeon
                        .imagen_icono && (

                        <img
                          className="matchup-champion-icon"
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


                    <div className="matchup-player-info">

                      <span>
                        Tú
                      </span>

                      <strong>
                        {
                          partida
                            .campeon
                            .nombre
                        }
                      </strong>

                      <small>

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

                      </small>

                    </div>

                  </div>

                  <div className="matchup-vs">

                    <span>
                      <b>
                        VS
                      </b>
                    </span>

                  </div>


                  {/* ============================================
                      RIVAL
                  ============================================ */}

                  <div className="matchup-player matchup-enemy">

                    <div className="matchup-player-info">

                      <span>
                        Rival
                      </span>

                      <strong>
                        {
                          rival
                            .campeon
                            .nombre
                        }
                      </strong>

                      <small>

                        {
                          rival
                            .combate
                            .kills
                        }

                        /

                        {
                          rival
                            .combate
                            .muertes
                        }

                        /

                        {
                          rival
                            .combate
                            .asistencias
                        }

                      </small>

                    </div>


                    {
                      rival
                        .campeon
                        .imagen_icono && (

                        <img
                          className="matchup-champion-icon"
                          src={
                            rival
                              .campeon
                              .imagen_icono
                          }
                          alt={
                            rival
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

                  </div>

                  <div
                    className={
                      partida.victoria
                        ? "matchup-result win"
                        : "matchup-result loss"
                    }
                  >

                    <span>

                      {
                        partida.victoria
                          ? "VICTORIA"
                          : "DERROTA"
                      }

                    </span>

                    <small>

                      {
                        Math.round(
                          partida
                            .duracion_minutos
                        )
                      }

                      {" min"}

                    </small>

                  </div>


                </article>

              );

            }
          )
        }


        {
          totalPartidas === 0 && (

            <div className="matchup-empty">

              No existen enfrentamientos
              directos disponibles en las
              partidas recientes.

            </div>

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


export default RoleMatchups;