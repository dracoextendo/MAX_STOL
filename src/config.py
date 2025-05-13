import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
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