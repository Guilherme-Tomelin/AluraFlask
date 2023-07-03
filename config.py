
from dotenv import load_dotenv
import os

SECRET_KEY = 'aprendendoflask'

load_dotenv()

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = os.getenv("DB_PASSWORD"),
        servidor = 'localhost',
        database = 'bibliotech'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'