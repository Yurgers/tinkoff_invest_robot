from pydantic import BaseSettings, ValidationError
from loguru import logger


class Settings(BaseSettings):
    api_token: str
    api_token_sandbox: str | None
    app_name: str = 'yurgers'


try:
    settings = Settings()

except ValidationError as err:
    logger.error(str(err))
    exit(-1)
