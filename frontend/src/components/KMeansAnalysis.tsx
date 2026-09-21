import type {
  MineriaDatosKMeans,
  ClusterKMeans,
} from "../types/analisis";


interface KMeansAnalysisProps {
  mineria: MineriaDatosKMeans;
}


function KMeansAnalysis({
  mineria,
}: KMeansAnalysisProps) {

  // ============================================================
  // FORMATEADORES
  // ============================================================

  const formatearNumero = (
    valor: number,
    decimales = 2
  ) => {

    return valor.toLocaleString(
      "es-PE",
      {
        minimumFractionDigits: decimales,
        maximumFractionDigits: decimales,
      }
    );

  };


  // ============================================================
  // DESCRIPCIÓN AUTOMÁTICA DEL CLUSTER
  // ============================================================

  const obtenerDescripcionCluster = (
    cluster: ClusterKMeans
  ) => {

    const metricas =
      cluster.metricas_promedio;


    const clusters =
      mineria.clusters;


    if (clusters.length === 0) {

      return {
        titulo: "Patrón de rendimiento",
        descripcion:
          "Agrupación identificada mediante K-Means.",
      };

    }


    const promedioGeneral = {

      kda:
        clusters.reduce(
          (total, item) =>
            total +
            item.metricas_promedio.kda,
          0
        ) / clusters.length,

      cs:
        clusters.reduce(
          (total, item) =>
            total +
            item.metricas_promedio
              .cs_por_minuto,
          0
        ) / clusters.length,

      oro:
        clusters.reduce(
          (total, item) =>
            total +
            item.metricas_promedio
              .oro_por_minuto,
          0
        ) / clusters.length,

      dano:
        clusters.reduce(
          (total, item) =>
            total +
            item.metricas_promedio
              .daño_por_minuto,
          0
        ) / clusters.length,

      vision:
        clusters.reduce(
          (total, item) =>
            total +
            item.metricas_promedio
              .vision_score,
          0
        ) / clusters.length,

    };


    const diferencias = [

      {
        nombre: "KDA",
        valor:
          promedioGeneral.kda !== 0
            ? metricas.kda /
              promedioGeneral.kda
            : 0,
      },

      {
        nombre: "farmeo",
        valor:
          promedioGeneral.cs !== 0
            ? metricas.cs_por_minuto /
              promedioGeneral.cs
            : 0,
      },

      {
        nombre: "generación de oro",
        valor:
          promedioGeneral.oro !== 0
            ? metricas.oro_por_minuto /
              promedioGeneral.oro
            : 0,
      },

      {
        nombre: "daño",
        valor:
          promedioGeneral.dano !== 0
            ? metricas.daño_por_minuto /
              promedioGeneral.dano
            : 0,
      },

      {
        nombre: "visión",
        valor:
          promedioGeneral.vision !== 0
            ? metricas.vision_score /
              promedioGeneral.vision
            : 0,
      },

    ];


    const mayor =
      [...diferencias].sort(
        (a, b) =>
          b.valor - a.valor
      )[0];


    const menor =
      [...diferencias].sort(
        (a, b) =>
          a.valor - b.valor
      )[0];


    if (
      mayor &&
      mayor.valor >= 1.25
    ) {

      return {
        titulo:
          `Alto impacto en ${mayor.nombre}`,
        descripcion:
          `Este patrón destaca principalmente por ` +
          `${mayor.nombre}, en relación con los demás ` +
          `grupos identificados en las partidas analizadas.`,
      };

    }


    if (
      menor &&
      menor.valor <= 0.75
    ) {

      return {
        titulo:
          `Menor impacto en ${menor.nombre}`,
        descripcion:
          `Este patrón presenta valores relativamente ` +
          `menores en ${menor.nombre} frente a los demás ` +
          `grupos identificados.`,
      };

    }


    return {
      titulo:
        "Rendimiento equilibrado",
      descripcion:
        "Este patrón mantiene métricas relativamente " +
        "equilibradas entre las variables analizadas.",
    };

  };


  // ============================================================
  // SIN DATOS
  // ============================================================

  if (!mineria.disponible) {

    return (

      <section className="section kmeans-section">

        <div className="section-head">

          <div>

            <span className="section-eyebrow">
              MINERÍA DE DATOS
            </span>

            <h2>
              Patrones de rendimiento
            </h2>

          </div>

          <p>
            Análisis de agrupamiento mediante
            el algoritmo K-Means.
          </p>

        </div>


        <div className="kmeans-empty">

          <strong>
            Análisis no disponible
          </strong>

          <p>
            {
              mineria.motivo ??
              "No existen suficientes partidas para aplicar K-Means."
            }
          </p>

        </div>

      </section>

    );

  }


  // ============================================================
  // RENDER
  // ============================================================

  return (

    <section className="section kmeans-section">


      {/* ========================================================
          CABECERA
      ======================================================== */}

      <div className="section-head">

        <div>

          <span className="section-eyebrow">
            MINERÍA DE DATOS
          </span>

          <h2>
            Patrones de rendimiento
          </h2>

        </div>


        <p>
          Agrupaciones encontradas automáticamente
          en tus partidas mediante K-Means,
          considerando las principales métricas
          de rendimiento.
        </p>

      </div>


      {/* ========================================================
          RESUMEN DEL MODELO
      ======================================================== */}

      <div className="kmeans-summary">


        <div className="kmeans-summary-main">

          <span className="kmeans-label">
            ALGORITMO
          </span>

          <strong className="kmeans-algorithm">
            {mineria.algoritmo}
          </strong>

          <p>
            El algoritmo agrupó partidas con
            características estadísticas similares.
          </p>

        </div>


        <div className="kmeans-summary-stat">

          <span>
            Partidas
          </span>

          <strong>
            {mineria.partidas_utilizadas}
          </strong>

          <small>
            utilizadas
          </small>

        </div>


        <div className="kmeans-summary-stat">

          <span>
            Patrones
          </span>

          <strong>
            {mineria.numero_clusters}
          </strong>

          <small>
            detectados
          </small>

        </div>


        <div className="kmeans-summary-stat">

          <span>
            Silhouette
          </span>

          <strong>
            {
              mineria.silhouette_score !==
                undefined &&
              mineria.silhouette_score !== null
                ? formatearNumero(
                    mineria.silhouette_score,
                    4
                  )
                : "—"
            }
          </strong>

          <small>
            criterio de agrupación
          </small>

        </div>


      </div>


      {/* ========================================================
          VARIABLES
      ======================================================== */}

      <div className="kmeans-variables">

        <span className="kmeans-variables-title">
          Variables analizadas
        </span>


        <div className="kmeans-variable-list">

          <span>
            KDA
          </span>

          <span>
            CS / min
          </span>

          <span>
            Oro / min
          </span>

          <span>
            Daño / min
          </span>

          <span>
            Visión
          </span>

        </div>

      </div>


      {/* ========================================================
          CLUSTERS
      ======================================================== */}

      <div className="kmeans-clusters">

        {
          mineria.clusters.map(
            (
              cluster,
              index
            ) => {

              const interpretacion =
                obtenerDescripcionCluster(
                  cluster
                );


              const metricas =
                cluster.metricas_promedio;


              return (

                <article
                  key={cluster.cluster}
                  className="kmeans-cluster-card"
                >


                  <div className="kmeans-cluster-top">

                    <div>

                      <span className="kmeans-pattern-number">

                        PATRÓN{" "}
                        {index + 1}

                      </span>


                      <h3>
                        {
                          interpretacion
                            .titulo
                        }
                      </h3>

                    </div>


                    <div className="kmeans-percentage">

                      <strong>
                        {
                          formatearNumero(
                            cluster.porcentaje,
                            1
                          )
                        }
                        %
                      </strong>

                      <span>
                        {
                          cluster
                            .cantidad_partidas
                        }{" "}
                        partidas
                      </span>

                    </div>

                  </div>


                  <p className="kmeans-cluster-description">

                    {
                      interpretacion
                        .descripcion
                    }

                  </p>


                  <div className="kmeans-metrics">


                    <div className="kmeans-metric">

                      <span>
                        KDA
                      </span>

                      <strong>
                        {
                          formatearNumero(
                            metricas.kda
                          )
                        }
                      </strong>

                    </div>


                    <div className="kmeans-metric">

                      <span>
                        CS / MIN
                      </span>

                      <strong>
                        {
                          formatearNumero(
                            metricas
                              .cs_por_minuto
                          )
                        }
                      </strong>

                    </div>


                    <div className="kmeans-metric">

                      <span>
                        ORO / MIN
                      </span>

                      <strong>
                        {
                          formatearNumero(
                            metricas
                              .oro_por_minuto,
                            0
                          )
                        }
                      </strong>

                    </div>


                    <div className="kmeans-metric">

                      <span>
                        DAÑO / MIN
                      </span>

                      <strong>
                        {
                          formatearNumero(
                            metricas
                              .daño_por_minuto,
                            0
                          )
                        }
                      </strong>

                    </div>


                    <div className="kmeans-metric">

                      <span>
                        VISIÓN
                      </span>

                      <strong>
                        {
                          formatearNumero(
                            metricas
                              .vision_score
                          )
                        }
                      </strong>

                    </div>


                  </div>


                  <div className="kmeans-share">

                    <div
                      className="kmeans-share-fill"
                      style={{
                        width:
                          `${Math.min(
                            cluster.porcentaje,
                            100
                          )}%`,
                      }}
                    />

                  </div>


                </article>

              );

            }
          )
        }

      </div>


      {/* ========================================================
          EVALUACIÓN DE K
      ======================================================== */}

      {
        mineria
          .evaluacion_clusters
          .length > 0 && (

          <div className="kmeans-evaluation">


            <div className="kmeans-evaluation-head">

              <div>

                <span className="kmeans-label">
                  SELECCIÓN DEL MODELO
                </span>

                <h3>
                  Evaluación del número
                  de clusters
                </h3>

              </div>


              <p>
                Se seleccionó K=
                {mineria.numero_clusters} porque
                obtuvo el mayor Silhouette Score
                entre los valores evaluados.
              </p>

            </div>


            <div className="kmeans-evaluation-grid">

              {
                mineria
                  .evaluacion_clusters
                  .map(
                    (evaluacion) => {

                      const seleccionado =
                        evaluacion.k ===
                        mineria.numero_clusters;


                      return (

                        <div
                          key={
                            evaluacion.k
                          }
                          className={
                            seleccionado
                              ? "kmeans-k-card selected"
                              : "kmeans-k-card"
                          }
                        >

                          <span>
                            K
                          </span>

                          <strong>
                            {
                              evaluacion.k
                            }
                          </strong>

                          <small>
                            Silhouette
                          </small>

                          <b>
                            {
                              formatearNumero(
                                evaluacion
                                  .silhouette_score,
                                4
                              )
                            }
                          </b>

                          {
                            seleccionado && (

                              <em>
                                Seleccionado
                              </em>

                            )
                          }

                        </div>

                      );

                    }
                  )
              }

            </div>


          </div>

        )
      }


      {/* ========================================================
          NOTA METODOLÓGICA
      ======================================================== */}

      <div className="kmeans-methodology">

        <span>
          MÉTODO
        </span>

        <p>
          Las métricas fueron normalizadas mediante{" "}
          <strong>
            {
              mineria.normalizacion ??
              "StandardScaler"
            }
          </strong>
          {" "}antes de aplicar K-Means. El número
          de agrupaciones fue seleccionado mediante{" "}
          <strong>
            {
              mineria.criterio_seleccion_k ??
              "Silhouette Score"
            }
          </strong>
          .
        </p>

      </div>


    </section>

  );

}


export default KMeansAnalysis;
