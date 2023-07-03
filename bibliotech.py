from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

from views_tecnologias import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)