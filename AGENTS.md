# AGENTS.md

Proyecto ML: predicción de precios de viviendas (Random Forest) -> API FastAPI -> dashboard Streamlit.

## Entorno y comandos

- **No hay `python` en PATH en esta máquina.** Usar `py -3.13` (o `py -3.11`; ambos tienen las deps). `py -3` cae en 3.14, que **no** tiene pandas.
- **Ejecutar siempre desde la raíz del repo**: scripts y tests usan rutas relativas (`data/Housing.csv`, `models/model.pkl`, `docs/pruebas/`).
- API: `py -3.13 src/app.py` -> puerto **8001**
- Dashboard: `py -3.13 -m streamlit run dashboard/app.py` -> puerto 8501
- Tests offline: `py -3.13 -m pytest tests/ --ignore=tests/test_api.py -q` (13 tests). Cobertura: `py -3.13 -m pytest tests/ --cov=src --cov-report=term-missing` (36% total; `app.py` 74%, `predict.py` 71%, `eda/train/generate_dataset` 0% porque corren como scripts).
- Tests con API: `tests/test_api.py` exige la API viva en `localhost:8001`. Sin ella falla con `ConnectionError`; no es un bug del código.

## Gotchas que rompen el flujo

- `data/Housing.csv` **está en git** (1000 filas, seed 42). Si se borra: `py -3.13 src/generate_dataset.py` lo regenera idéntico.
- `models/model.pkl` está commiteado (binario). Se regenera con `py -3.13 src/train.py`.
- Hay `.gitignore`; los `__pycache__/*.pyc` que estaban commiteados ya se quitaron del índice.
- `POST /run-eda` apunta a `src/eda.py` (minúsculas, correcto para Linux). Antes buscaba `src/EDA.py`.
- **Consola Windows = cp1252**: cualquier print con emoji revienta (`UnicodeEncodeError`). `src/app.py` hace `sys.stdout.reconfigure(encoding="utf-8")` al importar; `/run-eda` pasa `PYTHONIOENCODING=utf-8` al hijo. Si agregás prints a `src/eda.py` o `src/train.py`, no los toques sin ese reconfigure.
- El puerto 8001 sale de `PORT` en `src/app.py` y de `API_URL` en `dashboard/app.py` y `tests/test_api.py`. Default 8001 en los tres.

## Arquitectura real (distinta a la que sugiere el README)

- Flujo efectivo: `generate_dataset.py` -> `train.py` -> `models/model.pkl` -> `src/app.py` / `dashboard/app.py`.
- **`src/preprocess.py` fue borrado**: nada lo usaba (ni `train.py`, ni la API, ni los tests) y escalarle datos a Random Forest no aporta nada. `train.py` hace su propio `pd.get_dummies(drop_first=True)`. Cualquier cambio de encoding exige reentrenar `model.pkl` y resincronizar README + manual + panel del dashboard.
- **El dashboard ya no carga `model.pkl`**: predice vía `POST /predict`. Si la API no está arriba muestra error y listo; no hay fallback local. `models/model.pkl` solo lo leen `src/app.py` y `src/predict.py`.
- Encoding en predicción: se hace `get_dummies` sobre una sola fila y luego se rellenan con 0 las columnas de `model.feature_names_in_`, que fijan el orden. No mandar DataFrames crudos al modelo.

## Métricas (verificadas contra el modelo commiteado, 1000 filas)

- R² ≈ **0.83**, MAE ≈ **₹948.270** (1000 filas, 13 columnas tras encoding).
- Métricas, README y manual ya están sincronizados con el modelo commiteado. Si se reentrena `model.pkl`, recalcular y volver a sincronizar los tres.

## Convenciones

- Endpoints, UI y comentarios en español; identificadores en inglés. Los nombres de features vienen del dataset y los consume el modelo entrenado: no renombrar.
- Sin linter, formateador, type checker ni CI. No introducirlos sin que se pida.
- `src/predict.py` reescribe `sys.stdout` con un wrapper utf-8 al importarse; molesta bajo captura de pytest.
- Documentación de usuario en `docs/pruebas/MANUAL_USUARIO.md` (artefactos `[cite_start]` ya limpiados). Escenario 1 (casa de lujo) predice ~₹10,6M con el modelo actual; escenario 2 ~₹3,24M.