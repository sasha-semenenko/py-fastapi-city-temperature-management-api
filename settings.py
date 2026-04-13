from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///city_temperature.db"

    model_config = {"from_attributes": True}


settings = Settings()