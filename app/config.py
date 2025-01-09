import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    DEBUG = False
    TESTING = False
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/financial_ai")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
