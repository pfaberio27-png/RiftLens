import {
  useState,
} from "react";

import type {
  AnalisisCampeon,
} from "../types/analisis";

import ChampionAnalysisModal
  from "./ChampionAnalysisModal";


interface ChampionAnalysisProps {
  campeones: AnalisisCampeon[];
  rolPrincipal: string;
}


function ChampionAnalysis({
  campeones,
  rolPrincipal,
}: ChampionAnalysisProps) {

  const [
    modalAbierto,
    setModalAbierto,
  ] = useState(false);


  // ============================================================
  // SIN DATOS
  // ============================================================

  if (
    !campeones ||
    campeones.length === 0
  ) {

    return (

      <section className="section">

        <div className="section-head">

          <div>

            <span className="section-eyebrow">
              ANÁLISIS POR CAMPEÓN
            </span>

            <h2>
              Rendimiento por campeón
            </h2>

          </div>

          <p>
            No existen datos suficientes para
            realizar el análisis por campeón.
          </p>

        </div>

      </section>

    );

  }


  // ============================================================
  // RESUMEN
  // ============================================================

  const totalPartidas =
    campeones.reduce(
      (
        total,
        campeon
      ) =>
        total +
        campeon.partidas,
      0
    );


  const campeonMasUtilizado =
    campeones[0];


  return (

    <section
      className="
        section
        champion-analysis-section
        champion-analysis-compact
      "
    >

      {/* ========================================================
          CABECERA
      ======================================================== */}

      <div className="section-head">

        <div>

          <span className="section-eyebrow">
            ANÁLISIS POR CAMPEÓN
          </span>

          <h2>
            Rendimiento por campeón
          </h2>

        </div>


        <p>

          Métricas de los campeones utilizados
          en las partidas del rol principal{" "}

          <strong>
            {rolPrincipal}
          </strong>

          .

        </p>

      </div>


      {/* ========================================================
          RESUMEN
      ======================================================== */}

      <div className="champion-analysis-summary">

        <div>

          <span>
            CAMPEONES UTILIZADOS
          </span>

          <strong>
            {campeones.length}
          </strong>

        </div>


        <div>

          <span>
            MÁS UTILIZADO
          </span>

          <strong>

            {
              campeonMasUtilizado
                ?.campeon
                .nombre ?? "—"
            }

          </strong>

        </div>


        <div>

          <span>
            PARTIDAS ANALIZADAS
          </span>

          <strong>
            {totalPartidas}
          </strong>

        </div>

      </div>


      {/* ========================================================
          CAMPEÓN PRINCIPAL
      ======================================================== */}

      <div className="champion-compact-highlight">

        <div className="champion-compact-player">

          {
            campeonMasUtilizado
              ?.campeon
              .imagen_icono && (

              <img
                src={
                  campeonMasUtilizado
                    .campeon
                    .imagen_icono
                }
                alt={
                  campeonMasUtilizado
                    .campeon
                    .nombre
                }
              />

            )
          }


          <div>

            <span>
              CAMPEÓN MÁS UTILIZADO
            </span>

            <strong>

              {
                campeonMasUtilizado
                  .campeon
                  .nombre
              }

            </strong>

            <small>

              {
                campeonMasUtilizado
                  .partidas
              }

              {
                campeonMasUtilizado
                  .partidas === 1
                  ? " partida"
                  : " partidas"
              }

              {" · "}

              {
                campeonMasUtilizado
                  .porcentaje_uso
                  .toLocaleString(
                    "es-PE",
                    {
                      maximumFractionDigits: 1,
                    }
                  )
              }

              % de uso

            </small>

          </div>

        </div>


        <div className="champion-compact-metrics">

          <div>

            <span>
              WIN RATE
            </span>

            <strong>

              {
                campeonMasUtilizado
                  .win_rate
                  .toLocaleString(
                    "es-PE",
                    {
                      maximumFractionDigits: 1,
                    }
                  )
              }

              %

            </strong>

          </div>


          <div>

            <span>
              KDA
            </span>

            <strong>

              {
                campeonMasUtilizado
                  .kda
                  .toLocaleString(
                    "es-PE",
                    {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    }
                  )
              }

            </strong>

          </div>


          <div>

            <span>
              V / D
            </span>

            <strong>

              {
                campeonMasUtilizado
                  .victorias
              }

              {" / "}

              {
                campeonMasUtilizado
                  .derrotas
              }

            </strong>

          </div>

        </div>

      </div>


      {/* ========================================================
          BOTÓN
      ======================================================== */}

      <div className="champion-show-all">

        <button
          type="button"
          onClick={
            () =>
              setModalAbierto(
                true
              )
          }
        >

          Ver todos los campeones
          {" ("}
          {campeones.length}
          {")"}

        </button>

      </div>


      {/* ========================================================
          NOTA
      ======================================================== */}

      <div className="champion-analysis-note">

        <span>
          INTERPRETACIÓN
        </span>

        <p>
          Las métricas se calculan de forma
          independiente para cada campeón.
          Los porcentajes de victoria deben
          interpretarse junto con la cantidad
          de partidas disponibles.
        </p>

      </div>


      {/* ========================================================
          MODAL
      ======================================================== */}

      <ChampionAnalysisModal
        abierto={
          modalAbierto
        }
        campeones={
          campeones
        }
        rolPrincipal={
          rolPrincipal
        }
        onClose={
          () =>
            setModalAbierto(
              false
            )
        }
      />

    </section>

  );

}


export default ChampionAnalysis;