from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder='app/build')
app.config['DEBUG'] = True
CORS(app)

from app import views
