import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv("backend/.env")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")

RIOT_API_URL = "https://americas.api.riotgames.com"

# ============================================================
# ARCHIVO LOCAL DE PARTIDAS
# ============================================================

RUTA_PARTIDAS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "partidas.json"
)


def cargar_partidas_guardadas():

    if not os.path.exists(RUTA_PARTIDAS):

        return {
            "jugadores": {}
        }

    try:

        with open(
            RUTA_PARTIDAS,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except json.JSONDecodeError:

        return {
            "jugadores": {}
        }


def guardar_partidas_guardadas(datos):

    os.makedirs(
        os.path.dirname(RUTA_PARTIDAS),
        exist_ok=True
    )

    with open(
        RUTA_PARTIDAS,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

def obtener_rango_jugador(
    puuid: str,
    plataforma: str = "la2"
):

    url = (
        f"https://{plataforma}.api.riotgames.com"
        f"/lol/league/v4/entries/by-puuid/{puuid}"
    )

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code == 429:
            raise RiotRateLimitException(
                "Se alcanzó el límite de solicitudes de Riot API."
            )

        response.raise_for_status()

        ligas = response.json()


        # ================================================
        # BUSCAR SOLO/DUO
        # ================================================

        solo_duo = next(
            (
                liga
                for liga in ligas
                if liga.get("queueType")
                == "RANKED_SOLO_5x5"
            ),
            None
        )


        if not solo_duo:

            return {
                "clasificado": False,
                "cola": "Solo/Duo",
                "tier": None,
                "division": None,
                "lp": 0,
                "victorias": 0,
                "derrotas": 0
            }


        return {

            "clasificado": True,

            "cola": "Solo/Duo",

            "tier":
                solo_duo.get(
                    "tier"
                ),

            "division":
                solo_duo.get(
                    "rank"
                ),

            "lp":
                solo_duo.get(
                    "leaguePoints",
                    0
                ),

            "victorias":
                solo_duo.get(
                    "wins",
                    0
                ),

            "derrotas":
                solo_duo.get(
                    "losses",
                    0
                )
        }


    except RiotRateLimitException:
        raise

    except Exception as error:

        print(
            "Error obteniendo rango:",
            error
        )

        return {
            "clasificado": False,
            "cola": "Solo/Duo",
            "tier": None,
            "division": None,
            "lp": 0,
            "victorias": 0,
            "derrotas": 0
        }
        
# ============================================================
# EXCEPCIÓN PARA LÍMITE DE RIOT API
# ============================================================

class RiotRateLimitException(Exception):

    def __init__(self, mensaje, retry_after=None):
        self.mensaje = mensaje
        self.retry_after = retry_after

        super().__init__(mensaje)


# ============================================================
# 1. OBTENER CUENTA POR RIOT ID
# ============================================================

def obtener_cuenta_por_riot_id(game_name: str, tag_line: str):

    if not RIOT_API_KEY:
        raise Exception(
            "No se encontró RIOT_API_KEY en el archivo .env"
        )

    url = (
        f"{RIOT_API_URL}"
        f"/riot/account/v1/accounts/by-riot-id/"
        f"{game_name}/{tag_line}"
    )

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    if response.status_code == 400:
        raise Exception(
            "Solicitud incorrecta a Riot API."
        )

    if response.status_code == 401:
        raise Exception(
            "API Key no autorizada."
        )

    if response.status_code == 403:
        raise Exception(
            "API Key inválida o expirada."
        )

    if response.status_code == 404:
        raise Exception(
            "No se encontró el jugador."
        )

    if response.status_code == 429:

        retry_after = response.headers.get(
            "Retry-After"
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        f"Error de Riot API. Código HTTP: {response.status_code}"
    )


# ============================================================
# 2. OBTENER IDS DE PARTIDAS POR PUUID
# ============================================================

def obtener_ids_partidas_por_puuid(
    puuid: str,
    start: int = 0,
    count: int = 100
):

    if not RIOT_API_KEY:
        raise Exception(
            "No se encontró RIOT_API_KEY en el archivo .env"
        )

    url = (
        f"{RIOT_API_URL}"
        f"/lol/match/v5/matches/by-puuid/"
        f"{puuid}/ids"
    )

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }

    params = {
        "start": start,
        "count": count
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    if response.status_code == 400:
        raise Exception(
            "Solicitud incorrecta a Riot API."
        )

    if response.status_code == 401:
        raise Exception(
            "API Key no autorizada."
        )

    if response.status_code == 403:
        raise Exception(
            "API Key inválida o expirada."
        )

    if response.status_code == 404:
        raise Exception(
            "No se encontraron partidas para el jugador."
        )

    if response.status_code == 429:

        retry_after = response.headers.get(
            "Retry-After"
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        f"Error de Riot API. Código HTTP: {response.status_code}"
    )


# ============================================================
# 3. OBTENER INFORMACIÓN DE UNA PARTIDA
# ============================================================

def obtener_partida_por_id(match_id: str):

    if not RIOT_API_KEY:
        raise Exception(
            "No se encontró RIOT_API_KEY en el archivo .env"
        )

    url = (
        f"{RIOT_API_URL}"
        f"/lol/match/v5/matches/{match_id}"
    )

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    if response.status_code == 400:
        raise Exception(
            "Solicitud incorrecta a Riot API."
        )

    if response.status_code == 401:
        raise Exception(
            "API Key no autorizada."
        )

    if response.status_code == 403:
        raise Exception(
            "API Key inválida o expirada."
        )

    if response.status_code == 404:
        raise Exception(
            "No se encontró la partida."
        )

    if response.status_code == 429:

        retry_after = response.headers.get(
            "Retry-After"
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        f"Error de Riot API. Código HTTP: {response.status_code}"
    )


# ============================================================
# 4. EXTRAER ESTADÍSTICAS DEL JUGADOR
# ============================================================

def extraer_estadisticas_jugador(
    partida: dict,
    puuid: str
):
    """
    Extrae las estadísticas principales del jugador
    y también identifica al rival del equipo contrario
    que ocupó la misma posición.

    Esto permite posteriormente mostrar en el frontend:

        Sylas VS Bel'Veth
        Ahri VS Syndra
        Jhin VS Kai'Sa

    según el rol de cada partida.
    """

    # ========================================================
    # INFORMACIÓN GENERAL DE LA PARTIDA
    # ========================================================

    info = partida.get(
        "info",
        {}
    )

    participantes = info.get(
        "participants",
        []
    )

    if not participantes:
        raise Exception(
            "La partida no contiene participantes."
        )


    # ========================================================
    # BUSCAR JUGADOR
    # ========================================================

    jugador = None

    for participante in participantes:

        if participante.get(
            "puuid"
        ) == puuid:

            jugador = participante
            break


    if not jugador:
        raise Exception(
            "El jugador no se encuentra en esta partida."
        )


    # ========================================================
    # DATOS DEL JUGADOR
    # ========================================================

    team_id_jugador = jugador.get(
        "teamId"
    )

    posicion = jugador.get(
        "teamPosition"
    )

    champion_name = jugador.get(
        "championName"
    )

    champion_id = jugador.get(
        "championId"
    )


    # ========================================================
    # BUSCAR RIVAL DE LA MISMA POSICIÓN
    # ========================================================

    rival_rol = None


    if posicion:

        for participante in participantes:

            # No puede ser el mismo jugador
            if participante.get(
                "puuid"
            ) == puuid:
                continue

            # Debe pertenecer al equipo contrario
            if participante.get(
                "teamId"
            ) == team_id_jugador:
                continue

            # Debe ocupar la misma posición
            if participante.get(
                "teamPosition"
            ) != posicion:
                continue


            # ------------------------------------------------
            # Encontramos al rival directo del rol
            # ------------------------------------------------

            rival_kills = participante.get(
                "kills",
                0
            )

            rival_deaths = participante.get(
                "deaths",
                0
            )

            rival_assists = participante.get(
                "assists",
                0
            )


            if rival_deaths > 0:

                rival_kda = (
                    rival_kills
                    + rival_assists
                ) / rival_deaths

            else:

                rival_kda = (
                    rival_kills
                    + rival_assists
                )


            rival_rol = {

                "puuid":
                    participante.get(
                        "puuid"
                    ),

                "nombre":
                    participante.get(
                        "riotIdGameName"
                    ),

                "tag":
                    participante.get(
                        "riotIdTagline"
                    ),

                "team_id":
                    participante.get(
                        "teamId"
                    ),

                "posicion":
                    participante.get(
                        "teamPosition"
                    ),

                "campeon": {

                    "id":
                        participante.get(
                            "championId"
                        ),

                    "nombre":
                        participante.get(
                            "championName"
                        ),

                    "nivel":
                        participante.get(
                            "champLevel"
                        )
                },

                "combate": {

                    "kills":
                        rival_kills,

                    "muertes":
                        rival_deaths,

                    "asistencias":
                        rival_assists,

                    "kda":
                        round(
                            rival_kda,
                            2
                        )
                },

                "resultado": {

                    "victoria":
                        participante.get(
                            "win",
                            False
                        )
                }
            }

            break


    # ========================================================
    # DURACIÓN
    # ========================================================

    game_duration = info.get(
        "gameDuration",
        0
    )

    minutos = (
        game_duration / 60
        if game_duration
        else 0
    )


    # ========================================================
    # DATOS GENERALES
    # ========================================================

    queue_id = info.get(
        "queueId"
    )


    # ========================================================
    # COMBATE
    # ========================================================

    kills = jugador.get(
        "kills",
        0
    )

    deaths = jugador.get(
        "deaths",
        0
    )

    assists = jugador.get(
        "assists",
        0
    )


    if deaths > 0:

        kda = (
            kills
            + assists
        ) / deaths

    else:

        kda = (
            kills
            + assists
        )


    # ========================================================
    # FARMEO
    # ========================================================

    cs = (
        jugador.get(
            "totalMinionsKilled",
            0
        )
        +
        jugador.get(
            "neutralMinionsKilled",
            0
        )
    )


    cs_por_minuto = (
        cs / minutos
        if minutos > 0
        else 0
    )


    # ========================================================
    # ECONOMÍA
    # ========================================================

    oro = jugador.get(
        "goldEarned",
        0
    )


    oro_por_minuto = (
        oro / minutos
        if minutos > 0
        else 0
    )


    # ========================================================
    # DAÑO
    # ========================================================

    daño = jugador.get(
        "totalDamageDealtToChampions",
        0
    )


    daño_por_minuto = (
        daño / minutos
        if minutos > 0
        else 0
    )


    # ========================================================
    # RESPUESTA
    # ========================================================

    return {

        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        "jugador": {

            "puuid":
                puuid,

            "nombre":
                jugador.get(
                    "riotIdGameName"
                ),

            "tag":
                jugador.get(
                    "riotIdTagline"
                ),

            "team_id":
                team_id_jugador
        },


        # ----------------------------------------------------
        # PARTIDA
        # ----------------------------------------------------

        "partida": {

            "match_id":
                partida.get(
                    "metadata",
                    {}
                ).get(
                    "matchId"
                ),

            "modo":
                info.get(
                    "gameMode"
                ),

            "queue_id":
                queue_id,

            "posicion":
                posicion,

            "duracion_segundos":
                game_duration,

            "duracion_minutos":
                round(
                    minutos,
                    2
                ),

            "game_creation":
                info.get(
                    "gameCreation"
                ),

            "game_end_timestamp":
                info.get(
                    "gameEndTimestamp"
                )
        },


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        "resultado": {

            "victoria":
                jugador.get(
                    "win",
                    False
                )
        },


        # ----------------------------------------------------
        # CAMPEÓN
        # ----------------------------------------------------

        "campeon": {

            "id":
                champion_id,

            "nombre":
                champion_name,

            "nivel":
                jugador.get(
                    "champLevel"
                )
        },


        # ----------------------------------------------------
        # COMBATE
        # ----------------------------------------------------

        "combate": {

            "kills":
                kills,

            "muertes":
                deaths,

            "asistencias":
                assists,

            "kda":
                round(
                    kda,
                    2
                )
        },


        # ----------------------------------------------------
        # FARMEO
        # ----------------------------------------------------

        "farmeo": {

            "cs":
                cs,

            "cs_por_minuto":
                round(
                    cs_por_minuto,
                    2
                )
        },


        # ----------------------------------------------------
        # ECONOMÍA
        # ----------------------------------------------------

        "economia": {

            "oro":
                oro,

            "oro_por_minuto":
                round(
                    oro_por_minuto,
                    2
                )
        },


        # ----------------------------------------------------
        # DAÑO
        # ----------------------------------------------------

        "daño": {

            "daño_campeones":
                daño,

            "daño_por_minuto":
                round(
                    daño_por_minuto,
                    2
                )
        },


        # ----------------------------------------------------
        # VISIÓN
        # ----------------------------------------------------

        "vision": {

            "vision_score":
                jugador.get(
                    "visionScore",
                    0
                ),

            "wards_colocados":
                jugador.get(
                    "wardsPlaced",
                    0
                ),

            "wards_eliminados":
                jugador.get(
                    "wardsKilled",
                    0
                ),

            "control_wards":
                jugador.get(
                    "visionWardsBoughtInGame",
                    0
                )
        },


        # ----------------------------------------------------
        # RIVAL DEL MISMO ROL
        # ----------------------------------------------------

        "rival_rol":
            rival_rol
    }


# ============================================================
# 5. OBTENER ESTADÍSTICAS DE LAS ÚLTIMAS PARTIDAS
# ============================================================

def obtener_estadisticas_ultimas_partidas(
    puuid: str,
    count: int = 100
):
    """
    Obtiene las últimas partidas del jugador.

    Utiliza partidas.json como caché.

    Si una partida antigua fue almacenada antes de incorporar
    la información del rival de rol, esa partida se vuelve
    a consultar para actualizar su estructura.
    """

    # ========================================================
    # 1. CARGAR PARTIDAS GUARDADAS
    # ========================================================

    datos = cargar_partidas_guardadas()

    jugadores = datos.setdefault(
        "jugadores",
        {}
    )

    jugador_guardado = jugadores.get(
        puuid,
        {}
    )

    partidas_guardadas = jugador_guardado.get(
        "partidas",
        {}
    )


    # ========================================================
    # 2. OBTENER IDS RECIENTES
    # ========================================================

    partidas_ids = obtener_ids_partidas_por_puuid(
        puuid=puuid,
        start=0,
        count=count
    )


    resultados = []

    nuevas_consultas = 0

    datos_modificados = False


    # ========================================================
    # 3. PROCESAR PARTIDAS
    # ========================================================

    for match_id in partidas_ids:

        partida_guardada = partidas_guardadas.get(
            match_id
        )


        # ----------------------------------------------------
        # DETERMINAR SI EL CACHÉ YA TIENE LA NUEVA ESTRUCTURA
        # ----------------------------------------------------

        cache_actualizado = (
            isinstance(
                partida_guardada,
                dict
            )
            and
            "rival_rol"
            in partida_guardada
        )


        # ----------------------------------------------------
        # USAR CACHÉ ACTUALIZADO
        # ----------------------------------------------------

        if cache_actualizado:

            resultados.append(
                partida_guardada
            )

            continue


        # ----------------------------------------------------
        # SI NO EXISTE O ES ANTIGUO, CONSULTAR RIOT
        # ----------------------------------------------------

        try:

            if nuevas_consultas > 0:

                time.sleep(
                    1.2
                )


            partida_completa = (
                obtener_partida_por_id(
                    match_id
                )
            )


            estadisticas = (
                extraer_estadisticas_jugador(
                    partida_completa,
                    puuid
                )
            )


            # ------------------------------------------------
            # ACTUALIZAR CACHÉ
            # ------------------------------------------------

            partidas_guardadas[
                match_id
            ] = estadisticas


            resultados.append(
                estadisticas
            )


            nuevas_consultas += 1

            datos_modificados = True


        except RiotRateLimitException as e:

            resultados.append({

                "match_id":
                    match_id,

                "error":
                    e.mensaje,

                "retry_after":
                    e.retry_after
            })

            break


        except Exception as e:

            resultados.append({

                "match_id":
                    match_id,

                "error":
                    str(e)
            })


    # ========================================================
    # 4. OBTENER NOMBRE Y TAG
    # ========================================================

    nombre = jugador_guardado.get(
        "nombre"
    )

    tag = jugador_guardado.get(
        "tag"
    )


    for partida in resultados:

        if not isinstance(
            partida,
            dict
        ):
            continue

        datos_jugador = partida.get(
            "jugador"
        )

        if not datos_jugador:
            continue


        nombre = datos_jugador.get(
            "nombre"
        )

        tag = datos_jugador.get(
            "tag"
        )

        break


    # ========================================================
    # 5. ACTUALIZAR JUGADOR EN CACHÉ
    # ========================================================

    jugadores[
        puuid
    ] = {

        "puuid":
            puuid,

        "nombre":
            nombre,

        "tag":
            tag,

        "partidas":
            partidas_guardadas
    }


    # ========================================================
    # 6. GUARDAR JSON
    # ========================================================

    if (
        datos_modificados
        or
        puuid not in datos.get(
            "jugadores",
            {}
        )
    ):

        guardar_partidas_guardadas(
            datos
        )

    else:

        # También guardamos para mantener metadatos
        # del jugador sincronizados.
        guardar_partidas_guardadas(
            datos
        )


    # ========================================================
    # 7. RETORNAR RESULTADOS
    # ========================================================

    return resultados