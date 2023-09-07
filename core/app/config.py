class BaseConfig:
    DEBUG = False
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/edtech-dev-db"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
class ProductionConfig(BaseConfig):
    pass