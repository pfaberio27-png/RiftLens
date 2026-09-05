import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearRol,
  traducirTier,
} from "../utils/formatters";


type Analisis =
  AnalisisResponse["analisis"];


interface PlayerHeroProps {
  analisis: Analisis;
}


function PlayerHero({
  analisis,
}: PlayerHeroProps) {

  const rango =
    analisis.jugador.rango;


  return (

    <section className="player-hero">


      <div className="player-hero-left">


        <div className="rank-wrapper">

          <div className="rank-tag">

            <span className="rank-dot" />

            {
              rango?.clasificado
                ? (
                  <>

                    {
                      traducirTier(
                        rango.tier
                      )
                    }

                    {
                      rango.division
                        ? ` ${rango.division}`
                        : ""
                    }

                    {" · "}

                    {rango.cola}

                    {" · Temporada 2026"}

                  </>
                )
                : (
                  <>
                    Sin clasificación · Solo/Duo · Temporada 2026
                  </>
                )
            }

          </div>


          {
            rango?.clasificado && (

              <div className="rank-details">

                <span>
                  {rango.lp} LP
                </span>

                <span>
                  {" · "}
                </span>

                <span className="rank-wins">
                  {rango.victorias} V
                </span>

                <span>
                  {" · "}
                </span>

                <span className="rank-losses">
                  {rango.derrotas} D
                </span>

              </div>

            )
          }

        </div>


        <h2 className="player-title">

          {analisis.jugador.nombre}

          <span>
            #{analisis.jugador.tag}
          </span>

        </h2>


        <p className="player-subtitle">

          Últimas{" "}
          {
            analisis.muestra
              .partidas_obtenidas
          }
          {" "}partidas procesadas.

          {" "}

          Rol principal:{" "}

          <strong>
            {
              formatearRol(
                analisis.muestra
                  .rol_principal
              )
            }
          </strong>

          .

          {
            analisis
              .campeon_insignia
              .nombre && (

              <>

                {" "}Campeón insignia:{" "}

                <strong>
                  {
                    analisis
                      .campeon_insignia
                      .nombre
                  }
                </strong>

                .

              </>

            )
          }

        </p>


        <div className="hero-stats">


          <div className="hero-stat">

            <strong className="win">

              {
                analisis
                  .estadisticas_jugador
                  .resultados
                  .win_rate
              }

              %

            </strong>

            <span>

              Winrate (

              {
                analisis
                  .muestra
                  .partidas_analizadas
              }

              {" PJ)"}

            </span>

          </div>


          <div className="hero-stat">

            <strong>

              {
                analisis
                  .estadisticas_jugador
                  .combate
                  .kda_promedio
              }

            </strong>

            <span>
              KDA promedio
            </span>

          </div>


          <div className="hero-stat">

            <strong>

              {
                Math.round(
                  analisis
                    .estadisticas_jugador
                    .economia
                    .oro_por_minuto_promedio
                )
              }

            </strong>

            <span>
              Oro / min
            </span>

          </div>


        </div>


        <div className="form-strip">

          {
            analisis
              .forma_reciente
              .resultados
              .map(
                (
                  resultado,
                  index
                ) => (

                  <div
                    key={index}
                    className={
                      resultado === "V"
                        ? "form-pip win"
                        : "form-pip loss"
                    }
                  >
                    {resultado}
                  </div>

                )
              )
          }

        </div>


      </div>


      <div className="player-hero-right">


        {
          analisis
            .campeon_insignia
            .imagen_splash && (

            <img
              src={
                analisis
                  .campeon_insignia
                  .imagen_splash
              }
              alt={
                analisis
                  .campeon_insignia
                  .nombre ??
                "Campeón"
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


        <div className="champion-caption">

          <span>
            Campeón insignia
          </span>

          <strong>

            {
              analisis
                .campeon_insignia
                .nombre ??
              "Sin determinar"
            }

          </strong>

        </div>


      </div>


    </section>

  );
}


export default PlayerHero;