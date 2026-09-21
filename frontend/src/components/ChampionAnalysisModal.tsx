import {
  useEffect,
  useState,
} from "react";

import type {
  AnalisisCampeon,
} from "../types/analisis";


interface ChampionAnalysisModalProps {
  abierto: boolean;
  campeones: AnalisisCampeon[];
  rolPrincipal: string;
  onClose: () => void;
}


const CAMPEONES_POR_PAGINA = 6;


function ChampionAnalysisModal({
  abierto,
  campeones,
  rolPrincipal,
  onClose,
}: ChampionAnalysisModalProps) {

  const [
    paginaActual,
    setPaginaActual,
  ] = useState(1);


  // ============================================================
  // PAGINACIÓN
  // ============================================================

  const totalPaginas =
    Math.max(
      1,
      Math.ceil(
        campeones.length /
        CAMPEONES_POR_PAGINA
      )
    );


  const indiceInicial =
    (
      paginaActual - 1
    ) *
    CAMPEONES_POR_PAGINA;


  const campeonesPagina =
    campeones.slice(
      indiceInicial,
      indiceInicial +
        CAMPEONES_POR_PAGINA
    );


  // ============================================================
  // ABRIR / CERRAR
  // ============================================================

  useEffect(
    () => {

      if (!abierto) {
        return;
      }


      setPaginaActual(1);


      const overflowAnterior =
        document.body.style.overflow;


      document.body.style.overflow =
        "hidden";


      const manejarTeclado = (
        event: KeyboardEvent
      ) => {

        if (
          event.key === "Escape"
        ) {

          onClose();

        }

      };


      window.addEventListener(
        "keydown",
        manejarTeclado
      );


      return () => {

        document.body.style.overflow =
          overflowAnterior;

        window.removeEventListener(
          "keydown",
          manejarTeclado
        );

      };

    },
    [
      abierto,
      onClose,
    ]
  );


  // ============================================================
  // FORMATEADOR
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
  // NO MOSTRAR
  // ============================================================

  if (!abierto) {
    return null;
  }


  return (

    <div
      className="champion-modal-overlay"
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
        className="champion-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="champion-modal-title"
      >


        {/* ====================================================
            HEADER
        ==================================================== */}

        <header className="champion-modal-header">

          <div>

            <span className="champion-modal-eyebrow">
              ANÁLISIS POR CAMPEÓN
            </span>

            <h2 id="champion-modal-title">
              Rendimiento por campeón
            </h2>

            <p>

              Campeones utilizados en las
              partidas correspondientes al
              rol principal{" "}

              <strong>
                {rolPrincipal}
              </strong>

              .

            </p>

          </div>


          <button
            type="button"
            className="champion-modal-close"
            onClick={onClose}
            aria-label="Cerrar"
          >
            ×
          </button>

        </header>


        {/* ====================================================
            INFORMACIÓN DE PÁGINA
        ==================================================== */}

        <div className="champion-modal-toolbar">

          <span>

            {
              campeones.length
            }

            {
              campeones.length === 1
                ? " campeón analizado"
                : " campeones analizados"
            }

          </span>


          <span>

            Mostrando{" "}

            {
              indiceInicial + 1
            }

            {" - "}

            {
              Math.min(
                indiceInicial +
                  CAMPEONES_POR_PAGINA,
                campeones.length
              )
            }

            {" de "}

            {
              campeones.length
            }

          </span>

        </div>


        {/* ====================================================
            CAMPEONES
        ==================================================== */}

        <div className="champion-modal-body">

          <div className="champion-modal-grid">

            {
              campeonesPagina.map(
                (
                  datos,
                  index
                ) => {

                  const posicionGlobal =
                    indiceInicial +
                    index;

                  const muestraPequena =
                    datos.partidas < 3;


                  return (

                    <article
                      key={
                        datos
                          .campeon
                          .nombre
                      }
                      className="champion-modal-card"
                    >


                      {/* CAMPEÓN */}

                      <div className="champion-modal-card-header">

                        <div className="champion-modal-identity">

                          {
                            datos
                              .campeon
                              .imagen_icono && (

                              <img
                                src={
                                  datos
                                    .campeon
                                    .imagen_icono
                                }
                                alt={
                                  datos
                                    .campeon
                                    .nombre
                                }
                              />

                            )
                          }


                          <div>

                            {
                              posicionGlobal ===
                                0 && (

                                <span className="champion-modal-most-used">
                                  MÁS UTILIZADO
                                </span>

                              )
                            }

                            <h3>

                              {
                                datos
                                  .campeon
                                  .nombre
                              }

                            </h3>

                            <span className="champion-modal-use">

                              {
                                formatearNumero(
                                  datos
                                    .porcentaje_uso,
                                  1
                                )
                              }

                              % de uso

                            </span>

                          </div>

                        </div>


                        <div className="champion-modal-games">

                          <strong>
                            {datos.partidas}
                          </strong>

                          <span>

                            {
                              datos.partidas === 1
                                ? "partida"
                                : "partidas"
                            }

                          </span>

                        </div>

                      </div>


                      {/* RESULTADOS */}

                      <div className="champion-modal-results">

                        <div>

                          <span className="champion-modal-win">

                            {
                              datos.victorias
                            }

                            {" V"}

                          </span>

                          <span className="champion-modal-loss">

                            {
                              datos.derrotas
                            }

                            {" D"}

                          </span>

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


                      {/* MÉTRICAS */}

                      <div className="champion-modal-metrics">

                        <div>
                          <span>KDA</span>

                          <strong>
                            {
                              formatearNumero(
                                datos.kda
                              )
                            }
                          </strong>
                        </div>


                        <div>
                          <span>CS / MIN</span>

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .cs_por_minuto
                              )
                            }
                          </strong>
                        </div>


                        <div>
                          <span>ORO / MIN</span>

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .oro_por_minuto,
                                0
                              )
                            }
                          </strong>
                        </div>


                        <div>
                          <span>DAÑO / MIN</span>

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .daño_por_minuto,
                                0
                              )
                            }
                          </strong>
                        </div>


                        <div>
                          <span>VISIÓN</span>

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .vision_score
                              )
                            }
                          </strong>
                        </div>

                      </div>


                      {/* KDA DETALLE */}

                      <div className="champion-modal-combat">

                        <span>

                          Kills promedio

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .kills_promedio
                              )
                            }
                          </strong>

                        </span>


                        <span>

                          Muertes promedio

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .muertes_promedio
                              )
                            }
                          </strong>

                        </span>


                        <span>

                          Asistencias promedio

                          <strong>
                            {
                              formatearNumero(
                                datos
                                  .asistencias_promedio
                              )
                            }
                          </strong>

                        </span>

                      </div>


                      {/* USO */}

                      <div className="champion-modal-usage">

                        <div
                          style={{
                            width:
                              `${Math.min(
                                datos
                                  .porcentaje_uso,
                                100
                              )}%`,
                          }}
                        />

                      </div>


                      {/* MUESTRA PEQUEÑA */}

                      {
                        muestraPequena && (

                          <p className="champion-modal-warning">

                            Muestra reducida:
                            resultados calculados
                            con únicamente{" "}

                            <strong>
                              {
                                datos.partidas
                              }
                            </strong>

                            {
                              datos.partidas === 1
                                ? " partida."
                                : " partidas."
                            }

                          </p>

                        )
                      }

                    </article>

                  );

                }
              )
            }

          </div>

        </div>


        {/* ====================================================
            PAGINACIÓN
        ==================================================== */}

        <footer className="champion-modal-footer">

          {
            totalPaginas > 1 ? (

              <div className="champion-modal-pagination">

                <button
                  type="button"
                  disabled={
                    paginaActual === 1
                  }
                  onClick={
                    () =>
                      setPaginaActual(
                        (
                          pagina
                        ) =>
                          Math.max(
                            1,
                            pagina - 1
                          )
                      )
                  }
                >
                  ← Anterior
                </button>


                <div className="champion-modal-pages">

                  {
                    Array.from(
                      {
                        length:
                          totalPaginas,
                      },
                      (
                        _,
                        index
                      ) =>
                        index + 1
                    ).map(
                      (pagina) => (

                        <button
                          key={pagina}
                          type="button"
                          className={
                            pagina ===
                              paginaActual
                              ? "activo"
                              : ""
                          }
                          onClick={
                            () =>
                              setPaginaActual(
                                pagina
                              )
                          }
                        >
                          {pagina}
                        </button>

                      )
                    )
                  }

                </div>


                <span>

                  Página{" "}

                  <strong>
                    {paginaActual}
                  </strong>

                  {" de "}

                  <strong>
                    {totalPaginas}
                  </strong>

                </span>


                <button
                  type="button"
                  disabled={
                    paginaActual ===
                      totalPaginas
                  }
                  onClick={
                    () =>
                      setPaginaActual(
                        (
                          pagina
                        ) =>
                          Math.min(
                            totalPaginas,
                            pagina + 1
                          )
                      )
                  }
                >
                  Siguiente →
                </button>

              </div>

            ) : (

              <span className="champion-modal-single-page">

                {
                  campeones.length
                }

                {
                  campeones.length === 1
                    ? " campeón"
                    : " campeones"
                }

                {" · Página 1 de 1"}

              </span>

            )
          }

        </footer>


      </div>

    </div>

  );

}


export default ChampionAnalysisModal;