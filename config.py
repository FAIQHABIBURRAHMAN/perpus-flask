

import os

class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'kunci-rahasia-project'
    )

    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'db_perpustakaan'
