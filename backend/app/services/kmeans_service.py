from collections import Counter

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


VARIABLES_KMEANS = [
    "kda",
    "cs_por_minuto",
    "oro_por_minuto",
    "daño_por_minuto",
    "vision_score",
]


def _obtener_numero(valor, default=0.0):
    try:
        return float(valor or 0)
    except (TypeError, ValueError):
        return default


def extraer_vector_partida(partida):
    """
    Convierte una partida en un vector numérico
    para ser utilizado por K-Means.

    Variables:
        - KDA
        - CS por minuto
        - Oro por minuto
        - Daño por minuto
        - Vision Score
    """

    combate = partida.get("combate", {})
    farmeo = partida.get("farmeo", {})
    economia = partida.get("economia", {})
    dano = partida.get("daño", {})
    vision = partida.get("vision", {})

    return [
        _obtener_numero(
            combate.get("kda")
        ),
        _obtener_numero(
            farmeo.get("cs_por_minuto")
        ),
        _obtener_numero(
            economia.get("oro_por_minuto")
        ),
        _obtener_numero(
            dano.get("daño_por_minuto")
        ),
        _obtener_numero(
            vision.get("vision_score")
        ),
    ]


def preparar_datos_kmeans(partidas):
    """
    Extrae la matriz de características de las partidas.
    """

    matriz = []
    indices_validos = []

    for indice, partida in enumerate(partidas):

        if not isinstance(partida, dict):
            continue

        if "error" in partida:
            continue

        vector = extraer_vector_partida(
            partida
        )

        if not all(
            np.isfinite(valor)
            for valor in vector
        ):
            continue

        matriz.append(
            vector
        )

        indices_validos.append(
            indice
        )

    if not matriz:
        return (
            np.empty((0, len(VARIABLES_KMEANS))),
            []
        )

    return (
        np.array(
            matriz,
            dtype=float
        ),
        indices_validos
    )


def evaluar_numero_clusters(
    datos_normalizados,
    max_clusters=6
):
    """
    Evalúa diferentes valores de K mediante
    Silhouette Score.

    Retorna:
        - mejor número de clusters
        - resultados de evaluación
    """

    cantidad = len(
        datos_normalizados
    )

    # Se necesitan suficientes observaciones
    # para evaluar varios clusters.
    if cantidad < 3:
        return None, []

    limite_superior = min(
        max_clusters,
        cantidad - 1
    )

    resultados = []

    mejor_k = None
    mejor_score = -1

    for k in range(
        2,
        limite_superior + 1
    ):

        modelo = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        etiquetas = modelo.fit_predict(
            datos_normalizados
        )

        # Silhouette requiere por lo menos
        # dos clusters realmente presentes.
        if len(set(etiquetas)) < 2:
            continue

        score = silhouette_score(
            datos_normalizados,
            etiquetas
        )

        resultados.append({
            "k": k,
            "silhouette_score": round(
                float(score),
                4
            ),
            "inercia": round(
                float(modelo.inertia_),
                4
            )
        })

        if score > mejor_score:

            mejor_score = score
            mejor_k = k

    return (
        mejor_k,
        resultados
    )


def _calcular_promedio_cluster(
    datos_originales,
    indices
):
    """
    Calcula el centro interpretable de un cluster
    utilizando las unidades originales.
    """

    subconjunto = datos_originales[
        indices
    ]

    promedio = np.mean(
        subconjunto,
        axis=0
    )

    return {
        "kda":
            round(
                float(promedio[0]),
                2
            ),

        "cs_por_minuto":
            round(
                float(promedio[1]),
                2
            ),

        "oro_por_minuto":
            round(
                float(promedio[2]),
                2
            ),

        "daño_por_minuto":
            round(
                float(promedio[3]),
                2
            ),

        "vision_score":
            round(
                float(promedio[4]),
                2
            )
    }


def analizar_patrones_kmeans(
    partidas,
    max_clusters=6
):
    """
    Aplica K-Means sobre las partidas del rol principal.

    Flujo:
        1. Extrae métricas.
        2. Normaliza mediante StandardScaler.
        3. Evalúa K entre 2 y max_clusters.
        4. Selecciona K mediante Silhouette Score.
        5. Ejecuta K-Means.
        6. Calcula centroides interpretables.
        7. Retorna los patrones encontrados.
    """

    datos, indices_validos = (
        preparar_datos_kmeans(
            partidas
        )
    )

    cantidad = len(
        datos
    )

    if cantidad < 3:

        return {
            "disponible": False,
            "motivo": (
                "Se necesitan al menos 3 partidas "
                "válidas para aplicar K-Means."
            ),
            "algoritmo": "K-Means",
            "partidas_utilizadas": cantidad,
            "variables": VARIABLES_KMEANS,
            "numero_clusters": 0,
            "evaluacion_clusters": [],
            "clusters": []
        }

    # ========================================================
    # NORMALIZACIÓN
    # ========================================================

    scaler = StandardScaler()

    datos_normalizados = (
        scaler.fit_transform(
            datos
        )
    )

    # ========================================================
    # SELECCIÓN DE K
    # ========================================================

    mejor_k, evaluacion = (
        evaluar_numero_clusters(
            datos_normalizados,
            max_clusters=max_clusters
        )
    )

    if mejor_k is None:

        return {
            "disponible": False,
            "motivo": (
                "No fue posible determinar "
                "un número válido de clusters."
            ),
            "algoritmo": "K-Means",
            "partidas_utilizadas": cantidad,
            "variables": VARIABLES_KMEANS,
            "numero_clusters": 0,
            "evaluacion_clusters": evaluacion,
            "clusters": []
        }

    # ========================================================
    # MODELO FINAL
    # ========================================================

    modelo = KMeans(
        n_clusters=mejor_k,
        random_state=42,
        n_init=10
    )

    etiquetas = modelo.fit_predict(
        datos_normalizados
    )

    # ========================================================
    # CLUSTERS
    # ========================================================

    clusters = []

    contador = Counter(
        etiquetas.tolist()
    )

    for cluster_id in sorted(
        contador.keys()
    ):

        indices_cluster = np.where(
            etiquetas == cluster_id
        )[0]

        cantidad_cluster = len(
            indices_cluster
        )

        porcentaje = (
            cantidad_cluster
            / cantidad
        ) * 100

        promedios = (
            _calcular_promedio_cluster(
                datos,
                indices_cluster
            )
        )

        clusters.append({

            "cluster":
                int(cluster_id),

            "cantidad_partidas":
                cantidad_cluster,

            "porcentaje":
                round(
                    porcentaje,
                    2
                ),

            "metricas_promedio":
                promedios
        })

    # ========================================================
    # ASIGNACIÓN PARTIDA -> CLUSTER
    # ========================================================

    asignaciones = []

    for posicion, etiqueta in enumerate(
        etiquetas
    ):

        indice_original = (
            indices_validos[
                posicion
            ]
        )

        partida = partidas[
            indice_original
        ]

        datos_partida = partida.get(
            "partida",
            {}
        )

        campeon = partida.get(
            "campeon",
            {}
        )

        asignaciones.append({

            "indice_partida":
                indice_original,

            "match_id":
                datos_partida.get(
                    "match_id"
                ),

            "campeon":
                campeon.get(
                    "nombre"
                ),

            "cluster":
                int(etiqueta)
        })

    # ========================================================
    # RESULTADO
    # ========================================================

    mejor_silhouette = None

    for resultado in evaluacion:

        if resultado["k"] == mejor_k:

            mejor_silhouette = (
                resultado[
                    "silhouette_score"
                ]
            )

            break

    return {

        "disponible":
            True,

        "algoritmo":
            "K-Means",

        "normalizacion":
            "StandardScaler",

        "criterio_seleccion_k":
            "Silhouette Score",

        "partidas_utilizadas":
            cantidad,

        "variables":
            VARIABLES_KMEANS,

        "numero_clusters":
            mejor_k,

        "silhouette_score":
            mejor_silhouette,

        "evaluacion_clusters":
            evaluacion,

        "clusters":
            clusters,

        "asignaciones":
            asignaciones
    }