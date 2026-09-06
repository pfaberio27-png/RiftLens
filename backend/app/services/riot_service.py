import os
import time
import json
import requests

from dotenv import load_dotenv


load_dotenv("backend/.env")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")


# ============================================================
# CONFIGURACIÓN DE REGIONES RIOT
# ============================================================

PLATAFORMAS_RIOT = {

    "BR": {
        "plataforma": "br1",
        "routing": "americas",
    },

    "LAN": {
        "plataforma": "la1",
        "routing": "americas",
    },

    "LAS": {
        "plataforma": "la2",
        "routing": "americas",
    },

    "NA": {
        "plataforma": "na1",
        "routing": "americas",
    },


    "EUW": {
        "plataforma": "euw1",
        "routing": "europe",
    },

    "EUNE": {
        "plataforma": "eun1",
        "routing": "europe",
    },

    "TR": {
        "plataforma": "tr1",
        "routing": "europe",
    },

    "RU": {
        "plataforma": "ru",
        "routing": "europe",
    },


    "KR": {
        "plataforma": "kr",
        "routing": "asia",
    },

    "JP": {
        "plataforma": "jp1",
        "routing": "asia",
    },


    "OCE": {
        "plataforma": "oc1",
        "routing": "sea",
    },

    "PH": {
        "plataforma": "ph2",
        "routing": "sea",
    },

    "SG": {
        "plataforma": "sg2",
        "routing": "sea",
    },

    "TH": {
        "plataforma": "th2",
        "routing": "sea",
    },

    "TW": {
        "plataforma": "tw2",
        "routing": "sea",
    },

    "VN": {
        "plataforma": "vn2",
        "routing": "sea",
    },
}


# ============================================================
# ARCHIVO LOCAL DE PARTIDAS
# ============================================================

RUTA_PARTIDAS = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)
    ),
    "data",
    "partidas.json"
)


# ============================================================
# EXCEPCIÓN PARA LÍMITE DE RIOT API
# ============================================================

class RiotRateLimitException(Exception):

    def __init__(
        self,
        mensaje,
        retry_after=None
    ):
        self.mensaje = mensaje
        self.retry_after = retry_after

        super().__init__(
            mensaje
        )


# ============================================================
# CONFIGURACIÓN DE REGIÓN
# ============================================================

def obtener_configuracion_region(
    region: str
):

    region_normalizada = (
        region
        .strip()
        .upper()
    )

    configuracion = (
        PLATAFORMAS_RIOT.get(
            region_normalizada
        )
    )

    if not configuracion:

        raise Exception(
            f"Región no soportada: {region}"
        )

    return configuracion


def obtener_url_regional(
    region: str
):

    configuracion = (
        obtener_configuracion_region(
            region
        )
    )

    routing = (
        configuracion[
            "routing"
        ]
    )

    return (
        f"https://{routing}.api.riotgames.com"
    )


def obtener_url_plataforma(
    region: str
):

    configuracion = (
        obtener_configuracion_region(
            region
        )
    )

    plataforma = (
        configuracion[
            "plataforma"
        ]
    )

    return (
        f"https://{plataforma}.api.riotgames.com"
    )


# ============================================================
# FUNCIONES DE CACHÉ
# ============================================================

def cargar_partidas_guardadas():

    if not os.path.exists(
        RUTA_PARTIDAS
    ):

        return {
            "jugadores": {}
        }

    try:

        with open(
            RUTA_PARTIDAS,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(
                archivo
            )

    except json.JSONDecodeError:

        return {
            "jugadores": {}
        }


def guardar_partidas_guardadas(
    datos
):

    os.makedirs(
        os.path.dirname(
            RUTA_PARTIDAS
        ),
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


# ============================================================
# FUNCIÓN AUXILIAR PARA VALIDAR API KEY
# ============================================================

def validar_api_key():

    if not RIOT_API_KEY:

        raise Exception(
            "No se encontró RIOT_API_KEY en el archivo .env"
        )


# ============================================================
# 1. OBTENER CUENTA POR RIOT ID
# ============================================================

def obtener_cuenta_por_riot_id(
    game_name: str,
    tag_line: str,
    region: str
):

    validar_api_key()

    base_url = (
        obtener_url_regional(
            region
        )
    )

    url = (
        f"{base_url}"
        f"/riot/account/v1/accounts/by-riot-id/"
        f"{game_name}/{tag_line}"
    )

    headers = {
        "X-Riot-Token":
            RIOT_API_KEY
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

        retry_after = (
            response.headers.get(
                "Retry-After"
            )
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        "Error de Riot API. "
        f"Código HTTP: {response.status_code}"
    )


# ============================================================
# 2. OBTENER RANGO DEL JUGADOR
# ============================================================

def obtener_rango_jugador(
    puuid: str,
    region: str
):

    validar_api_key()

    base_url = (
        obtener_url_plataforma(
            region
        )
    )

    url = (
        f"{base_url}"
        f"/lol/league/v4/entries/by-puuid/{puuid}"
    )

    headers = {
        "X-Riot-Token":
            RIOT_API_KEY
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code == 429:

            retry_after = (
                response.headers.get(
                    "Retry-After"
                )
            )

            raise RiotRateLimitException(
                "Se alcanzó el límite de solicitudes de Riot API.",
                retry_after
            )

        if response.status_code == 401:

            raise Exception(
                "API Key no autorizada."
            )

        if response.status_code == 403:

            raise Exception(
                "API Key inválida o expirada."
            )

        response.raise_for_status()

        ligas = response.json()

        solo_duo = next(
            (
                liga
                for liga in ligas
                if (
                    liga.get(
                        "queueType"
                    )
                    ==
                    "RANKED_SOLO_5x5"
                )
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
# 3. OBTENER IDS DE PARTIDAS POR PUUID
# ============================================================

def obtener_ids_partidas_por_puuid(
    puuid: str,
    region: str,
    start: int = 0,
    count: int = 100
):

    validar_api_key()

    base_url = (
        obtener_url_regional(
            region
        )
    )

    url = (
        f"{base_url}"
        f"/lol/match/v5/matches/by-puuid/"
        f"{puuid}/ids"
    )

    headers = {
        "X-Riot-Token":
            RIOT_API_KEY
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

        retry_after = (
            response.headers.get(
                "Retry-After"
            )
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        "Error de Riot API. "
        f"Código HTTP: {response.status_code}"
    )


# ============================================================
# 4. OBTENER INFORMACIÓN DE UNA PARTIDA
# ============================================================

def obtener_partida_por_id(
    match_id: str,
    region: str
):

    validar_api_key()

    base_url = (
        obtener_url_regional(
            region
        )
    )

    url = (
        f"{base_url}"
        f"/lol/match/v5/matches/{match_id}"
    )

    headers = {
        "X-Riot-Token":
            RIOT_API_KEY
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

        retry_after = (
            response.headers.get(
                "Retry-After"
            )
        )

        raise RiotRateLimitException(
            "Se alcanzó el límite de solicitudes de Riot API.",
            retry_after
        )

    raise Exception(
        "Error de Riot API. "
        f"Código HTTP: {response.status_code}"
    )


# ============================================================
# 5. EXTRAER ESTADÍSTICAS DEL JUGADOR
# ============================================================

def extraer_estadisticas_jugador(
    partida: dict,
    puuid: str
):
    """
    Extrae las estadísticas principales del jugador
    y también identifica al rival del equipo contrario
    que ocupó la misma posición.
    """

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

        if (
            participante.get(
                "puuid"
            )
            ==
            puuid
        ):

            jugador = participante

            break


    if not jugador:

        raise Exception(
            "El jugador no se encuentra en esta partida."
        )


    # ========================================================
    # DATOS PRINCIPALES
    # ========================================================

    team_id_jugador = (
        jugador.get(
            "teamId"
        )
    )

    posicion = (
        jugador.get(
            "teamPosition"
        )
    )

    champion_name = (
        jugador.get(
            "championName"
        )
    )

    champion_id = (
        jugador.get(
            "championId"
        )
    )


    # ========================================================
    # RIVAL DE LA MISMA POSICIÓN
    # ========================================================

    rival_rol = None

    if posicion:

        for participante in participantes:

            if (
                participante.get(
                    "puuid"
                )
                ==
                puuid
            ):
                continue

            if (
                participante.get(
                    "teamId"
                )
                ==
                team_id_jugador
            ):
                continue

            if (
                participante.get(
                    "teamPosition"
                )
                !=
                posicion
            ):
                continue


            rival_kills = (
                participante.get(
                    "kills",
                    0
                )
            )

            rival_deaths = (
                participante.get(
                    "deaths",
                    0
                )
            )

            rival_assists = (
                participante.get(
                    "assists",
                    0
                )
            )


            if rival_deaths > 0:

                rival_kda = (
                    rival_kills
                    +
                    rival_assists
                ) / rival_deaths

            else:

                rival_kda = (
                    rival_kills
                    +
                    rival_assists
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

    game_duration = (
        info.get(
            "gameDuration",
            0
        )
    )

    minutos = (
        game_duration / 60
        if game_duration
        else 0
    )


    # ========================================================
    # COMBATE
    # ========================================================

    kills = (
        jugador.get(
            "kills",
            0
        )
    )

    deaths = (
        jugador.get(
            "deaths",
            0
        )
    )

    assists = (
        jugador.get(
            "assists",
            0
        )
    )


    if deaths > 0:

        kda = (
            kills
            +
            assists
        ) / deaths

    else:

        kda = (
            kills
            +
            assists
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

    oro = (
        jugador.get(
            "goldEarned",
            0
        )
    )

    oro_por_minuto = (
        oro / minutos
        if minutos > 0
        else 0
    )


    # ========================================================
    # DAÑO
    # ========================================================

    daño = (
        jugador.get(
            "totalDamageDealtToChampions",
            0
        )
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
                info.get(
                    "queueId"
                ),

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


        "resultado": {

            "victoria":
                jugador.get(
                    "win",
                    False
                )
        },


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


        "farmeo": {

            "cs":
                cs,

            "cs_por_minuto":
                round(
                    cs_por_minuto,
                    2
                )
        },


        "economia": {

            "oro":
                oro,

            "oro_por_minuto":
                round(
                    oro_por_minuto,
                    2
                )
        },


        "daño": {

            "daño_campeones":
                daño,

            "daño_por_minuto":
                round(
                    daño_por_minuto,
                    2
                )
        },


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


        "rival_rol":
            rival_rol
    }


# ============================================================
# 6. OBTENER ESTADÍSTICAS DE LAS ÚLTIMAS PARTIDAS
# ============================================================

def obtener_estadisticas_ultimas_partidas(
    puuid: str,
    region: str,
    count: int = 100
):
    """
    Obtiene las últimas partidas del jugador
    utilizando partidas.json como caché.
    """

    datos = (
        cargar_partidas_guardadas()
    )

    jugadores = (
        datos.setdefault(
            "jugadores",
            {}
        )
    )


    # ========================================================
    # CACHÉ SEPARADO POR PUUID + REGIÓN
    # ========================================================

    clave_jugador = (
        f"{region.upper()}:{puuid}"
    )

    jugador_guardado = (
        jugadores.get(
            clave_jugador,
            {}
        )
    )

    partidas_guardadas = (
        jugador_guardado.get(
            "partidas",
            {}
        )
    )


    # ========================================================
    # OBTENER IDS RECIENTES
    # ========================================================

    partidas_ids = (
        obtener_ids_partidas_por_puuid(
            puuid=puuid,
            region=region,
            start=0,
            count=count
        )
    )


    resultados = []

    nuevas_consultas = 0

    datos_modificados = False


    # ========================================================
    # PROCESAR PARTIDAS
    # ========================================================

    for match_id in partidas_ids:

        partida_guardada = (
            partidas_guardadas.get(
                match_id
            )
        )

        cache_actualizado = (
            isinstance(
                partida_guardada,
                dict
            )
            and
            "rival_rol"
            in partida_guardada
        )

        if cache_actualizado:

            resultados.append(
                partida_guardada
            )

            continue


        try:

            if nuevas_consultas > 0:

                time.sleep(
                    1.2
                )


            partida_completa = (
                obtener_partida_por_id(
                    match_id=match_id,
                    region=region
                )
            )


            estadisticas = (
                extraer_estadisticas_jugador(
                    partida_completa,
                    puuid
                )
            )


            partidas_guardadas[
                match_id
            ] = estadisticas


            resultados.append(
                estadisticas
            )


            nuevas_consultas += 1

            datos_modificados = True


        except RiotRateLimitException as error:

            resultados.append({

                "match_id":
                    match_id,

                "error":
                    error.mensaje,

                "retry_after":
                    error.retry_after
            })

            break


        except Exception as error:

            resultados.append({

                "match_id":
                    match_id,

                "error":
                    str(
                        error
                    )
            })


    # ========================================================
    # OBTENER NOMBRE Y TAG
    # ========================================================

    nombre = (
        jugador_guardado.get(
            "nombre"
        )
    )

    tag = (
        jugador_guardado.get(
            "tag"
        )
    )


    for partida in resultados:

        if not isinstance(
            partida,
            dict
        ):
            continue

        datos_jugador = (
            partida.get(
                "jugador"
            )
        )

        if not datos_jugador:
            continue

        nombre = (
            datos_jugador.get(
                "nombre"
            )
        )

        tag = (
            datos_jugador.get(
                "tag"
            )
        )

        break


    # ========================================================
    # ACTUALIZAR CACHÉ
    # ========================================================

    jugadores[
        clave_jugador
    ] = {

        "puuid":
            puuid,

        "region":
            region.upper(),

        "nombre":
            nombre,

        "tag":
            tag,

        "partidas":
            partidas_guardadas
    }


    if (
        datos_modificados
        or
        clave_jugador
        not in jugadores
    ):

        guardar_partidas_guardadas(
            datos
        )

    else:

        guardar_partidas_guardadas(
            datos
        )


    return resultados