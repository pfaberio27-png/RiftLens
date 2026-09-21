import {
  useEffect,
} from "react";

import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearRol,
} from "../utils/formatters";


type AnalisisPosiciones =
  AnalisisResponse["analisis"]["analisis_posiciones"];

type Rol =
  keyof AnalisisPosiciones;

type DatosRol =
  AnalisisPosiciones[Rol];


interface RoleAnalysisModalProps {

  abierto: boolean;

  rol: Rol | null;

  datos: DatosRol | null;

  onClose: () => void;

}


function RoleAnalysisModal({
  abierto,
  rol,
  datos,
  onClose,
}: RoleAnalysisModalProps) {


  // ============================================================
  // CERRAR CON ESC + BLOQUEAR SCROLL
  // ============================================================

  useEffect(
    () => {

      if (!abierto) {
        return;
      }


      const manejarEscape = (
        event: KeyboardEvent
      ) => {

        if (event.key === "Escape") {
          onClose();
        }

      };


      const overflowAnterior =
        document.body.style.overflow;


      document.body.style.overflow =
        "hidden";


      window.addEventListener(
        "keydown",
        manejarEscape
      );


      return () => {

        document.body.style.overflow =
          overflowAnterior;

        window.removeEventListener(
          "keydown",
          manejarEscape
        );

      };

    },
    [
      abierto,
      onClose,
    ]
  );


  // ============================================================
  // FORMATEAR NÚMEROS
  // ============================================================

  const formatearNumero = (
    valor: number,
    decimales = 2
  ) => {

    return valor.toLocaleString(
      "es-PE",
      {
        minimumFractionDigits:
          decimales,

        maximumFractionDigits:
          decimales,
      }
    );

  };


  // ============================================================
  // NO RENDERIZAR
  // ============================================================

  if (
    !abierto ||
    !rol ||
    !datos
  ) {

    return null;

  }


  return (

    <div
      className="role-modal-overlay"
      role="presentation"
      onMouseDown={
        (event) => {

          if (
            event.target ===
            event.currentTarget
          ) {

            onClose();

          }

        }
      }
    >

      <div
        className="role-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="role-modal-title"
      >


        {/* ====================================================
            CABECERA
        ==================================================== */}

        <div className="role-modal-header">

          <div>

            <span className="role-modal-eyebrow">
              ANÁLISIS POR POSICIÓN
            </span>

            <h2 id="role-modal-title">

              Rendimiento en{" "}

              {
                formatearRol(
                  rol
                )
              }

            </h2>

            <p>

              Métricas calculadas exclusivamente
              con las partidas disputadas en
              esta posición.

            </p>

          </div>


          <button
            type="button"
            className="role-modal-close"
            onClick={onClose}
            aria-label="Cerrar análisis"
          >

            ×

          </button>

        </div>


        {/* ====================================================
            RESUMEN
        ==================================================== */}

        <div className="role-modal-summary">


          <div>

            <span>
              PARTIDAS
            </span>

            <strong>
              {datos.partidas}
            </strong>

          </div>


          <div>

            <span>
              % DE LA MUESTRA
            </span>

            <strong>

              {
                formatearNumero(
                  datos.porcentaje,
                  1
                )
              }

              %

            </strong>

          </div>


          <div>

            <span>
              VICTORIAS
            </span>

            <strong className="role-modal-win">
              {datos.victorias}
            </strong>

          </div>


          <div>

            <span>
              DERROTAS
            </span>

            <strong className="role-modal-loss">
              {datos.derrotas}
            </strong>

          </div>


          <div>

            <span>
              WIN RATE
            </span>

            <strong>

              {
                formatearNumero(
                  datos.win_rate,
                  1
                )
              }

              %

            </strong>

          </div>


        </div>


        {/* ====================================================
            MÉTRICAS PRINCIPALES
        ==================================================== */}

        <div className="role-modal-block">

          <div className="role-modal-block-title">

            <span>
              MÉTRICAS DE RENDIMIENTO
            </span>

          </div>


          <div className="role-modal-metrics">


            <div>

              <span>
                KDA
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.kda
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                CS / MIN
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.cs_por_minuto
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                ORO / MIN
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.oro_por_minuto,
                    0
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                DAÑO / MIN
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.daño_por_minuto,
                    0
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                VISIÓN
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.vision_score
                  )
                }

              </strong>

            </div>


          </div>

        </div>


        {/* ====================================================
            COMBATE
        ==================================================== */}

        <div className="role-modal-block">

          <div className="role-modal-block-title">

            <span>
              PROMEDIOS DE COMBATE
            </span>

          </div>


          <div className="role-modal-combat">


            <div>

              <span>
                KILLS PROMEDIO
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.kills_promedio
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                MUERTES PROMEDIO
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.muertes_promedio
                  )
                }

              </strong>

            </div>


            <div>

              <span>
                ASISTENCIAS PROMEDIO
              </span>

              <strong>

                {
                  formatearNumero(
                    datos.asistencias_promedio
                  )
                }

              </strong>

            </div>


          </div>

        </div>


        {/* ====================================================
            MUESTRA PEQUEÑA
        ==================================================== */}

        {
          datos.partidas < 3 && (

            <div className="role-modal-warning">

              <strong>
                MUESTRA REDUCIDA
              </strong>

              <p>

                Este análisis se basa en{" "}

                <b>
                  {datos.partidas}
                </b>

                {
                  datos.partidas === 1
                    ? " partida. "
                    : " partidas. "
                }

                Los resultados deben interpretarse
                con cautela debido al tamaño de
                la muestra.

              </p>

            </div>

          )
        }


        {/* ====================================================
            PIE
        ==================================================== */}

        <div className="role-modal-footer">

          <span>

            {
              formatearRol(
                rol
              )
            }

            {" · "}

            {
              datos.partidas
            }

            {
              datos.partidas === 1
                ? " partida analizada"
                : " partidas analizadas"
            }

          </span>

        </div>


      </div>

    </div>

  );

}


export default RoleAnalysisModal;