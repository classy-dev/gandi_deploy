from flask import Flask

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_object('config')

from app import api_bp, template_bp

app.register_blueprint(api_bp, url_prefix='/api')

app.register_blueprint(template_bp, url_prefix='/')

from Model import db

db.init_app(app)

if __name__ == "__main__":

    app.run(host='localhost', debug=True)
