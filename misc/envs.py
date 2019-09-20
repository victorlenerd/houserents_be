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
        'DATA_SERVER': os.environ.get('DATA_SERVER', 'http://3.16.29.55:8080'),
        'PORT': os.environ.get('PORT', 5000),
        'REDIS_HOST': os.environ.get('REDIS_HOST', 'localhost'),
        'REDIS_PORT': os.environ.get('REDIS_PORT', 6379),
        'REDIS_PASSWORD': os.environ.get('REDIS_PASSWORD', ''),
        'API_KEY': os.environ.get('API_KEY', 'AKIA2FQCSKOO2PYLYV7M'),
        'API_SECRET': os.environ.get('API_SECRET', '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'),
        'BUCKET_REGION': os.environ.get('BUCKET_REGION', 'us-east-2'),
        'BUCKET_ID': os.environ.get('BUCKET_ID', 'houserents-data')
    }
