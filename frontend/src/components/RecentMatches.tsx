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
          partidas.map(
            (
              partida,
              index
            ) => (

              <article
                key={
                  partida.match_id ??
                  index
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


    </section>

  );
}


export default RecentMatches;