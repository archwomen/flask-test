from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
from app import views
app.wsgi_app = ProxyFix(app.wsgi_app)
