import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


class Config:
    """
    Configuration class for handling application settings.
    """

    def __init__(self):
        self.load_env()
        self.setup_database()

    def load_env(self):
        """
        Load environment variables from .env file.
        """
        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
        self.IS_ALLOWED_CREDENTIALS = os.getenv("IS_ALLOWED_CREDENTIALS")
        self.ALLOWED_METHODS = os.getenv("ALLOWED_METHODS")
        self.ALLOWED_HEADERS = os.getenv("ALLOWED_HEADERS")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        if self.SECRET_KEY is None:
            raise ValueError("No SECRET_KEY found in environment variables")
        if self.ALGORITHM is None:
            raise ValueError("No ALGORITHM found in environment variables")

    def setup_database(self):
        """
        Setup database connection and engine.
        """
        self.database_url = os.getenv("DATABASE_URL")
        if self.database_url is None:
            raise ValueError("No DATABASE_URL found in environment variables")

        self.engine = create_engine(self.database_url, echo=True)


config_env = Config()
