from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.services.riot_service import (
    RiotRateLimitException,
    obtener_cuenta_por_riot_id,
    obtener_ids_partidas_por_puuid,
    obtener_partida_por_id,
    extraer_estadisticas_jugador,
    obtener_estadisticas_ultimas_partidas,
    obtener_rango_jugador
)

from backend.app.services.analisis_service import (
    calcular_promedios,
    analizar_jugador_con_referencia
)


# ============================================================
# MODELOS
# ============================================================

class AnalisisJugadorRequest(BaseModel):
    riot_id: str = Field(
        ...,
        min_length=3,
        description="Riot ID del jugador en formato Nombre#TAG",
        examples=["Faker#KR1"]
    )


# ============================================================
# CONFIGURACIÓN FASTAPI
# ============================================================

app = FastAPI(
    title="Sistema de Análisis de Rendimiento LOL",
    description=(
        "API para analizar el rendimiento individual de jugadores "
        "de League of Legends y compararlo contra referencias "
        "profesionales obtenidas de Oracle's Elixir."
    ),
    version="2.0.0"
)


# ============================================================
# CONFIGURACIÓN CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://rift-lens-eta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def validar_riot_id(riot_id: str):
    """
    Valida un Riot ID y devuelve game_name y tag_line.
    """

    riot_id = riot_id.strip()

    if "#" not in riot_id:
        raise HTTPException(
            status_code=400,
            detail="El Riot ID debe tener el formato Nombre#TAG."
        )

    game_name, tag_line = riot_id.split("#", 1)

    game_name = game_name.strip()
    tag_line = tag_line.strip()

    if not game_name or not tag_line:
        raise HTTPException(
            status_code=400,
            detail="El Riot ID no puede contener campos vacíos."
        )

    return game_name, tag_line


def manejar_rate_limit(error: RiotRateLimitException):
    """
    Convierte la excepción de rate limit de Riot
    en una respuesta HTTP 429.
    """

    detail = error.mensaje

    if error.retry_after:
        detail += (
            f" Espera aproximadamente {error.retry_after} "
            "segundos antes de volver a intentarlo."
        )

    raise HTTPException(
        status_code=429,
        detail=detail
    )


# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@app.get("/")
def inicio():
    return {
        "mensaje": (
            "API del Sistema de Análisis de Rendimiento LOL "
            "funcionando correctamente"
        ),
        "version": "2.0.0",
        "modelo_analisis": (
            "Jugador individual vs referencia profesional por rol"
        )
    }


# ============================================================
# OBTENER JUGADOR POR RIOT ID
# ============================================================

@app.get("/api/jugador")
def obtener_jugador(
    riot_id: str = Query(
        ...,
        description="Riot ID en formato Nombre#TAG"
    )
):
    try:

        game_name, tag_line = validar_riot_id(
            riot_id
        )

        cuenta = obtener_cuenta_por_riot_id(
            game_name,
            tag_line
        )

        puuid = cuenta.get("puuid")

        if not puuid:
            raise HTTPException(
                status_code=404,
                detail="No se pudo obtener el PUUID del jugador."
            )

        return {
            "mensaje": "Jugador encontrado correctamente",
            "riot_id": (
                f"{cuenta.get('gameName', game_name)}"
                f"#{cuenta.get('tagLine', tag_line)}"
            ),
            "puuid": puuid,
            "gameName": cuenta.get(
                "gameName",
                game_name
            ),
            "tagLine": cuenta.get(
                "tagLine",
                tag_line
            )
        }

    except HTTPException:
        raise

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OBTENER IDS DE PARTIDAS POR PUUID
# ============================================================

@app.get("/api/jugador/{puuid}/partidas")
def obtener_partidas(
    puuid: str,
    start: int = Query(
        0,
        ge=0,
        description="Índice desde donde comenzar"
    ),
    count: int = Query(
        20,
        ge=1,
        le=100,
        description="Cantidad de partidas a obtener"
    )
):
    try:

        partidas = obtener_ids_partidas_por_puuid(
            puuid=puuid,
            start=start,
            count=count
        )

        return {
            "mensaje": "Partidas obtenidas correctamente",
            "puuid": puuid,
            "cantidad": len(partidas),
            "partidas": partidas
        }

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OBTENER INFORMACIÓN COMPLETA DE UNA PARTIDA
# ============================================================

@app.get("/api/partida/{match_id}")
def obtener_partida(match_id: str):
    try:

        partida = obtener_partida_por_id(
            match_id
        )

        return {
            "mensaje": "Partida obtenida correctamente",
            "partida": partida
        }

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OBTENER ESTADÍSTICAS DEL JUGADOR EN UNA PARTIDA
# ============================================================

@app.get("/api/partida/{match_id}/jugador/{puuid}")
def obtener_estadisticas_jugador_partida(
    match_id: str,
    puuid: str
):
    try:

        partida = obtener_partida_por_id(
            match_id
        )

        estadisticas = extraer_estadisticas_jugador(
            partida,
            puuid
        )

        return {
            "mensaje": (
                "Estadísticas del jugador obtenidas correctamente"
            ),
            "match_id": match_id,
            "puuid": puuid,
            "estadisticas": estadisticas
        }

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OBTENER ESTADÍSTICAS DE PARTIDAS RECIENTES
# ============================================================

@app.get("/api/jugador/{puuid}/estadisticas")
def obtener_estadisticas(
    puuid: str,
    count: int = Query(
        100,
        ge=1,
        le=100,
        description="Cantidad de partidas a procesar"
    )
):
    try:

        estadisticas = (
            obtener_estadisticas_ultimas_partidas(
                puuid=puuid,
                count=count
            )
        )

        return {
            "mensaje": (
                "Estadísticas obtenidas correctamente"
            ),
            "puuid": puuid,
            "cantidad": len(estadisticas),
            "partidas": estadisticas
        }

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OBTENER PROMEDIOS GENERALES POR PUUID
# ============================================================

@app.get("/api/jugador/{puuid}/promedios")
def obtener_promedios_jugador(
    puuid: str,
    count: int = Query(
        100,
        ge=1,
        le=100,
        description="Cantidad de partidas a analizar"
    )
):
    """
    Endpoint auxiliar.

    Calcula promedios generales de todas las partidas
    independientemente del rol.

    No realiza todavía la comparación profesional.
    """

    try:

        partidas = (
            obtener_estadisticas_ultimas_partidas(
                puuid=puuid,
                count=count
            )
        )

        promedios = calcular_promedios(
            partidas
        )

        return {
            "mensaje": (
                "Promedios calculados correctamente"
            ),
            "puuid": puuid,
            "promedios": promedios
        }

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ANALIZAR JUGADOR POR PUUID CONTRA REFERENCIA PROFESIONAL
# ============================================================

@app.get("/api/jugador/{puuid}/analisis")
def analizar_rendimiento_por_puuid(
    puuid: str,
    count: int = Query(
        100,
        ge=1,
        le=100,
        description="Cantidad de partidas recientes a evaluar"
    )
):
    """
    Ejecuta la nueva lógica de análisis utilizando directamente
    el PUUID.

    Es útil para pruebas internas desde Swagger.
    """

    try:

        partidas = (
            obtener_estadisticas_ultimas_partidas(
                puuid=puuid,
                count=count
            )
        )

        if not partidas:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontraron partidas "
                    "para realizar el análisis."
                )
            )

        analisis = analizar_jugador_con_referencia(
            partidas=partidas,
            puuid=puuid
        )

        return {
            "mensaje": (
                "Análisis contra referencia profesional "
                "realizado correctamente"
            ),
            "analisis": analisis
        }

    except HTTPException:
        raise

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# NUEVO ENDPOINT PRINCIPAL DE ANÁLISIS
# ============================================================

@app.post("/api/analisis")
def analizar_jugador(
    solicitud: AnalisisJugadorRequest
):

    try:

        # ----------------------------------------------------
        # VALIDAR RIOT ID
        # ----------------------------------------------------

        game_name, tag_line = validar_riot_id(
            solicitud.riot_id
        )

        # ----------------------------------------------------
        # OBTENER CUENTA RIOT
        # ----------------------------------------------------

        cuenta = obtener_cuenta_por_riot_id(
            game_name,
            tag_line
        )

        puuid = cuenta.get(
            "puuid"
        )

        if not puuid:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No se pudo obtener el PUUID "
                    "del jugador."
                )
            )

        nombre = cuenta.get(
            "gameName",
            game_name
        )

        tag = cuenta.get(
            "tagLine",
            tag_line
        )


        rango = obtener_rango_jugador(
            puuid=puuid
        )

        # ----------------------------------------------------
        # OBTENER ÚLTIMAS 100 PARTIDAS
        # ----------------------------------------------------

        partidas = (
            obtener_estadisticas_ultimas_partidas(
                puuid=puuid,
                count=100
            )
        )

        if not partidas:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontraron partidas recientes "
                    "para este jugador."
                )
            )

        # ----------------------------------------------------
        # EJECUTAR ANÁLISIS COMPLETO
        # ----------------------------------------------------

        analisis = (
            analizar_jugador_con_referencia(
                partidas=partidas,
                puuid=puuid,
                nombre=nombre,
                tag=tag,
                rango=rango
            )
        )

        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        return {
            "mensaje": (
                "Análisis de rendimiento realizado "
                "correctamente"
            ),
            "riot_id": f"{nombre}#{tag}",
            "analisis": analisis
        }

    except HTTPException:
        raise

    except RiotRateLimitException as e:
        manejar_rate_limit(e)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )