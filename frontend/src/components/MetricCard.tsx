import type {
  ComparacionMetrica,
} from "../types/analisis";

import {
  formatearDiferencia,
  obtenerClaseEstado,
} from "../utils/formatters";


interface MetricCardProps {
  datos: ComparacionMetrica;
}


function MetricCard({
  datos,
}: MetricCardProps) {

  const porcentajeBarra =
    Math.min(
      Math.max(
        datos.porcentaje_referencia,
        0
      ),
      100
    );


  return (

    <article className="metric-card">

      {/* NOMBRE DE LA MÉTRICA */}

      <div className="metric-label">
        {datos.nombre}
      </div>


      {/* JUGADOR VS REFERENCIA */}

      <div className="metric-values">

        <div className="metric-value-block">

          <span className="metric-value-label">
            Tu rendimiento
          </span>

          <strong className="you">
            {datos.jugador}
          </strong>

        </div>


        <div className="metric-value-block metric-reference">

          <span className="metric-value-label">
            Referencia profesional
          </span>

          <strong className="sys">
            {datos.referencia}
          </strong>

        </div>

      </div>


      {/* BARRA DE COMPARACIÓN */}

      <div className="bar-track">

        <div
          className={
            datos.estado === "inferior"
              ? "bar-fill inferior"
              : "bar-fill"
          }
          style={{
            width: `${porcentajeBarra}%`,
          }}
        />

        <div
          className="bar-marker"
          style={{
            left: "60%",
          }}
        />

      </div>


      {/* DIFERENCIA */}

      <div className="comparison-difference">

        <span className="difference-label">
          Diferencia
        </span>

        <strong
          className={
            obtenerClaseEstado(
              datos.estado
            )
          }
        >
          {
            formatearDiferencia(
              datos.diferencia_porcentual
            )
          }
        </strong>

      </div>

    </article>

  );
}


export default MetricCard;