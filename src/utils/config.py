import os
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..", ".env"),
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
    private_key_path: SecretStr
    public_key_path: SecretStr
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 2

    @property
    def PRIVATE_KEY_PATH(self):
        return Path(self.private_key_path.get_secret_value())

    @property
    def PUBLIC_KEY_PATH(self):
        return Path(self.public_key_path.get_secret_value())

jwt_config = JWTConfig()