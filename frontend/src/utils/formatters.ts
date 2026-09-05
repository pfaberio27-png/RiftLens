import type {
  ComparacionMetrica,
} from "../types/analisis";


export const traducirTier = (
  tier: string | null
) => {

  if (!tier) {
    return "Sin rango";
  }

  const tiers: Record<string, string> = {
    IRON: "Hierro",
    BRONZE: "Bronce",
    SILVER: "Plata",
    GOLD: "Oro",
    PLATINUM: "Platino",
    EMERALD: "Esmeralda",
    DIAMOND: "Diamante",
    MASTER: "Maestro",
    GRANDMASTER: "Gran Maestro",
    CHALLENGER: "Retador",
  };

  return tiers[tier] ?? tier;
};


export const formatearRol = (
  rol: string | null
) => {

  if (!rol) {
    return "Sin rol";
  }

  const roles: Record<string, string> = {
    TOP: "Top",
    JUNGLE: "Jungla",
    MID: "Medio",
    ADC: "ADC",
    SUPPORT: "Soporte",
  };

  return roles[rol] ?? rol;
};


export const formatearDiferencia = (
  valor: number
) => {

  if (valor > 0) {
    return `+${valor}%`;
  }

  return `${valor}%`;
};


export const obtenerClaseEstado = (
  estado: ComparacionMetrica["estado"]
) => {

  switch (estado) {

    case "superior":
      return "metrica-superior";

    case "inferior":
      return "metrica-inferior";

    default:
      return "metrica-similar";
  }
};