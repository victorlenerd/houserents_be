import os


def get():
    return {
        'ENV': os.environ.get('ENV', 'DEV'),
        'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
        'DB_NAME': os.environ.get('DB_NAME', 'postgres'),
        'DB_USER': os.environ.get('DB_USER', 'postgres'),
        'DB_PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'DB_PORT': os.environ.get('DB_PORT', 5432),
        'PORT': os.environ.get('PORT', 5000),
        'DATA_SERVER': os.environ.get('DATA_SERVER', 'http://localhost:8080'),
        'PORT': os.environ.get('PORT', 5000),
        'REDIS_HOST': os.environ.get('REDIS_HOST', 'localhost'),
        'REDIS_PORT': os.environ.get('REDIS_PORT', 6379),
        'REDIS_PASSWORD': os.environ.get('REDIS_PASSWORD', '')
    }
