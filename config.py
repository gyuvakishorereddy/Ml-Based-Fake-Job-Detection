"""
Flask Configuration
"""
import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JSON_SORT_KEYS = False
    
    # Model paths
    MODEL_DIR = 'models'
    DATASET_DIR = '.'
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    HOST = '0.0.0.0'
    PORT = 5000

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
