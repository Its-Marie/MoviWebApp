from flask import Flask
from data_manager import DataManager
from models import db, Movie
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "temporary-secret-key-12345")

db.init_app(app)
data_manager = DataManager()


@app.route("/")
def home():
    return "Welcome to MoviWeb App!"


@app.route("/users")
def list_users():
    users = data_manager.get_all_users()  # Correct method name from your DataManager
    return str(users)  # Temporarily returning users as a string


if __name__ == "__main__":
    with app.app_context():
        os.makedirs("data", exist_ok=True)
        db.create_all()

    app.run(debug=True)
