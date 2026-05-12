import os


class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    JSON_INDENT = 2
    API_VERSION = '1.0.0'
    API_NAME = 'External API Server'
