import type {
  AnalisisResponse,
} from "../types/analisis";


type Recomendaciones =
  AnalisisResponse["analisis"]["recomendaciones"];


interface RecommendationsProps {
  recomendaciones: Recomendaciones;
}


function Recommendations({
  recomendaciones,
}: RecommendationsProps) {

  return (

    <section className="section">


      <div className="section-head">

        <div>

          <h2>
            Recomendaciones
          </h2>

        </div>

        <p>
          Sugerencias generadas según las métricas
          que se encuentran debajo de la referencia
          profesional 2026.
        </p>

      </div>


      {
        recomendaciones.length > 0
          ? (

            <div className="recomendaciones-list">

              {
                recomendaciones.map(
                  (
                    recomendacion,
                    index
                  ) => (

                    <article
                      className="recomendacion-card"
                      key={
                        recomendacion.metrica
                      }
                    >

                      <div className="recomendacion-numero">

                        {index + 1}

                      </div>


                      <div>

                        <h4>

                          {
                            recomendacion
                              .nombre
                          }

                        </h4>

                        <p>

                          {
                            recomendacion
                              .recomendacion
                          }

                        </p>

                      </div>


                    </article>

                  )
                )
              }

            </div>

          )
          : (

            <p className="empty-text">

              No existen recomendaciones
              prioritarias.

            </p>

          )
      }


    </section>

  );
}


export default Recommendations;