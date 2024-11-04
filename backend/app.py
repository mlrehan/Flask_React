from flask import Flask
from models import db
from flask_cors import CORS
from routes import views

app = Flask(__name__)
CORS(app=app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///lait.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)

app.register_blueprint(views)


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)
