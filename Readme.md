### empty draft for FastApi project

### Stack
Fastapi, 
postgres,
Sqlalchemy,
Alembic,
Docker,
poetry,
pytest
python (3.10 - 3.13)

### setup
- create virtual environment, .env, check DB_PORT for local postgres or postgres in docker
- `poetry install --no-root`

- running using poetry and make: `make run`
- http://localhost:8000/docs/
- creating postgres db from docker-compose: `make up`

### notes


enter docker container (why?):
`docker exec -it 47dece677d93  bash`

in host console:
`psql -h 127.0.0.1 -p 5433 -U user postgres`


### alembic:

`alembic init -t async migration`


-edit files configs:

`sqlalchemy.url = postgresql+asyncpg://%(DB_USERNAME)s:%(DB_PASSWORD)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s`

--
```
from starlette.config import Config

settingenv = Config(".env")
DB_NAME: str = settingenv("DB_NAME", cast=str)
DB_HOST: str = settingenv("DB_HOST", default="localhost", cast=str)
DB_USERNAME: str = settingenv("DB_USERNAME", cast=str)
DB_PORT: int = settingenv("DB_PORT", cast=str)
DB_PASSWORD: str = settingenv("DB_PASSWORD", cast=str)

config = context.config
section = config.config_ini_section

config.set_section_option(section, "DB_USERNAME", DB_USERNAME)
config.set_section_option(section, "DB_PASSWORD", DB_PASSWORD)
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_NAME", DB_NAME)

from service.db_setup.models import User, Base
target_metadata = Base.metadata
```



`alembic revision --autogenerate -m 'initial'`
