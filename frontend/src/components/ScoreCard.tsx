interface ScoreCardProps {

  score: number;

  titulo?: string;
}


function ScoreCard({
  score,
  titulo = "Puntuación de rendimiento",
}: ScoreCardProps) {

  const scoreNormalizado =
    Math.min(
      Math.max(
        score,
        0
      ),
      100
    );


  const obtenerNivel = () => {

    if (scoreNormalizado >= 85) {
      return "Excelente";
    }

    if (scoreNormalizado >= 70) {
      return "Muy bueno";
    }

    if (scoreNormalizado >= 55) {
      return "Bueno";
    }

    if (scoreNormalizado >= 40) {
      return "En desarrollo";
    }

    return "Necesita mejorar";
  };


  return (

    <section className="section score-section">

      <div className="score-card">

        <div>

          <span className="section-eyebrow">
            SCORE
          </span>

          <h2>
            {titulo}
          </h2>

          <p>
            Evaluación general de tu rendimiento
            frente a la referencia profesional.
          </p>

        </div>


        <div className="score-value">

          <strong>
            {Math.round(scoreNormalizado)}
          </strong>

          <span>
            /100
          </span>

        </div>


        <div className="score-level">
          {obtenerNivel()}
        </div>

      </div>

    </section>

  );
}


export default ScoreCard;