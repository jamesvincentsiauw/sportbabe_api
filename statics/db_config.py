from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "GB981UA7YT91"
engine = create_engine('postgres://kmyuvxeo:YdvWUnLQU-pjXW-Bh1HjpBDvby5I17nv@topsy.db.elephantsql.com:5432/kmyuvxeo')
Session = sessionmaker(bind=engine)
sess = Session()

db = SQLAlchemy(app)