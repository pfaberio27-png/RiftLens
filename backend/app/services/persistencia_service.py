from datetime import datetime

from sqlalchemy import select

from backend.app.database import (
    DB_ENABLED,
    SessionLocal,
)

from backend.app.models import (
    EstadisticaPartida,
    Jugador,
    Partida,
)


# ============================================================
# AUXILIAR - TIMESTAMP RIOT → DATETIME
# ============================================================

def convertir_timestamp_riot(timestamp):

    if not timestamp:
        return None

    try:
        return datetime.fromtimestamp(
            timestamp / 1000
        )

    except (TypeError, ValueError, OSError):
        return None


# ============================================================
# GUARDAR ANÁLISIS EN SQL SERVER
# ============================================================

def guardar_partidas_sql(
    puuid: str,
    region: str,
    partidas: list,
):
    """
    Persiste en SQL Server el jugador, las partidas y
    las estadísticas obtenidas desde Riot.

    Evita duplicar:
        - jugador por PUUID
        - partida por match_id
        - estadística por jugador + partida
    """

    if not DB_ENABLED or SessionLocal is None:

        return {
            "habilitado": False,
            "jugador_nuevo": False,
            "partidas_nuevas": 0,
            "estadisticas_nuevas": 0,
            "omitidas": 0,
        }

    db = SessionLocal()

    resumen = {
        "jugador_nuevo": False,
        "partidas_nuevas": 0,
        "estadisticas_nuevas": 0,
        "omitidas": 0,
    }

    try:

        # ====================================================
        # OBTENER PRIMERA PARTIDA VÁLIDA
        # ====================================================

        partidas_validas = [
            partida
            for partida in partidas
            if (
                isinstance(partida, dict)
                and
                "error" not in partida
                and
                partida.get("jugador")
                and
                partida.get("partida")
            )
        ]

        if not partidas_validas:
            return resumen


        primera = partidas_validas[0]

        datos_jugador = primera.get(
            "jugador",
            {},
        )


        nombre = (
            datos_jugador.get("nombre")
            or "Desconocido"
        )

        tag = (
            datos_jugador.get("tag")
            or "UNKNOWN"
        )


        # ====================================================
        # JUGADOR
        # ====================================================

        jugador = db.scalar(
            select(Jugador).where(
                Jugador.puuid == puuid
            )
        )


        if jugador is None:

            jugador = Jugador(
                puuid=puuid,
                riot_name=nombre,
                tag_line=tag,
                region=region.upper(),
            )

            db.add(jugador)

            # Necesitamos jugador_id antes de continuar.
            db.flush()

            resumen[
                "jugador_nuevo"
            ] = True

        else:

            jugador.riot_name = nombre
            jugador.tag_line = tag
            jugador.region = region.upper()
            jugador.fecha_ultima_actualizacion = (
                datetime.now()
            )


        # ====================================================
        # PARTIDAS
        # ====================================================

        for datos in partidas_validas:

            datos_partida = datos.get(
                "partida",
                {},
            )

            match_id = datos_partida.get(
                "match_id"
            )


            if not match_id:

                resumen["omitidas"] += 1

                continue


            # ================================================
            # BUSCAR / CREAR PARTIDA
            # ================================================

            partida_db = db.scalar(
                select(Partida).where(
                    Partida.match_id
                    ==
                    match_id
                )
            )


            if partida_db is None:

                fecha_partida = (
                    convertir_timestamp_riot(
                        datos_partida.get(
                            "game_creation"
                        )
                    )
                )


                partida_db = Partida(
                    match_id=match_id,
                    queue_id=datos_partida.get(
                        "queue_id"
                    ),
                    modo=datos_partida.get(
                        "modo"
                    ),
                    duracion_segundos=datos_partida.get(
                        "duracion_segundos"
                    ),
                    fecha_partida=fecha_partida,
                )

                db.add(partida_db)

                db.flush()

                resumen[
                    "partidas_nuevas"
                ] += 1


            # ================================================
            # EVITAR ESTADÍSTICA DUPLICADA
            # ================================================

            estadistica_existente = db.scalar(
                select(
                    EstadisticaPartida
                ).where(
                    EstadisticaPartida.jugador_id
                    ==
                    jugador.jugador_id,

                    EstadisticaPartida.partida_id
                    ==
                    partida_db.partida_id,
                )
            )


            if estadistica_existente:

                resumen["omitidas"] += 1

                continue


            # ================================================
            # EXTRAER BLOQUES
            # ================================================

            resultado = datos.get(
                "resultado",
                {},
            )

            campeon = datos.get(
                "campeon",
                {},
            )

            combate = datos.get(
                "combate",
                {},
            )

            farmeo = datos.get(
                "farmeo",
                {},
            )

            economia = datos.get(
                "economia",
                {},
            )

            daño = datos.get(
                "daño",
                {},
            )

            vision = datos.get(
                "vision",
                {},
            )


            # ================================================
            # CREAR ESTADÍSTICA
            # ================================================

            estadistica = EstadisticaPartida(

                jugador_id=
                    jugador.jugador_id,

                partida_id=
                    partida_db.partida_id,

                campeon=
                    campeon.get("nombre"),

                rol=
                    datos_partida.get(
                        "posicion"
                    ),

                victoria=
                    bool(
                        resultado.get(
                            "victoria",
                            False,
                        )
                    ),

                kills=
                    int(
                        combate.get(
                            "kills",
                            0,
                        )
                        or 0
                    ),

                deaths=
                    int(
                        combate.get(
                            "muertes",
                            0,
                        )
                        or 0
                    ),

                assists=
                    int(
                        combate.get(
                            "asistencias",
                            0,
                        )
                        or 0
                    ),

                kda=
                    float(
                        combate.get(
                            "kda",
                            0,
                        )
                        or 0
                    ),

                cs=
                    int(
                        farmeo.get(
                            "cs",
                            0,
                        )
                        or 0
                    ),

                cs_por_minuto=
                    float(
                        farmeo.get(
                            "cs_por_minuto",
                            0,
                        )
                        or 0
                    ),

                oro=
                    int(
                        economia.get(
                            "oro",
                            0,
                        )
                        or 0
                    ),

                oro_por_minuto=
                    float(
                        economia.get(
                            "oro_por_minuto",
                            0,
                        )
                        or 0
                    ),

                daño_campeones=
                    int(
                        daño.get(
                            "daño_campeones",
                            0,
                        )
                        or 0
                    ),

                daño_por_minuto=
                    float(
                        daño.get(
                            "daño_por_minuto",
                            0,
                        )
                        or 0
                    ),

                vision_score=
                    int(
                        vision.get(
                            "vision_score",
                            0,
                        )
                        or 0
                    ),
            )


            db.add(
                estadistica
            )

            resumen[
                "estadisticas_nuevas"
            ] += 1


        # ====================================================
        # CONFIRMAR TRANSACCIÓN
        # ====================================================

        db.commit()

        return resumen


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()