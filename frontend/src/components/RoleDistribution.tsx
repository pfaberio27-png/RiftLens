import {
  useState,
} from "react";

import type {
  AnalisisResponse,
} from "../types/analisis";

import {
  formatearRol,
} from "../utils/formatters";

import RoleAnalysisModal
  from "./RoleAnalysisModal";


type Muestra =
  AnalisisResponse["analisis"]["muestra"];

type AnalisisPosiciones =
  AnalisisResponse["analisis"]["analisis_posiciones"];

type Rol =
  keyof AnalisisPosiciones;


interface RoleDistributionProps {

  muestra: Muestra;

  analisisPosiciones: AnalisisPosiciones;

}


function RoleDistribution({
  muestra,
  analisisPosiciones,
}: RoleDistributionProps) {


  // ============================================================
  // MODAL
  // ============================================================

  const [
    rolSeleccionado,
    setRolSeleccionado,
  ] = useState<Rol | null>(
    null
  );


  const abrirModal = (
    rol: Rol
  ) => {

    const datos =
      analisisPosiciones[
        rol
      ];


    if (
      !datos ||
      !datos.disponible ||
      datos.partidas === 0
    ) {

      return;

    }


    setRolSeleccionado(
      rol
    );

  };


  const cerrarModal = () => {

    setRolSeleccionado(
      null
    );

  };


  const datosRolSeleccionado =
    rolSeleccionado
      ? analisisPosiciones[
          rolSeleccionado
        ]
      : null;


  return (

    <section className="section">


      {/* ========================================================
          CABECERA
      ======================================================== */}

      <div className="section-head">

        <div>

          <h2>
            Distribución de roles
          </h2>

        </div>


        <p>
          Selecciona una posición para
          consultar el rendimiento obtenido
          en sus partidas.
        </p>

      </div>


      {/* ========================================================
          ROLES
      ======================================================== */}

      <div className="roles-grid">

        {
          Object.entries(
            muestra.distribucion_roles
          ).map(
            ([
              rol,
              datos,
            ]) => {

              const rolTipado =
                rol as Rol;

              const esPrincipal =
                rol ===
                muestra.rol_principal;

              const sinPartidas =
                datos.partidas === 0;


              return (

                <button
                  key={rol}
                  type="button"
                  disabled={
                    sinPartidas
                  }
                  onClick={
                    () =>
                      abrirModal(
                        rolTipado
                      )
                  }
                  className={
                    [
                      "rol-card",
                      esPrincipal
                        ? "activo"
                        : "",
                      sinPartidas
                        ? "sin-partidas"
                        : "",
                    ]
                      .filter(Boolean)
                      .join(" ")
                  }
                >


                  {
                    esPrincipal && (

                      <em className="rol-main-label">
                        ROL PRINCIPAL
                      </em>

                    )
                  }


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

                    {
                      datos.partidas === 1
                        ? " partida"
                        : " partidas"
                    }

                  </span>


                  <small>

                    {
                      datos.porcentaje
                    }

                    %

                  </small>


                  {
                    !sinPartidas && (

                      <span className="rol-open-detail">
                        VER ANÁLISIS →
                      </span>

                    )
                  }


                </button>

              );

            }
          )
        }

      </div>


      {/* ========================================================
          MODAL
      ======================================================== */}

      <RoleAnalysisModal
        abierto={
          rolSeleccionado !== null
        }
        rol={
          rolSeleccionado
        }
        datos={
          datosRolSeleccionado
        }
        onClose={
          cerrarModal
        }
      />


    </section>

  );

}


export default RoleDistribution;