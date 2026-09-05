import type {
  AnalisisResponse,
} from "../types/analisis";

import MetricCard
  from "./MetricCard";

import {
  formatearRol,
} from "../utils/formatters";


type Analisis =
  AnalisisResponse["analisis"];


interface PerformanceComparisonProps {
  analisis: Analisis;
}


function PerformanceComparison({
  analisis,
}: PerformanceComparisonProps) {

  const metricas =
    Object.entries(
      analisis.comparacion
    );


  return (

    <section className="section comparison-section">


      <div className="section-head">

        <div>

          <h2>
            
            Comparación con la referencia profesional
            
          </h2>

        </div>


        <p>
            Tu rendimiento como{" "}
            
            <strong>
                {
                formatearRol(
                    analisis.muestra.rol_principal
                )
                }
            </strong>
            
            {" "}comparado con los valores promedio
            de jugadores profesionales de la temporada
            2026, obtenidos de Oracle&apos;s Elixir.
        </p>

      </div>


      <div className="compare-wrap">


        <div className="compare-champ">


          <div className="compare-champ-image">

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
                />

              )
            }

          </div>


          <div className="compare-champ-body">

            <span className="compare-role">

              {
                formatearRol(
                  analisis
                    .muestra
                    .rol_principal
                )
              }

            </span>


            <h3>

              {
                analisis
                  .campeon_insignia
                  .nombre ??
                "Sin determinar"
              }

            </h3>


            <p>

              {
                analisis
                  .campeon_insignia
                  .partidas
              }

              {" partidas jugadas"}

              {
                analisis
                  .campeon_insignia
                  .estadisticas && (

                  <>

                    {" · "}

                    {
                      analisis
                        .campeon_insignia
                        .estadisticas
                        .resultados
                        .win_rate
                    }

                    {"% de victorias"}

                  </>

                )
              }

            </p>

          </div>


        </div>


        <div className="metric-grid">

          {
            metricas.map(
              ([
                clave,
                datos,
              ]) => (

                <MetricCard
                  key={clave}
                  datos={datos}
                />

              )
            )
          }

        </div>


      </div>


    </section>

  );
}


export default PerformanceComparison;