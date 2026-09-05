import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearRol,
} from "../utils/formatters";


type Muestra =
  AnalisisResponse["analisis"]["muestra"];


interface RoleDistributionProps {
  muestra: Muestra;
}


function RoleDistribution({
  muestra,
}: RoleDistributionProps) {

  return (

    <section className="section">


      <div className="section-head">

        <div>

          <h2>
            Distribución de roles
          </h2>

        </div>


        <p>
          Distribución de las partidas recientes
          según la posición jugada.
        </p>

      </div>


      <div className="roles-grid">

        {
          Object.entries(
            muestra.distribucion_roles
          ).map(
            ([
              rol,
              datos,
            ]) => (

              <article
                key={rol}
                className={
                  rol ===
                  muestra.rol_principal
                    ? "rol-card activo"
                    : "rol-card"
                }
              >

                <strong>
                  {
                    formatearRol(
                      rol
                    )
                  }
                </strong>


                <span>

                  {
                    datos.partidas
                  }

                  {" partidas"}

                </span>


                <small>

                  {
                    datos.porcentaje
                  }

                  %

                </small>

              </article>

            )
          )
        }

      </div>


    </section>

  );
}


export default RoleDistribution;