import {
  useEffect,
} from "react";

import type {
  PartidaReciente,
  ParticipantePartida,
} from "../types/analisis";

import {
  formatearRol,
} from "../utils/formatters";


interface MatchDetailModalProps {
  partida: PartidaReciente;
  onCerrar: () => void;
}


function MatchDetailModal({
  partida,
  onCerrar,
}: MatchDetailModalProps) {

  useEffect(() => {

    const manejarEscape = (
      event: KeyboardEvent
    ) => {

      if (
        event.key === "Escape"
      ) {

        onCerrar();

      }

    };


    document.addEventListener(
      "keydown",
      manejarEscape
    );


    document.body.style.overflow =
      "hidden";


    return () => {

      document.removeEventListener(
        "keydown",
        manejarEscape
      );

      document.body.style.overflow =
        "";

    };

  }, [onCerrar]);


  const aliados =
    partida.equipos?.aliados ?? [];

  const rivales =
    partida.equipos?.rivales ?? [];


  const totalKills = (
    jugadores: ParticipantePartida[]
  ) =>
    jugadores.reduce(
      (
        total,
        jugador
      ) =>
        total +
        jugador.combate.kills,
      0
    );


  const totalOro = (
    jugadores: ParticipantePartida[]
  ) =>
    jugadores.reduce(
      (
        total,
        jugador
      ) =>
        total +
        jugador.recursos.oro,
      0
    );


  const totalVision = (
    jugadores: ParticipantePartida[]
  ) =>
    jugadores.reduce(
      (
        total,
        jugador
      ) =>
        total +
        jugador.vision.score,
      0
    );


  const formatearOro = (
    oro: number
  ) => {

    return `${(
      oro / 1000
    ).toFixed(1)}k`;

  };


    const DATA_DRAGON_VERSION =
    "14.24.1";


  const obtenerIconoCampeon = (
    nombre: string | null
  ) => {

    if (!nombre) {
      return null;
    }

    const nombreNormalizado =
      nombre.replace(
        /[^a-zA-Z0-9]/g,
        ""
      );

    return (
      "https://ddragon.leagueoflegends.com/" +
      `cdn/${DATA_DRAGON_VERSION}/img/champion/` +
      `${nombreNormalizado}.png`
    );

  };


  const obtenerIconoObjeto = (
    itemId: number
  ) => {

    if (!itemId) {
      return null;
    }

    return (
      "https://ddragon.leagueoflegends.com/" +
      `cdn/${DATA_DRAGON_VERSION}/img/item/` +
      `${itemId}.png`
    );

  };


  const renderJugador = (
    jugador: ParticipantePartida
  ) => {

    const iconoCampeon =
      obtenerIconoCampeon(
        jugador.campeon.nombre
      );


    return (

      <div
        key={
          jugador.puuid ??
          `${jugador.nombre}-${jugador.campeon.nombre}`
        }
        className={
          jugador.es_jugador
            ? "modal-player-row highlighted"
            : "modal-player-row"
        }
      >


        <div className="modal-player-main">

          {
            iconoCampeon && (

              <img
                src={
                  iconoCampeon
                }
                alt={
                  jugador
                    .campeon
                    .nombre ??
                  "Campeón"
                }
                className="modal-champion-icon"
                onError={(event) => {

                  event
                    .currentTarget
                    .style
                    .display =
                    "none";

                }}
              />

            )
          }


          <div className="modal-player-name">

            <strong>

              {
                jugador.nombre ??
                "Jugador"
              }

              {
                jugador.tag
                  ? `#${jugador.tag}`
                  : ""
              }

            </strong>

            <span>

              {
                formatearRol(
                  jugador.posicion
                )
              }

              {" · Nv. "}

              {
                jugador
                  .campeon
                  .nivel ??
                "-"
              }

            </span>

          </div>

        </div>


        <div className="modal-player-kda">

          <strong>

            {
              jugador
                .combate
                .kills
            }

            /

            {
              jugador
                .combate
                .muertes
            }

            /

            {
              jugador
                .combate
                .asistencias
            }

          </strong>

          <span>

            KDA{" "}

            {
              jugador
                .combate
                .kda
                .toFixed(2)
            }

          </span>

        </div>


        <div className="modal-player-stats">

          <span>

            {
              jugador
                .recursos
                .cs
            }

            {" CS"}

          </span>

          <span>

            {
              formatearOro(
                jugador
                  .recursos
                  .oro
              )
            }

            {" oro"}

          </span>

          <span>

            {
              jugador
                .daño
                .campeones
                .toLocaleString()
            }

            {" daño"}

          </span>

          <span>

            Visión{" "}

            {
              jugador
                .vision
                .score
            }

          </span>

        </div>


        <div className="modal-items">

          {
            jugador.objetos.map(
              (
                itemId,
                index
              ) => {

                const icono =
                  obtenerIconoObjeto(
                    itemId
                  );

                return (

                  <div
                    key={
                      `${itemId}-${index}`
                    }
                    className="modal-item-slot"
                  >

                    {
                      icono ? (

                        <img
                          src={
                            icono
                          }
                          alt={
                            `Objeto ${itemId}`
                          }
                          onError={(event) => {

                            event
                              .currentTarget
                              .style
                              .display =
                              "none";

                          }}
                        />

                      ) : null
                    }

                  </div>

                );

              }
            )
          }

        </div>


      </div>

    );

  };


  return (

    <div
      className="match-modal-backdrop"
      onMouseDown={
        onCerrar
      }
    >

      <div
        className="match-modal"
        onMouseDown={(
          event
        ) => {

          event.stopPropagation();

        }}
      >


        <div className="match-modal-header">

          <div>

            <span
              className={
                partida.victoria
                  ? "match-modal-result win"
                  : "match-modal-result loss"
              }
            >

              {
                partida.victoria
                  ? "VICTORIA"
                  : "DERROTA"
              }

            </span>


            <h2>

              Detalle de la partida

            </h2>


            <p>

              {
                partida.modo ??
                "Partida"
              }

              {" · "}

              {
                formatearRol(
                  partida.rol
                )
              }

              {" · "}

              {
                Math.round(
                  partida
                    .duracion_minutos
                )
              }

              {" min"}

            </p>

          </div>


          <button
            type="button"
            className="match-modal-close"
            onClick={
              onCerrar
            }
            aria-label="Cerrar detalle"
          >
            ×
          </button>

        </div>


        {
          (
            aliados.length > 0 ||
            rivales.length > 0
          ) ? (

            <>

              <div className="match-modal-score">

                <div>

                  <span>
                    TU EQUIPO
                  </span>

                  <strong>

                    {
                      totalKills(
                        aliados
                      )
                    }

                  </strong>

                </div>


                <span className="match-modal-vs">
                    <b>
                        VS
                    </b>
                </span>


                <div>

                  <span>
                    EQUIPO RIVAL
                  </span>

                  <strong>

                    {
                      totalKills(
                        rivales
                      )
                    }

                  </strong>

                </div>

              </div>


              <div className="match-modal-team-summary">

                <div>

                  <span>
                    Oro total
                  </span>

                  <strong>

                    {
                      formatearOro(
                        totalOro(
                          aliados
                        )
                      )
                    }

                  </strong>

                </div>


                <div>

                  <span>
                    Visión total
                  </span>

                  <strong>

                    {
                      totalVision(
                        aliados
                      )
                    }

                  </strong>

                </div>


                <div>

                  <span>
                    Oro rival
                  </span>

                  <strong>

                    {
                      formatearOro(
                        totalOro(
                          rivales
                        )
                      )
                    }

                  </strong>

                </div>


                <div>

                  <span>
                    Visión rival
                  </span>

                  <strong>

                    {
                      totalVision(
                        rivales
                      )
                    }

                  </strong>

                </div>

              </div>


              <div className="match-modal-teams">

                <div className="match-modal-team">

                  <div className="match-modal-team-title">

                    <span>
                      Tu equipo
                    </span>

                  </div>


                  <div className="match-modal-player-list">

                    {
                      aliados.map(
                        renderJugador
                      )
                    }

                  </div>

                </div>


                <div className="match-modal-team enemy">

                  <div className="match-modal-team-title">

                    <span>
                      Equipo rival
                    </span>

                  </div>


                  <div className="match-modal-player-list">

                    {
                      rivales.map(
                        renderJugador
                      )
                    }

                  </div>

                </div>

              </div>

            </>

          ) : (

            <div className="match-modal-empty">

              <strong>
                Detalle no disponible
              </strong>

              <p>
                Esta partida todavía no contiene
                la información completa de los
                diez participantes.
              </p>

            </div>

          )
        }


      </div>

    </div>

  );

}


export default MatchDetailModal;