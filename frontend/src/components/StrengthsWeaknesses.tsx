import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearDiferencia,
} from "../utils/formatters";


type Fortalezas =
  AnalisisResponse["analisis"]["fortalezas"];

type Debilidades =
  AnalisisResponse["analisis"]["debilidades"];


interface StrengthsWeaknessesProps {

  fortalezas: Fortalezas;

  debilidades: Debilidades;
}


function StrengthsWeaknesses({
  fortalezas,
  debilidades,
}: StrengthsWeaknessesProps) {

  return (

    <section className="evaluacion-grid">


      <article className="evaluacion-card">


        <div className="evaluacion-title">

          <span className="icon-success">
            ↑
          </span>

          <h3>
            Fortalezas
          </h3>

        </div>


        {
          fortalezas.length > 0
            ? (

              <div className="evaluacion-list">

                {
                  fortalezas.map(
                    (item) => (

                      <div
                        className="evaluacion-item"
                        key={
                          item.metrica
                        }
                      >

                        <span>
                          {item.nombre}
                        </span>

                        <strong className="metrica-superior">

                          {
                            formatearDiferencia(
                              item
                                .diferencia_porcentual
                            )
                          }

                        </strong>

                      </div>

                    )
                  )
                }

              </div>

            )
            : (

              <p className="empty-text">

                No se detectaron métricas
                significativamente superiores
                a la referencia profesional.

              </p>

            )
        }


      </article>


      <article className="evaluacion-card">


        <div className="evaluacion-title">

          <span className="icon-danger">
            ↓
          </span>

          <h3>
            Áreas de mejora
          </h3>

        </div>


        {
          debilidades.length > 0
            ? (

              <div className="evaluacion-list">

                {
                  debilidades.map(
                    (item) => (

                      <div
                        className="evaluacion-item"
                        key={
                          item.metrica
                        }
                      >

                        <span>
                          {item.nombre}
                        </span>

                        <strong className="metrica-inferior">

                          {
                            formatearDiferencia(
                              item
                                .diferencia_porcentual
                            )
                          }

                        </strong>

                      </div>

                    )
                  )
                }

              </div>

            )
            : (

              <p className="empty-text">

                No se detectaron métricas
                significativamente inferiores.

              </p>

            )
        }


      </article>


    </section>

  );
}


export default StrengthsWeaknesses;