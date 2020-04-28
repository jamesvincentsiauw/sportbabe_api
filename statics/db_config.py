from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = "GB981UA7YT91"
engine = create_engine(os.getenv("DB_URI"))
Session = sessionmaker(bind=engine)
sess = Session()

db = SQLAlchemy(app)