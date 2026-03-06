# FastAPI Project Template

## 🚀 Tech Stack

- **Framework**: FastAPI (async support)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **Dependency Management**: Poetry
- **Testing**: pytest
- **Python Version**: 3.10 - 3.13

## 📋 Prerequisites

- Python 3.10+
- Poetry
- Docker and Docker Compose
- PostgreSQL (optional - use Docker)

## 🛠️ Project Setup

### 1. Environment Configuration
- pyenv local 3.10
- pyenv exec python3 -m venv .venv
- source .venv/bin/activate
- Create an `.env` file in the root directory.


### 2.  Install Dependencies
`poetry install --no-root`

### 3.  Setup

- running using poetry and make: `make run`
- http://localhost:8000/docs/
- creating postgres db from docker-compose: `make up`

###  Notes

enter docker container (example):
`docker exec -it 47dece677d93  bash`

in host console:
`psql -h 127.0.0.1 -p 5433 -U user postgres`


