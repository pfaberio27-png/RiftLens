import {
  type FormEvent,
  useState,
} from "react";

import "./App.css";

import {
  analizarJugador,
} from "./services/analisisService";

import Toast, {
  type ToastTipo,
} from "./components/Toast";

import type {
  AnalisisResponse,
} from "./types/analisis";

import Navbar
  from "./components/Navbar";

import PlayerHero
  from "./components/PlayerHero";

import RecentMatches
  from "./components/RecentMatches";

import PerformanceComparison
  from "./components/PerformanceComparison";

import RoleMatchups
  from "./components/RoleMatchups";

import RoleDistribution
  from "./components/RoleDistribution";

import StrengthsWeaknesses
  from "./components/StrengthsWeaknesses";

import Recommendations
  from "./components/Recommendations";


function App() {

  const [riotId, setRiotId] =
    useState("");

  const [region, setRegion] =
    useState("LAS");

  const [resultado, setResultado] =
    useState<AnalisisResponse | null>(
      null
    );

  const [cargando, setCargando] =
    useState(false);


  // ============================================================
  // TOAST
  // ============================================================

  const [
    toastMensaje,
    setToastMensaje,
  ] =
    useState("");

  const [
    toastTipo,
    setToastTipo,
  ] =
    useState<ToastTipo>(
      "success"
    );


  const mostrarToast = (
    mensaje: string,
    tipo: ToastTipo
  ) => {

    setToastMensaje(
      mensaje
    );

    setToastTipo(
      tipo
    );

  };


  // ============================================================
  // ANALIZAR JUGADOR
  // ============================================================

  const analizarRendimiento = async (
    event?: FormEvent
  ) => {

    event?.preventDefault();


    const riotIdLimpio =
      riotId.trim();


    setResultado(
      null
    );

    setToastMensaje(
      ""
    );


    // ==========================================================
    // VALIDAR RIOT ID VACÍO
    // ==========================================================

    if (!riotIdLimpio) {

      mostrarToast(
        "Ingresa un Riot ID.",
        "error"
      );

      return;
    }


    // ==========================================================
    // VALIDAR FORMATO #
    // ==========================================================

    if (
      !riotIdLimpio.includes("#")
    ) {

      mostrarToast(
        "El Riot ID debe tener el formato Nombre#TAG.",
        "error"
      );

      return;
    }


    const [
      nombre,
      tag,
    ] =
      riotIdLimpio.split(
        "#",
        2
      );


    // ==========================================================
    // VALIDAR NOMBRE Y TAG
    // ==========================================================

    if (
      !nombre?.trim() ||
      !tag?.trim()
    ) {

      mostrarToast(
        "El Riot ID debe tener el formato Nombre#TAG.",
        "error"
      );

      return;
    }


    // ==========================================================
    // CONSULTAR BACKEND
    // ==========================================================

    try {

      setCargando(
        true
      );


      const data =
        await analizarJugador(
          riotIdLimpio,
          region
        );


      setResultado(
        data
      );


      mostrarToast(
        `${data.riot_id} fue analizado correctamente en ${region}.`,
        "success"
      );

    } catch (error) {

      const mensaje =
        error instanceof Error
          ? error.message
          : "Ocurrió un error inesperado.";


      mostrarToast(
        mensaje,
        "error"
      );

    } finally {

      setCargando(
        false
      );

    }

  };


  // ============================================================
  // DATOS
  // ============================================================

  const analisis =
    resultado?.analisis;


  // ============================================================
  // VISTA
  // ============================================================

  return (

    <div className="app">


      {/* ========================================================
          NAVBAR
      ======================================================== */}

      <Navbar
        riotId={riotId}
        setRiotId={setRiotId}
        region={region}
        setRegion={setRegion}
        cargando={cargando}
        onAnalizar={
          analizarRendimiento
        }
      />


      {/* ========================================================
          TOAST FLOTANTE
      ======================================================== */}

      {
        toastMensaje && (

          <Toast
            mensaje={
              toastMensaje
            }
            tipo={
              toastTipo
            }
            onCerrar={() =>
              setToastMensaje("")
            }
          />

        )
      }


      <main className="container">


        {/* ======================================================
            HERO INICIAL
        ====================================================== */}

        {
          !resultado &&
          !cargando && (

            <section className="hero">


              <span className="hero-eyebrow">

                ANÁLISIS COMPETITIVO

              </span>


              <h2>

                Analiza tu rendimiento
                en League of Legends

              </h2>


              <p>

                Analiza tus partidas recientes
                y compara tus métricas de
                rendimiento con referencias
                profesionales según tu rol
                principal.

              </p>


              <form
                className="hero-search"
                onSubmit={
                  analizarRendimiento
                }
              >
              </form>


            </section>

          )
        }


        {/* ======================================================
            CARGANDO
        ====================================================== */}

        {
          cargando && (

            <section className="loading">


              <div className="spinner" />


              <h3>

                Analizando jugador...

              </h3>


              <p>

                Procesando las partidas
                recientes y comparando
                el rendimiento con la
                referencia profesional
                2026.

              </p>


            </section>

          )
        }


        {/* ======================================================
            RESULTADOS
        ====================================================== */}

        {
          analisis &&
          !cargando && (

            <div className="resultados">


              {/* =================================================
                  HERO DEL JUGADOR
              ================================================= */}

              <PlayerHero
                analisis={
                  analisis
                }
              />


              {/* =================================================
                  PARTIDAS RECIENTES
              ================================================= */}

              <RecentMatches
                partidas={
                  analisis
                    .partidas_recientes
                }
              />


              {/* =================================================
                  COMPARACIÓN PROFESIONAL
              ================================================= */}

              <PerformanceComparison
                analisis={
                  analisis
                }
              />


              {/* =================================================
                  ENFRENTAMIENTOS DIRECTOS
              ================================================= */}

              <RoleMatchups
                partidas={
                  analisis
                    .partidas_recientes
                }
              />


              {/* =================================================
                  DISTRIBUCIÓN DE ROLES
              ================================================= */}

              <RoleDistribution
                muestra={
                  analisis
                    .muestra
                }
              />


              {/* =================================================
                  FORTALEZAS Y DEBILIDADES
              ================================================= */}

              <StrengthsWeaknesses
                fortalezas={
                  analisis
                    .fortalezas
                }
                debilidades={
                  analisis
                    .debilidades
                }
              />


              {/* =================================================
                  RECOMENDACIONES
              ================================================= */}

              <Recommendations
                recomendaciones={
                  analisis
                    .recomendaciones
                }
              />


              {/* =================================================
                  FOOTER
              ================================================= */}

              <footer className="analisis-footer">


                <span>

                  RiftLens — Sistema web de análisis
                  de rendimiento competitivo, 2026

                </span>


                <span>

                  Datos vía Riot Games API

                  {" · "}

                  Referencia{" "}

                  {
                    analisis
                      .referencia_profesional
                      .fuente
                  }

                  {" · Temporada 2026"}

                </span>


              </footer>


            </div>

          )
        }


      </main>


    </div>

  );

}


export default App;