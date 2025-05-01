from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """
    Loads and validates environment variables for JWT settings
    and test credentials.
    Automatically reads from a '.env' file at the project root.
    """
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_exp_delta_seconds: int = 3600
    test_username: str
    test_password: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                "..", ".env")


settings = Settings()
