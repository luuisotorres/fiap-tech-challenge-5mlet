# FIAP Tech Challenge — Vitivinicultura Embrapa API

[![Run on Render](https://img.shields.io/badge/Run%20on-Render-2f3241?logo=render&logoColor=white&style=for-the-badge)](https://fiap-tech-challenge-5mlet.onrender.com)

![In Construction](https://img.shields.io/badge/status-in--construction-yellow?style=for-the-badge)
---
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Poetry](https://img.shields.io/badge/Poetry-1.6.1-4B5162?style=for-the-badge&logo=python)

> A FastAPI project to serve production, processing, commercialization, import, and export data from [Vitivinicultura Embrapa](http://vitibrasil.cnpuv.embrapa.br/).

This project was built as part of the Machine Learning Engineering postgrad challenge at [FIAP](https://github.com/fiap). It uses `Poetry`, `FastAPI`, and a custom scraping pipeline with JWT authentication.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Authentication](#authentication)
- [Endpoints Overview](#endpoints-overview)
- [Testing Locally](#testing-locally)
- [Environment Variables](#environment-variables)
- [Poetry Usage](#poetry-usage)
- [Deployment (Render)](#deployment-render)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Video Demonstration](#video-demonstration)
- [Authors](#authors)
- [License](#license)

---

## Features

- `/login` for JWT token authentication
- `/producao`, `/processamento`, `/comercializacao`, `/importacao` and `/exportacao` endpoints with structured BaseModel responses
- Swagger and ReDoc API docs included
- Data scraped and parsed directly from Vitibrasil HTML tables
- Environment variable management with `.env` support
- Fully deployable on Render

---

## Project Structure

```
.
├── assets/               # Images used in README
├── cache/                # Cached HTML pages 
├── notebooks/            # Jupyter notebooks
├── src/
│   └── fiap_tech_challenge_5mlet/
│       ├── api/              # API routes
│       ├── auth/             # JWT handlers
│       ├── models/           # Pydantic BaseModels
│       ├── scraper/          # HTML scraping and parsing logic
│       ├── utils/            # Table parsers
│       ├── config.py         # Settings via pydantic-settings
│       └── app.py            # FastAPI app entrypoint
├── render.yaml           # Render deployment configuration
├── README.md             # Project documentation
├── .env.example          # Sample environment variables
├── pyproject.toml        # Poetry dependencies and metadata
└── poetry.lock           # Locked package versions for reproducibility
```

---

## Authentication

Make a `POST` request to `/login` with the following JSON:

```json
{
  "username": "admin",
  "password": "secret"
}
```

Returns a JWT token to access protected endpoints.

![Postman login](assets/postman-login.png)

---

## Endpoints Overview

Authenticated routes include:

- `GET /comercializacao?year=2023`
- `GET /processamento?year=2023&category=viniferas`
- `GET /producao?year=2023`
- `GET /importacao?year=2023&category=vinhos_de_mesa`
- `GET /exportacao?year=2023&category=vinhos_de_mesa`

**Possible HTTP Status Codes for endpoints:**
- 200 OK: Request succeeded
- 401 Unauthorized: Missing or invalid token
- 422 Unprocessable Entity: Invalid parameters
- 503 Service Unavailable: External data source unreachable

Send a `GET` request to `/comercializacao` to get data for default year`2023`:
![postman-comercializacao](assets/post-comercializacao.png)

The following flowchart illustrates how the API functions.
![api-flowchart](assets/api-flowchart.png)

## Docs Interface:

FastAPI automatically provides Swagger UI:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (if running locally) or use the deployed URL's `/docs`.
![Swagger UI](assets/docs.png)

---

## Testing Locally

1. Clone this repo:
   ```bash
   git clone https://github.com/luuisotorres/fiap-tech-challenge-5mlet.git
   cd fiap-tech-challenge-5mlet
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Copy `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Run app:
   ```bash
   poetry run uvicorn fiap_tech_challenge_5mlet.app:app --reload
   ```

---

## Environment Variables

Create a `.env` file using the provided `.env.example`.

| Variable               | Description                         |
|------------------------|-------------------------------------|
| JWT_SECRET_KEY         | Secret used to sign tokens          |
| JWT_ALGORITHM          | Signing algorithm (default: HS256)  |
| JWT_EXP_DELTA_SECONDS  | Token lifetime (default: 3600 sec)  |
| TEST_USERNAME          | Login username                      |
| TEST_PASSWORD          | Login password                      |

Generate a secure JWT secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Poetry Usage

This project uses [Poetry](https://python-poetry.org/) for dependency management and environment isolation. Poetry simplifies handling Python packages by:

- Managing the project's virtual environment
- Installing dependencies from `pyproject.toml`
- Keeping dependency versions locked via `poetry.lock`
- Providing an easy way to run scripts inside the virtual environment

### Common Commands

- Install dependencies:

  ```bash
  poetry install
  ```

- Activate the virtual environment:

  ```bash
  poetry env activate
  ```

- Run commands inside the environment:

  ```bash
  poetry run <your-command>
  ```

Example (running the FastAPI app):

```bash
poetry run uvicorn fiap_tech_challenge_5mlet.app:app --reload
```

If you don't have Poetry installed, you can install it with:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## Deployment (Render)

This API is live and publicly accessible via [Render](https://render.com), a platform that makes it easy to deploy web apps, APIs, and background workers with minimal configuration.

👉 **[Try it on Render](https://fiap-tech-challenge-5mlet.onrender.com)** — no setup required, just explore the live API!

---


## Machine Learning Pipeline

Embrapa's data will be used to feed a forecasting model.

Our API will be consumed at scheduled intervals, and the retrieved data will be stored in a database.

This data will then undergo an ETL process to generate relevant features for use in the machine learning model.

Finally, predictions will be made available through a `/predict` endpoint, and the results will also be stored back in the database.

The following diagram provides an overview of the application's workflow.
![ml-diagram](assets/ml-diagram.png)

### 1. Data Ingestion

Data will be made available through our application and served via an API hosted on Render.
A scheduler — such as AWS Lambda, a cron job, or Apache Airflow — will periodically call this API to retrieve the data.


### 2. Data Storage and ETL

Each time the API is called, the raw data will be stored in an S3 bucket (raw layer).
Using AWS Glue, Apache Airflow, or equivalent orchestration tools — alongside libraries such as Pandas and NumPy — the data will be cleaned and transformed as needed.
As part of this process, relevant features will be engineered for use in the machine learning model.

### 3. Machine Learning

Models will be trained and evaluated using MLflow, which will also be used to track experiments.
Model artifacts will be stored in an S3 bucket and consumed during the inference stage.
A /predict endpoint will be exposed through a FastAPI application, serving predictions to users and storing the results in a predictions table.

---

## Video Demonstration

Here's a quick video demonstration of the project in action and further explanation:

[![Watch the video](https://img.youtube.com/vi/vAFqORreXL8/0.jpg)](https://www.youtube.com/watch?v=vAFqORreXL8)

---

## Authors

[Izabelly de Oliveira Menezes](https://github.com/izabellyomenezes)

[Larissa Diniz](https://github.com/Ldiniz737)

[Luis Fernando Torres](https://github.com/luuisotorres)

[Rafael Callegari](https://github.com/rafaelcallegari)

[Renato Inomata](https://github.com/renatoinomata)

---

## License

MIT License