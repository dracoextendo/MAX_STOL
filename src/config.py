import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        env_file_encoding="utf-8",
        extra='ignore'
    )

class S3Config(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="S3_")
    access_key: SecretStr
    secret_key: SecretStr
    endpoint_url: SecretStr
    bucket_name: SecretStr
    domain: SecretStr

class DBConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="DB_")
    user: SecretStr
    password: SecretStr
    host: SecretStr
    port: SecretStr
    name: SecretStr

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.user.get_secret_value()}:{self.password.get_secret_value()}@{self.host.get_secret_value()}:{self.port.get_secret_value()}/{self.name.get_secret_value()}"

class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="JWT_")
    secret: SecretStr