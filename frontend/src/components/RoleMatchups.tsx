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

  const partidasConRival =
    partidas.filter(
      (partida) =>
        partida.rival_rol !== null
    );


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
          partidasConRival.map(
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
                    index
                  }
                  className={
                    partida.victoria
                      ? "matchup-row win"
                      : "matchup-row loss"
                  }
                >


                  {/* ============================================
                      ROL
                  ============================================ */}

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


                  {/* ============================================
                      JUGADOR
                  ============================================ */}

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


                  {/* ============================================
                      VS
                  ============================================ */}

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


                  {/* ============================================
                      RESULTADO
                  ============================================ */}

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
          partidasConRival.length === 0 && (

            <div className="matchup-empty">

              No existen enfrentamientos
              directos disponibles en las
              partidas recientes.

            </div>

          )
        }

      </div>


    </section>

  );
}


export default RoleMatchups;