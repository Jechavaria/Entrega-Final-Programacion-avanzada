import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const defaultFeatures = {
  LIMIT_BAL: 20000,
  SEX: 2,
  EDUCATION: 2,
  MARRIAGE: 1,
  AGE: 30,
  PAY_0: 0,
  PAY_2: 0,
  PAY_3: 0,
  PAY_4: 0,
  PAY_5: 0,
  PAY_6: 0,
  BILL_AMT1: 0,
  BILL_AMT2: 0,
  BILL_AMT3: 0,
  BILL_AMT4: 0,
  BILL_AMT5: 0,
  BILL_AMT6: 0,
  PAY_AMT1: 0,
  PAY_AMT2: 0,
  PAY_AMT3: 0,
  PAY_AMT4: 0,
  PAY_AMT5: 0,
  PAY_AMT6: 0,
}

function App() {
  const [metrics, setMetrics] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [features, setFeatures] = useState(defaultFeatures)
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('Listo')

  useEffect(() => {
    loadMetrics()
    loadPredictions()
  }, [])

  async function loadMetrics() {
    try {
      const res = await fetch(`${API_URL}/metrics`)
      if (res.ok) setMetrics(await res.json())
    } catch (error) {
      console.warn('No se pudieron cargar métricas', error)
    }
  }

  async function loadPredictions() {
    try {
      const res = await fetch(`${API_URL}/predictions`)
      if (res.ok) setPredictions(await res.json())
    } catch (error) {
      console.warn('No se pudieron cargar predicciones', error)
    }
  }

  async function handleTrain() {
    setStatus('Entrenando...')
    const res = await fetch(`${API_URL}/train`, { method: 'POST' })
    if (res.ok) {
      setMetrics(await res.json())
      setStatus('Entrenamiento completado')
    } else {
      setStatus('Error en entrenamiento')
    }
  }

  async function handlePredict(event) {
    event.preventDefault()
    setStatus('Generando predicción...')
    const res = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(features),
    })
    if (res.ok) {
      const data = await res.json()
      setResult(data)
      setStatus('Predicción lista')
      loadPredictions()
    } else {
      setStatus('Error en predicción')
    }
  }

  function handleChange(event) {
    const { name, value } = event.target
    setFeatures((prev) => ({ ...prev, [name]: Number(value) }))
  }

  return (
    <div className="container">
      <h1>ML Credit Default</h1>
      <section className="card">
        <h2>Pipelines & endpoints</h2>
        <p>Backend: <code>{API_URL}</code></p>
        <button onClick={handleTrain}>Entrenar modelo</button>
        <p>Status: {status}</p>
      </section>

      <section className="card">
        <h2>Métricas actuales</h2>
        {metrics ? (
          <div className="grid">
            <div>Accuracy</div><div>{metrics.accuracy.toFixed(4)}</div>
            <div>ROC AUC</div><div>{metrics.roc_auc.toFixed(4)}</div>
            <div>Casos de prueba</div><div>{metrics.n_samples}</div>
            <div>Entrenado</div><div>{metrics.created_at}</div>
          </div>
        ) : (
          <p>No hay métricas todavía. Usa Entrenar modelo.</p>
        )}
      </section>

      <section className="card">
        <h2>Predicción</h2>
        <form onSubmit={handlePredict} className="prediction-form">
          {Object.entries(features).map(([key, value]) => (
            <label key={key}>
              {key}
              <input name={key} value={value} onChange={handleChange} type="number" />
            </label>
          ))}
          <button type="submit">Predecir</button>
        </form>
        {result && (
          <div className="result">
            <p>Predicción: {result.prediction === 1 ? 'Default' : 'No default'}</p>
            <p>Probabilidad: {result.probability}</p>
          </div>
        )}
      </section>

      <section className="card">
        <h2>Predicciones recientes</h2>
        {predictions.length ? (
          <table>
            <thead>
              <tr><th>ID</th><th>Predicción</th><th>Probabilidad</th><th>Creado</th></tr>
            </thead>
            <tbody>
              {predictions.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.prediction}</td>
                  <td>{item.probability.toFixed(4)}</td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No hay predicciones registradas.</p>
        )}
      </section>
    </div>
  )
}

export default App
