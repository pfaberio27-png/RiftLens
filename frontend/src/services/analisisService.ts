import type {
  AnalisisRequest,
  AnalisisResponse,
} from "../types/analisis";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

export async function analizarJugador(
  riotId: string,
  region: string
): Promise<AnalisisResponse> {

  const body: AnalisisRequest = {
    riot_id: riotId,
    region: region,
  };

  let response: Response;

  try {

    response = await fetch(
      `${API_URL}/api/analisis`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(body),
      }
    );

  } catch {

    throw new Error(
      "No se pudo conectar con el servidor de RiftLens."
    );

  }

  let data: unknown;

  try {

    data = await response.json();

  } catch {

    throw new Error(
      "El servidor devolvió una respuesta no válida."
    );

  }

  if (!response.ok) {

    const errorData = data as {
      detail?: string;
    };

    throw new Error(
      errorData.detail ||
      "Ocurrió un error al analizar al jugador."
    );

  }

  return data as AnalisisResponse;
}