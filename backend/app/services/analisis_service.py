import json
import os
from collections import Counter

# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RUTA_REFERENCIA_PROFESIONAL = os.path.join(
    BASE_DIR,
    "data",
    "referencia_profesional.json"
)


# ============================================================
# EQUIVALENCIAS DE POSICIONES RIOT -> SISTEMA
# ============================================================

EQUIVALENCIAS_ROLES = {
    "TOP": "TOP",

    "JUNGLE": "JUNGLE",
    "JNG": "JUNGLE",

    "MIDDLE": "MID",
    "MID": "MID",

    "BOTTOM": "ADC",
    "BOT": "ADC",
    "ADC": "ADC",

    "UTILITY": "SUPPORT",
    "SUPPORT": "SUPPORT",
    "SUP": "SUPPORT"
}


# ============================================================
# NOMBRES DE MÉTRICAS
# ============================================================

NOMBRES_METRICAS = {
    "win_rate": "Win Rate",
    "kda": "KDA",
    "cs_por_minuto": "CS por minuto",
    "oro_por_minuto": "Oro por minuto",
    "daño_por_minuto": "Daño por minuto",
    "vision_score": "Puntuación de visión"
}


# ============================================================
# CARGAR REFERENCIA PROFESIONAL
# ============================================================

def cargar_referencia_profesional():
    """
    Carga las referencias profesionales generadas
    a partir del dataset de Oracle's Elixir.
    """

    if not os.path.exists(RUTA_REFERENCIA_PROFESIONAL):
        raise FileNotFoundError(
            "No se encontró el archivo referencia_profesional.json "
            f"en la ruta: {RUTA_REFERENCIA_PROFESIONAL}"
        )

    try:
        with open(
            RUTA_REFERENCIA_PROFESIONAL,
            "r",
            encoding="utf-8"
        ) as archivo:
            datos = json.load(archivo)

    except json.JSONDecodeError as error:
        raise Exception(
            "El archivo referencia_profesional.json "
            "no contiene un JSON válido."
        ) from error

    if "roles" not in datos:
        raise Exception(
            "El archivo referencia_profesional.json "
            "no contiene la propiedad 'roles'."
        )

    return datos


# ============================================================
# NORMALIZAR POSICIÓN
# ============================================================

def normalizar_rol(posicion):
    """
    Convierte la posición entregada por Riot Games
    al formato utilizado por el sistema.

    Ejemplos:
        MIDDLE  -> MID
        BOTTOM  -> ADC
        UTILITY -> SUPPORT
    """

    if not posicion:
        return None

    posicion = str(posicion).strip().upper()

    return EQUIVALENCIAS_ROLES.get(posicion)


# ============================================================
# FILTRAR PARTIDAS VÁLIDAS
# ============================================================

def obtener_partidas_validas(partidas):
    """
    Elimina registros con errores o formatos inválidos.
    """

    if isinstance(partidas, dict):
        partidas = list(partidas.values())

    if not isinstance(partidas, list):
        return []

    return [
        partida
        for partida in partidas
        if isinstance(partida, dict)
        and "error" not in partida
    ]


# ============================================================
# DISTRIBUCIÓN DE ROLES
# ============================================================

def obtener_distribucion_roles(partidas):
    """
    Cuenta cuántas partidas jugó el usuario
    en cada posición.
    """

    partidas_validas = obtener_partidas_validas(partidas)

    contador = Counter()

    for partida in partidas_validas:

        posicion = (
            partida
            .get("partida", {})
            .get("posicion")
        )

        rol = normalizar_rol(posicion)

        if rol:
            contador[rol] += 1

    total_con_rol = sum(contador.values())

    distribucion = {}

    for rol in [
        "TOP",
        "JUNGLE",
        "MID",
        "ADC",
        "SUPPORT"
    ]:

        cantidad = contador.get(rol, 0)

        porcentaje = (
            (cantidad / total_con_rol) * 100
            if total_con_rol > 0
            else 0
        )

        distribucion[rol] = {
            "partidas": cantidad,
            "porcentaje": round(porcentaje, 2)
        }

    return distribucion


# ============================================================
# DETERMINAR ROL PRINCIPAL
# ============================================================

def determinar_rol_principal(partidas):
    """
    Determina el rol predominante del jugador
    según sus partidas recientes.
    """

    partidas_validas = obtener_partidas_validas(partidas)

    contador = Counter()

    for partida in partidas_validas:

        posicion = (
            partida
            .get("partida", {})
            .get("posicion")
        )

        rol = normalizar_rol(posicion)

        if rol:
            contador[rol] += 1

    if not contador:
        raise Exception(
            "No fue posible determinar el rol principal "
            "del jugador con las partidas disponibles."
        )

    rol_principal, cantidad = contador.most_common(1)[0]

    return rol_principal


# ============================================================
# FILTRAR PARTIDAS POR ROL
# ============================================================

def filtrar_partidas_por_rol(partidas, rol):
    """
    Selecciona únicamente las partidas correspondientes
    al rol que será comparado contra la referencia profesional.
    """

    partidas_validas = obtener_partidas_validas(partidas)

    rol = normalizar_rol(rol) or str(rol).upper()

    resultado = []

    for partida in partidas_validas:

        posicion = (
            partida
            .get("partida", {})
            .get("posicion")
        )

        rol_partida = normalizar_rol(posicion)

        if rol_partida == rol:
            resultado.append(partida)

    return resultado


# ============================================================
# CALCULAR PROMEDIOS DEL JUGADOR
# ============================================================

def calcular_promedios(partidas):
    """
    Calcula las estadísticas promedio de las
    partidas proporcionadas.
    """

    partidas_validas = obtener_partidas_validas(partidas)

    if not partidas_validas:
        raise Exception(
            "No existen partidas válidas para realizar el análisis."
        )

    cantidad = len(partidas_validas)

    # --------------------------------------------------------
    # RESULTADOS
    # --------------------------------------------------------

    victorias = sum(
        1
        for partida in partidas_validas
        if partida.get(
            "resultado",
            {}
        ).get(
            "victoria",
            False
        )
    )

    derrotas = cantidad - victorias

    win_rate = (
        (victorias / cantidad) * 100
        if cantidad > 0
        else 0
    )

    # --------------------------------------------------------
    # COMBATE
    # --------------------------------------------------------

    kills_total = sum(
        float(
            partida.get(
                "combate",
                {}
            ).get(
                "kills",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    muertes_total = sum(
        float(
            partida.get(
                "combate",
                {}
            ).get(
                "muertes",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    asistencias_total = sum(
        float(
            partida.get(
                "combate",
                {}
            ).get(
                "asistencias",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    kda_total = sum(
        float(
            partida.get(
                "combate",
                {}
            ).get(
                "kda",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    # --------------------------------------------------------
    # FARMEO
    # --------------------------------------------------------

    cs_total = sum(
        float(
            partida.get(
                "farmeo",
                {}
            ).get(
                "cs",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    cs_por_minuto_total = sum(
        float(
            partida.get(
                "farmeo",
                {}
            ).get(
                "cs_por_minuto",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    # --------------------------------------------------------
    # ECONOMÍA
    # --------------------------------------------------------

    oro_total = sum(
        float(
            partida.get(
                "economia",
                {}
            ).get(
                "oro",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    oro_por_minuto_total = sum(
        float(
            partida.get(
                "economia",
                {}
            ).get(
                "oro_por_minuto",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    # --------------------------------------------------------
    # DAÑO
    # --------------------------------------------------------

    daño_total = sum(
        float(
            partida.get(
                "daño",
                {}
            ).get(
                "daño_campeones",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    daño_por_minuto_total = sum(
        float(
            partida.get(
                "daño",
                {}
            ).get(
                "daño_por_minuto",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    # --------------------------------------------------------
    # VISIÓN
    # --------------------------------------------------------

    vision_total = sum(
        float(
            partida.get(
                "vision",
                {}
            ).get(
                "vision_score",
                0
            ) or 0
        )
        for partida in partidas_validas
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    return {

        "partidas_analizadas": cantidad,

        "resultados": {
            "victorias": victorias,
            "derrotas": derrotas,
            "win_rate": round(
                win_rate,
                2
            )
        },

        "combate": {
            "kills_promedio": round(
                kills_total / cantidad,
                2
            ),
            "muertes_promedio": round(
                muertes_total / cantidad,
                2
            ),
            "asistencias_promedio": round(
                asistencias_total / cantidad,
                2
            ),
            "kda_promedio": round(
                kda_total / cantidad,
                2
            )
        },

        "farmeo": {
            "cs_promedio": round(
                cs_total / cantidad,
                2
            ),
            "cs_por_minuto_promedio": round(
                cs_por_minuto_total / cantidad,
                2
            )
        },

        "economia": {
            "oro_promedio": round(
                oro_total / cantidad,
                2
            ),
            "oro_por_minuto_promedio": round(
                oro_por_minuto_total / cantidad,
                2
            )
        },

        "daño": {
            "daño_promedio": round(
                daño_total / cantidad,
                2
            ),
            "daño_por_minuto_promedio": round(
                daño_por_minuto_total / cantidad,
                2
            )
        },

        "vision": {
            "vision_score_promedio": round(
                vision_total / cantidad,
                2
            )
        }
    }


# ============================================================
# OBTENER REFERENCIA DE UN ROL
# ============================================================

def obtener_referencia_por_rol(rol):
    """
    Obtiene los valores profesionales correspondientes
    al rol principal del jugador.
    """

    datos = cargar_referencia_profesional()

    roles = datos.get(
        "roles",
        {}
    )

    rol = normalizar_rol(rol) or str(rol).upper()

    if rol not in roles:
        raise Exception(
            f"No existe una referencia profesional para el rol {rol}."
        )

    return roles[rol]


# ============================================================
# PORCENTAJE RESPECTO A REFERENCIA
# ============================================================

def calcular_porcentaje_comparacion(
    valor_jugador,
    valor_referencia
):
    """
    Calcula qué porcentaje representa el valor del jugador
    con respecto al valor profesional.
    """

    valor_jugador = float(
        valor_jugador or 0
    )

    valor_referencia = float(
        valor_referencia or 0
    )

    if valor_referencia <= 0:
        return 0

    porcentaje = (
        valor_jugador
        / valor_referencia
    ) * 100

    return round(
        porcentaje,
        2
    )


# ============================================================
# DIFERENCIA PORCENTUAL
# ============================================================

def calcular_diferencia_porcentual(
    valor_jugador,
    valor_referencia
):
    """
    Calcula cuánto se encuentra el jugador por encima
    o por debajo de la referencia profesional.
    """

    valor_jugador = float(
        valor_jugador or 0
    )

    valor_referencia = float(
        valor_referencia or 0
    )

    if valor_referencia <= 0:
        return 0

    diferencia = (
        (
            valor_jugador
            - valor_referencia
        )
        / valor_referencia
    ) * 100

    return round(
        diferencia,
        2
    )


# ============================================================
# EXTRAER MÉTRICAS COMPARABLES
# ============================================================

def extraer_metricas_comparables(metricas_jugador):
    """
    Convierte la estructura completa de estadísticas
    en las seis métricas usadas en la comparación.
    """

    return {

        "win_rate":
            metricas_jugador[
                "resultados"
            ][
                "win_rate"
            ],

        "kda":
            metricas_jugador[
                "combate"
            ][
                "kda_promedio"
            ],

        "cs_por_minuto":
            metricas_jugador[
                "farmeo"
            ][
                "cs_por_minuto_promedio"
            ],

        "oro_por_minuto":
            metricas_jugador[
                "economia"
            ][
                "oro_por_minuto_promedio"
            ],

        "daño_por_minuto":
            metricas_jugador[
                "daño"
            ][
                "daño_por_minuto_promedio"
            ],

        "vision_score":
            metricas_jugador[
                "vision"
            ][
                "vision_score_promedio"
            ]
    }


# ============================================================
# COMPARAR CONTRA REFERENCIA PROFESIONAL
# ============================================================

def comparar_con_referencia(
    metricas_jugador,
    referencia_profesional
):
    """
    Compara las seis métricas principales del jugador
    contra el estándar profesional correspondiente a su rol.
    """

    jugador = extraer_metricas_comparables(
        metricas_jugador
    )

    resultados = {}

    for metrica, valor_jugador in jugador.items():

        valor_referencia = float(
            referencia_profesional.get(
                metrica,
                0
            ) or 0
        )

        diferencia = (
            float(valor_jugador)
            - valor_referencia
        )

        diferencia_porcentual = (
            calcular_diferencia_porcentual(
                valor_jugador,
                valor_referencia
            )
        )

        porcentaje_referencia = (
            calcular_porcentaje_comparacion(
                valor_jugador,
                valor_referencia
            )
        )

        if diferencia_porcentual >= 5:
            estado = "superior"

        elif diferencia_porcentual <= -5:
            estado = "inferior"

        else:
            estado = "similar"

        resultados[metrica] = {

            "nombre":
                NOMBRES_METRICAS.get(
                    metrica,
                    metrica
                ),

            "jugador":
                round(
                    float(valor_jugador),
                    2
                ),

            "referencia":
                round(
                    valor_referencia,
                    2
                ),

            "diferencia":
                round(
                    diferencia,
                    2
                ),

            "diferencia_porcentual":
                diferencia_porcentual,

            "porcentaje_referencia":
                porcentaje_referencia,

            "estado":
                estado
        }

    return resultados


# ============================================================
# CALCULAR SCORE GENERAL
# ============================================================

def calcular_score(comparacion):
    """
    Genera un indicador general de rendimiento
    entre 0 y 100.

    Alcanzar o superar el estándar profesional
    equivale a 100 puntos en una métrica.
    """

    if not comparacion:
        return 0

    puntuaciones = []

    for metrica in NOMBRES_METRICAS.keys():

        if metrica not in comparacion:
            continue

        porcentaje = float(
            comparacion[
                metrica
            ].get(
                "porcentaje_referencia",
                0
            ) or 0
        )

        puntuacion = max(
            0,
            min(
                porcentaje,
                100
            )
        )

        puntuaciones.append(
            puntuacion
        )

    if not puntuaciones:
        return 0

    score = (
        sum(puntuaciones)
        / len(puntuaciones)
    )

    return round(
        score,
        2
    )


# ============================================================
# CLASIFICACIÓN DEL SCORE
# ============================================================

def clasificar_score(score):
    """
    Devuelve una clasificación descriptiva
    para el score general.
    """

    score = float(
        score or 0
    )

    if score >= 90:
        return "Muy cercano al nivel profesional"

    if score >= 75:
        return "Rendimiento alto"

    if score >= 60:
        return "Rendimiento intermedio"

    if score >= 40:
        return "Rendimiento en desarrollo"

    return "Rendimiento inicial"


# ============================================================
# FORTALEZAS, DEBILIDADES Y MÉTRICAS SIMILARES
# ============================================================

def detectar_fortalezas_debilidades(comparacion):
    """
    Clasifica las métricas según su diferencia
    con la referencia profesional.

    >= +5%  -> fortaleza
    <= -5%  -> debilidad
    entre ambos -> similar
    """

    fortalezas = []
    debilidades = []
    similares = []

    for metrica, datos in comparacion.items():

        diferencia = float(
            datos.get(
                "diferencia_porcentual",
                0
            ) or 0
        )

        elemento = {
            "metrica": metrica,
            "nombre": NOMBRES_METRICAS.get(
                metrica,
                metrica
            ),
            "jugador": datos.get(
                "jugador"
            ),
            "referencia": datos.get(
                "referencia"
            ),
            "diferencia_porcentual": diferencia
        }

        if diferencia >= 5:

            fortalezas.append(
                elemento
            )

        elif diferencia <= -5:

            debilidades.append(
                elemento
            )

        else:

            similares.append(
                elemento
            )

    fortalezas.sort(
        key=lambda item:
            item["diferencia_porcentual"],
        reverse=True
    )

    debilidades.sort(
        key=lambda item:
            item["diferencia_porcentual"]
    )

    return {
        "fortalezas": fortalezas,
        "debilidades": debilidades,
        "similares": similares
    }


# ============================================================
# GENERAR RECOMENDACIONES
# ============================================================

def generar_recomendaciones(debilidades):
    """
    Genera recomendaciones según las métricas
    que se encuentren por debajo de la referencia.
    """

    recomendaciones = {

        "win_rate": (
            "Trabaja la toma de decisiones durante el juego medio "
            "y tardío, priorizando objetivos como torres, dragones, "
            "Barón Nashor y peleas con ventaja numérica."
        ),

        "kda": (
            "Mejora el posicionamiento y reduce las muertes evitables. "
            "Evalúa mejor cuándo iniciar, continuar o abandonar una pelea."
        ),

        "cs_por_minuto": (
            "Mejora la eficiencia de farmeo durante la fase de líneas "
            "y el juego medio, evitando perder oleadas y aprovechando "
            "campamentos disponibles cuando sea apropiado para tu rol."
        ),

        "oro_por_minuto": (
            "Optimiza la generación de oro mediante farmeo constante, "
            "participación en objetivos, placas, torres y eliminaciones "
            "sin sacrificar recursos innecesariamente."
        ),

        "daño_por_minuto": (
            "Mejora tu participación efectiva en intercambios y peleas "
            "grupales. Revisa posicionamiento, selección de objetivos "
            "y uso de habilidades durante los combates."
        ),

        "vision_score": (
            "Incrementa el control de visión mediante colocación y "
            "eliminación de wards, especialmente alrededor de objetivos "
            "neutrales y zonas importantes del mapa."
        )
    }

    resultado = []

    for debilidad in debilidades:

        metrica = debilidad.get(
            "metrica"
        )

        recomendacion = recomendaciones.get(
            metrica
        )

        if not recomendacion:
            continue

        resultado.append({
            "metrica": metrica,
            "nombre": NOMBRES_METRICAS.get(
                metrica,
                metrica
            ),
            "diferencia_porcentual":
                debilidad.get(
                    "diferencia_porcentual"
                ),
            "recomendacion":
                recomendacion
        })

    return resultado


# ============================================================
# ANÁLISIS COMPLETO DEL JUGADOR
# ============================================================

def analizar_jugador_con_referencia(
    partidas,
    puuid=None,
    nombre=None,
    tag=None,
    rango=None
):
    """
    Función principal del análisis individual del jugador.

    Flujo:

    1. Valida partidas.
    2. Determina el rol principal.
    3. Filtra partidas de ese rol.
    4. Calcula estadísticas.
    5. Determina campeón insignia.
    6. Prepara partidas recientes para frontend.
    7. Carga referencia profesional.
    8. Compara métricas.
    9. Calcula score.
    10. Detecta fortalezas y debilidades.
    11. Genera recomendaciones.
    """

    # ========================================================
    # PARTIDAS VÁLIDAS
    # ========================================================

    partidas_validas = obtener_partidas_validas(
        partidas
    )

    if not partidas_validas:
        raise Exception(
            "No existen partidas válidas para analizar al jugador."
        )


    # ========================================================
    # DISTRIBUCIÓN DE ROLES
    # ========================================================

    distribucion_roles = obtener_distribucion_roles(
        partidas_validas
    )


    # ========================================================
    # ROL PRINCIPAL
    # ========================================================

    rol_principal = determinar_rol_principal(
        partidas_validas
    )


    # ========================================================
    # PARTIDAS DEL ROL PRINCIPAL
    # ========================================================

    partidas_rol = filtrar_partidas_por_rol(
        partidas_validas,
        rol_principal
    )

    if not partidas_rol:
        raise Exception(
            f"No existen partidas válidas para el rol {rol_principal}."
        )


    # ========================================================
    # ESTADÍSTICAS DEL JUGADOR
    # ========================================================

    estadisticas = calcular_promedios(
        partidas_rol
    )


    # ========================================================
    # CAMPEÓN INSIGNIA
    # ========================================================

    contador_campeones = Counter()

    for partida in partidas_rol:

        campeon = (
            partida
            .get(
                "campeon",
                {}
            )
            .get(
                "nombre"
            )
        )

        if campeon:
            contador_campeones[campeon] += 1


    campeon_insignia = None
    partidas_campeon_insignia = 0


    if contador_campeones:

        campeon_insignia, partidas_campeon_insignia = (
            contador_campeones.most_common(1)[0]
        )


    # ========================================================
    # ESTADÍSTICAS DEL CAMPEÓN INSIGNIA
    # ========================================================

    partidas_insignia = []

    if campeon_insignia:

        for partida in partidas_rol:

            nombre_campeon = (
                partida
                .get(
                    "campeon",
                    {}
                )
                .get(
                    "nombre"
                )
            )

            if nombre_campeon == campeon_insignia:
                partidas_insignia.append(
                    partida
                )


    if partidas_insignia:

        estadisticas_campeon_insignia = (
            calcular_promedios(
                partidas_insignia
            )
        )

    else:

        estadisticas_campeon_insignia = None


    # ========================================================
    # PARTIDAS RECIENTES PARA EL FRONTEND
    # ========================================================

    partidas_recientes = []


    for partida in partidas_validas:

        # ----------------------------------------------------
        # BLOQUES PRINCIPALES
        # ----------------------------------------------------

        datos_partida = partida.get(
            "partida",
            {}
        )

        resultado = partida.get(
            "resultado",
            {}
        )

        campeon = partida.get(
            "campeon",
            {}
        )

        combate = partida.get(
            "combate",
            {}
        )

        farmeo = partida.get(
            "farmeo",
            {}
        )

        economia = partida.get(
            "economia",
            {}
        )

        daño = partida.get(
            "daño",
            {}
        )

        vision = partida.get(
            "vision",
            {}
        )

        rival_rol = partida.get(
            "rival_rol",
            {}
        )

        equipos = partida.get(
            "equipos",
            {
                "aliados": [],
                "rivales": []
            }
        )


        # ----------------------------------------------------
        # CAMPEÓN DEL JUGADOR
        # ----------------------------------------------------

        nombre_campeon = campeon.get(
            "nombre",
            "Desconocido"
        )


        # ----------------------------------------------------
        # ROL NORMALIZADO DEL JUGADOR
        # ----------------------------------------------------

        rol_partida = normalizar_rol(
            datos_partida.get(
                "posicion"
            )
        )


        # ----------------------------------------------------
        # RIVAL DEL MISMO ROL
        # ----------------------------------------------------

        rival_frontend = None


        if isinstance(
            rival_rol,
            dict
        ):

            rival_campeon = rival_rol.get(
                "campeon",
                {}
            )

            rival_combate = rival_rol.get(
                "combate",
                {}
            )

            rival_resultado = rival_rol.get(
                "resultado",
                {}
            )

            nombre_campeon_rival = (
                rival_campeon.get(
                    "nombre"
                )
            )


            rival_frontend = {

                "puuid":
                    rival_rol.get(
                        "puuid"
                    ),

                "nombre":
                    rival_rol.get(
                        "nombre"
                    ),

                "tag":
                    rival_rol.get(
                        "tag"
                    ),

                "team_id":
                    rival_rol.get(
                        "team_id"
                    ),

                "rol":
                    normalizar_rol(
                        rival_rol.get(
                            "posicion"
                        )
                    ),

                "campeon": {

                    "id":
                        rival_campeon.get(
                            "id"
                        ),

                    "nombre":
                        nombre_campeon_rival,

                    "nivel":
                        rival_campeon.get(
                            "nivel",
                            0
                        ),

                    "imagen_icono":
                        (
                            "https://ddragon.leagueoflegends.com/"
                            f"cdn/14.24.1/img/champion/{nombre_campeon_rival}.png"
                            if nombre_campeon_rival
                            else None
                        ),

                    "imagen_splash":
                        (
                            "https://ddragon.leagueoflegends.com/"
                            f"cdn/img/champion/splash/{nombre_campeon_rival}_0.jpg"
                            if nombre_campeon_rival
                            else None
                        )
                },

                "combate": {

                    "kills":
                        rival_combate.get(
                            "kills",
                            0
                        ),

                    "muertes":
                        rival_combate.get(
                            "muertes",
                            0
                        ),

                    "asistencias":
                        rival_combate.get(
                            "asistencias",
                            0
                        ),

                    "kda":
                        rival_combate.get(
                            "kda",
                            0
                        )
                },

                "resultado": {

                    "victoria":
                        rival_resultado.get(
                            "victoria",
                            False
                        )
                }
            }


        # ----------------------------------------------------
        # RESPUESTA DE LA PARTIDA RECIENTE
        # ----------------------------------------------------

        partidas_recientes.append({

            "match_id":
                datos_partida.get(
                    "match_id"
                ),

            "modo":
                datos_partida.get(
                    "modo"
                ),

            "queue_id":
                datos_partida.get(
                    "queue_id"
                ),

            "rol":
                rol_partida,

            "duracion_segundos":
                datos_partida.get(
                    "duracion_segundos",
                    0
                ),

            "duracion_minutos":
                datos_partida.get(
                    "duracion_minutos",
                    0
                ),

            "victoria":
                resultado.get(
                    "victoria",
                    False
                ),

            "campeon": {

                "id":
                    campeon.get(
                        "id"
                    ),

                "nombre":
                    nombre_campeon,

                "nivel":
                    campeon.get(
                        "nivel",
                        0
                    ),

                "imagen_icono":
                    (
                        "https://ddragon.leagueoflegends.com/"
                        f"cdn/14.24.1/img/champion/{nombre_campeon}.png"
                    ),

                "imagen_splash":
                    (
                        "https://ddragon.leagueoflegends.com/"
                        f"cdn/img/champion/splash/{nombre_campeon}_0.jpg"
                    )
            },

            "combate": {

                "kills":
                    combate.get(
                        "kills",
                        0
                    ),

                "muertes":
                    combate.get(
                        "muertes",
                        0
                    ),

                "asistencias":
                    combate.get(
                        "asistencias",
                        0
                    ),

                "kda":
                    combate.get(
                        "kda",
                        0
                    )
            },

            "farmeo": {

                "cs":
                    farmeo.get(
                        "cs",
                        0
                    ),

                "cs_por_minuto":
                    farmeo.get(
                        "cs_por_minuto",
                        0
                    )
            },

            "economia": {

                "oro":
                    economia.get(
                        "oro",
                        0
                    ),

                "oro_por_minuto":
                    economia.get(
                        "oro_por_minuto",
                        0
                    )
            },

            "daño": {

                "daño_campeones":
                    daño.get(
                        "daño_campeones",
                        0
                    ),

                "daño_por_minuto":
                    daño.get(
                        "daño_por_minuto",
                        0
                    )
            },

            "vision": {

                "vision_score":
                    vision.get(
                        "vision_score",
                        0
                    )
            },

            "rival_rol":
                rival_frontend,
                
            "equipos":
                equipos
        })


    # ========================================================
    # FORMA RECIENTE
    # ========================================================

    partidas_forma_reciente = partidas_recientes[:10]
    
    forma_reciente = []

    for partida in partidas_recientes[:10]:

        forma_reciente.append(
            "V"
            if partida["victoria"]
            else "D"
        )


    # ========================================================
    # VICTORIAS Y DERROTAS RECIENTES
    # ========================================================

    victorias_recientes = sum(
        1
        for partida in partidas_recientes
        if partida["victoria"]
    )

    derrotas_recientes = (
        len(partidas_recientes)
        - victorias_recientes
    )


    # ========================================================
    # REFERENCIA PROFESIONAL
    # ========================================================

    datos_referencia = cargar_referencia_profesional()

    referencia_rol = obtener_referencia_por_rol(
        rol_principal
    )


    # ========================================================
    # COMPARACIÓN
    # ========================================================

    comparacion = comparar_con_referencia(
        estadisticas,
        referencia_rol
    )


    # ========================================================
    # SCORE
    # ========================================================

    score = calcular_score(
        comparacion
    )

    clasificacion = clasificar_score(
        score
    )


    # ========================================================
    # FORTALEZAS / DEBILIDADES
    # ========================================================

    evaluacion = detectar_fortalezas_debilidades(
        comparacion
    )


    # ========================================================
    # RECOMENDACIONES
    # ========================================================

    recomendaciones = generar_recomendaciones(
        evaluacion[
            "debilidades"
        ]
    )


    # ========================================================
    # RESPUESTA FINAL
    # ========================================================

    return {

        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        "jugador": {

            "puuid":
                puuid,

            "nombre":
                nombre,

            "tag":
                tag,

            "riot_id":
                (
                    f"{nombre}#{tag}"
                    if nombre and tag
                    else None
                ),
            "rango":
               rango
        },


        # ----------------------------------------------------
        # CAMPEÓN INSIGNIA
        # ----------------------------------------------------

        "campeon_insignia": {

            "nombre":
                campeon_insignia,

            "partidas":
                partidas_campeon_insignia,

            "imagen_icono":
                (
                    "https://ddragon.leagueoflegends.com/"
                    f"cdn/14.24.1/img/champion/{campeon_insignia}.png"
                    if campeon_insignia
                    else None
                ),

            "imagen_splash":
                (
                    "https://ddragon.leagueoflegends.com/"
                    f"cdn/img/champion/splash/{campeon_insignia}_0.jpg"
                    if campeon_insignia
                    else None
                ),

            "estadisticas":
                estadisticas_campeon_insignia
        },


        # ----------------------------------------------------
        # MUESTRA
        # ----------------------------------------------------

        "muestra": {

            "partidas_obtenidas":
                len(partidas_validas),

            "partidas_analizadas":
                len(partidas_rol),

            "rol_principal":
                rol_principal,

            "distribucion_roles":
                distribucion_roles
        },


        # ----------------------------------------------------
        # FORMA RECIENTE
        # ----------------------------------------------------

        "forma_reciente": {

            "resultados":
                forma_reciente,

            "victorias":
                victorias_recientes,

            "derrotas":
                derrotas_recientes,

            "cantidad":
                len(partidas_forma_reciente)
        },


        # ----------------------------------------------------
        # PARTIDAS RECIENTES
        # ----------------------------------------------------

        "partidas_recientes":
            partidas_recientes,


        # ----------------------------------------------------
        # REFERENCIA PROFESIONAL
        # ----------------------------------------------------

        "referencia_profesional": {

            "fuente":
                datos_referencia.get(
                    "fuente"
                ),

            "dataset":
                datos_referencia.get(
                    "dataset"
                ),

            "temporada":
                datos_referencia.get(
                    "temporada"
                ),

            "tipo_referencia":
                datos_referencia.get(
                    "tipo_referencia"
                ),

            "ligas":
                datos_referencia.get(
                    "ligas",
                    []
                ),

            "rol":
                rol_principal,

            "partidas_referencia":
                referencia_rol.get(
                    "partidas"
                ),

            "metricas": {

                "win_rate":
                    referencia_rol.get(
                        "win_rate"
                    ),

                "kda":
                    referencia_rol.get(
                        "kda"
                    ),

                "cs_por_minuto":
                    referencia_rol.get(
                        "cs_por_minuto"
                    ),

                "oro_por_minuto":
                    referencia_rol.get(
                        "oro_por_minuto"
                    ),

                "daño_por_minuto":
                    referencia_rol.get(
                        "daño_por_minuto"
                    ),

                "vision_score":
                    referencia_rol.get(
                        "vision_score"
                    )
            }
        },


        # ----------------------------------------------------
        # ESTADÍSTICAS DEL JUGADOR
        # ----------------------------------------------------

        "estadisticas_jugador":
            estadisticas,


        # ----------------------------------------------------
        # COMPARACIÓN
        # ----------------------------------------------------

        "comparacion":
            comparacion,


        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        "score": {

            "valor":
                score,

            "maximo":
                100,

            "clasificacion":
                clasificacion
        },


        # ----------------------------------------------------
        # FORTALEZAS
        # ----------------------------------------------------

        "fortalezas":
            evaluacion[
                "fortalezas"
            ],


        # ----------------------------------------------------
        # DEBILIDADES
        # ----------------------------------------------------

        "debilidades":
            evaluacion[
                "debilidades"
            ],


        # ----------------------------------------------------
        # MÉTRICAS SIMILARES
        # ----------------------------------------------------

        "metricas_similares":
            evaluacion[
                "similares"
            ],


        # ----------------------------------------------------
        # RECOMENDACIONES
        # ----------------------------------------------------

        "recomendaciones":
            recomendaciones
    }


# ============================================================
# COMPATIBILIDAD TEMPORAL CON LA LÓGICA ANTERIOR
# ============================================================

def comparar_jugadores(jugadores):
    """
    Función conservada temporalmente para evitar romper
    el endpoint /api/comparacion existente en main.py.

    La nueva lógica principal del proyecto utiliza:
        analizar_jugador_con_referencia()

    Esta función podrá eliminarse cuando eliminemos
    definitivamente /api/comparacion de main.py.
    """

    resultados = []

    for jugador in jugadores:

        partidas = jugador.get(
            "partidas",
            []
        )

        partidas_validas = obtener_partidas_validas(
            partidas
        )

        if not partidas_validas:
            continue

        analisis = calcular_promedios(
            partidas_validas
        )

        resultados.append({

            "puuid":
                jugador.get(
                    "puuid"
                ),

            "nombre":
                jugador.get(
                    "nombre"
                ),

            "tag":
                jugador.get(
                    "tag"
                ),

            "analisis":
                analisis
        })

    if not resultados:
        raise Exception(
            "No existen jugadores con partidas válidas para comparar."
        )

    return resultados