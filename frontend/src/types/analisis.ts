export interface AnalisisRequest {
  riot_id: string;
}


// ============================================================
// DISTRIBUCIÓN DE ROLES
// ============================================================

export interface DistribucionRol {
  partidas: number;
  porcentaje: number;
}

export interface DistribucionRoles {
  TOP: DistribucionRol;
  JUNGLE: DistribucionRol;
  MID: DistribucionRol;
  ADC: DistribucionRol;
  SUPPORT: DistribucionRol;
}

export interface RangoJugador {
  clasificado: boolean;

  cola: string;

  tier: string | null;

  division: string | null;

  lp: number;

  victorias: number;

  derrotas: number;
}

// ============================================================
// JUGADOR
// ============================================================

export interface JugadorAnalizado {
  puuid: string;

  nombre: string;

  tag: string;

  riot_id: string | null;

  rango: RangoJugador | null;
}


// ============================================================
// MUESTRA
// ============================================================

export interface MuestraAnalisis {
  partidas_obtenidas: number;
  partidas_analizadas: number;
  rol_principal: string;
  distribucion_roles: DistribucionRoles;
}


// ============================================================
// REFERENCIA PROFESIONAL
// ============================================================

export interface MetricasReferencia {
  win_rate: number;
  kda: number;
  cs_por_minuto: number;
  oro_por_minuto: number;
  daño_por_minuto: number;
  vision_score: number;
}

export interface ReferenciaProfesional {
  fuente: string;
  dataset: string;
  temporada: number;
  tipo_referencia?: string;
  ligas?: string[];
  rol: string;
  partidas_referencia: number;
  metricas: MetricasReferencia;
}


// ============================================================
// ESTADÍSTICAS DEL JUGADOR
// ============================================================

export interface ResultadosJugador {
  victorias: number;
  derrotas: number;
  win_rate: number;
}

export interface CombateJugador {
  kills_promedio: number;
  muertes_promedio: number;
  asistencias_promedio: number;
  kda_promedio: number;
}

export interface FarmeoJugador {
  cs_promedio: number;
  cs_por_minuto_promedio: number;
}

export interface EconomiaJugador {
  oro_promedio: number;
  oro_por_minuto_promedio: number;
}

export interface DanoJugador {
  daño_promedio: number;
  daño_por_minuto_promedio: number;
}

export interface VisionJugador {
  vision_score_promedio: number;
}

export interface EstadisticasJugador {
  partidas_analizadas: number;
  resultados: ResultadosJugador;
  combate: CombateJugador;
  farmeo: FarmeoJugador;
  economia: EconomiaJugador;
  daño: DanoJugador;
  vision: VisionJugador;
}


// ============================================================
// CAMPEÓN INSIGNIA
// ============================================================

export interface CampeonInsignia {
  nombre: string | null;
  partidas: number;
  imagen_icono: string | null;
  imagen_splash: string | null;
  estadisticas: EstadisticasJugador | null;
}


// ============================================================
// FORMA RECIENTE
// ============================================================

export type ResultadoReciente =
  | "V"
  | "D";

export interface FormaReciente {
  resultados: ResultadoReciente[];
  victorias: number;
  derrotas: number;
  cantidad: number;
}


// ============================================================
// CAMPEÓN DE PARTIDA
// ============================================================

export interface CampeonPartida {
  id?: number | null;
  nombre: string;
  nivel: number;
  imagen_icono: string | null;
  imagen_splash: string | null;
}


// ============================================================
// COMBATE DE PARTIDA
// ============================================================

export interface CombatePartida {
  kills: number;
  muertes: number;
  asistencias: number;
  kda: number;
}


// ============================================================
// FARMEO
// ============================================================

export interface FarmeoPartida {
  cs: number;
  cs_por_minuto: number;
}


// ============================================================
// ECONOMÍA
// ============================================================

export interface EconomiaPartida {
  oro: number;
  oro_por_minuto: number;
}


// ============================================================
// DAÑO
// ============================================================

export interface DanoPartida {
  daño_campeones: number;
  daño_por_minuto: number;
}


// ============================================================
// VISIÓN
// ============================================================

export interface VisionPartida {
  vision_score: number;
}


// ============================================================
// RESULTADO DEL RIVAL
// ============================================================

export interface ResultadoRival {
  victoria: boolean;
}


// ============================================================
// RIVAL DEL MISMO ROL
// ============================================================

export interface RivalRol {
  puuid: string | null;
  nombre: string | null;
  tag: string | null;
  team_id: number | null;
  rol: string | null;

  campeon: CampeonPartida;

  combate: CombatePartida;

  resultado: ResultadoRival;
}


// ============================================================
// PARTIDAS RECIENTES
// ============================================================

export interface PartidaReciente {
  match_id: string | null;

  modo: string | null;

  queue_id: number | null;

  rol: string | null;

  duracion_segundos: number;

  duracion_minutos: number;

  victoria: boolean;

  campeon: CampeonPartida;

  combate: CombatePartida;

  farmeo: FarmeoPartida;

  economia: EconomiaPartida;

  daño: DanoPartida;

  vision: VisionPartida;

  rival_rol: RivalRol | null;
}


// ============================================================
// COMPARACIÓN PROFESIONAL
// ============================================================

export type EstadoMetrica =
  | "superior"
  | "inferior"
  | "similar";

export interface ComparacionMetrica {
  nombre: string;
  jugador: number;
  referencia: number;
  diferencia: number;
  diferencia_porcentual: number;
  porcentaje_referencia: number;
  estado: EstadoMetrica;
}

export interface Comparacion {
  win_rate: ComparacionMetrica;
  kda: ComparacionMetrica;
  cs_por_minuto: ComparacionMetrica;
  oro_por_minuto: ComparacionMetrica;
  daño_por_minuto: ComparacionMetrica;
  vision_score: ComparacionMetrica;
}


// ============================================================
// SCORE
// ============================================================

export interface Score {
  valor: number;
  maximo: number;
  clasificacion: string;
}


// ============================================================
// FORTALEZAS / DEBILIDADES
// ============================================================

export interface EvaluacionMetrica {
  metrica: string;
  nombre: string;
  jugador: number;
  referencia: number;
  diferencia_porcentual: number;
}


// ============================================================
// RECOMENDACIONES
// ============================================================

export interface Recomendacion {
  metrica: string;
  nombre: string;
  diferencia_porcentual: number;
  recomendacion: string;
}


// ============================================================
// ANÁLISIS COMPLETO
// ============================================================

export interface AnalisisCompleto {
  jugador: JugadorAnalizado;

  campeon_insignia: CampeonInsignia;

  muestra: MuestraAnalisis;

  forma_reciente: FormaReciente;

  partidas_recientes: PartidaReciente[];

  referencia_profesional: ReferenciaProfesional;

  estadisticas_jugador: EstadisticasJugador;

  comparacion: Comparacion;

  score: Score;

  fortalezas: EvaluacionMetrica[];

  debilidades: EvaluacionMetrica[];

  metricas_similares: EvaluacionMetrica[];

  recomendaciones: Recomendacion[];
}


// ============================================================
// RESPUESTA API
// ============================================================

export interface AnalisisResponse {
  mensaje: string;
  riot_id: string;
  analisis: AnalisisCompleto;
}