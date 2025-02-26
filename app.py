from flask import Flask
from db import init_db
from routes import bp
from config import DevelopmentConfig, ProductionConfig
import os

app = Flask(__name__)

if os.getenv("FLASK_ENV") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

init_db(app)

# Registrar as rotas organizadas
app.register_blueprint(bp, url_prefix='/runIFG')

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])



