from flask import Flask
from data_manager import DataManager
from models import db, Movie
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
