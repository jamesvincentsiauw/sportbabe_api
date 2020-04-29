import random
import string
import datetime
import requests
import os

from flask import Flask, jsonify, request

from statics.models import User, Bebep, Booking, get, get_by_id, topup_bebep
from statics.ktp_verification import id_verification

app = Flask(__name__)
app.secret_key = "GB981UA7YT91"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def generateID(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users', methods=['GET', 'POST'])
def process_user():
    if request.method == 'GET':
        if request.args.get('id'):
            return jsonify(get_by_id(request.args.get('id'), "User"))
        else:
            return jsonify(get("User"))
    elif request.method == 'POST':
        new_user = User(id=generateID(30), nama=request.form['nama'], email=request.form['email'],
                        phone=request.form['phone'], registered_at=datetime.datetime.now())
        return jsonify(new_user.save())


@app.route('/bebep', methods=['POST', 'PUT'])
def process_bebep():
    if request.method == 'POST':
        new_bebep_account = Bebep(id=generateID(30), user_id=request.form['user_id'], balance=0)
        return jsonify(new_bebep_account.save())
    elif request.method == 'PUT':
        return jsonify(topup_bebep(user_id=request.form['user_id'], balance=request.form['balance']))


@app.route('/venue/book/<id>', methods=['POST'])
def book_venue(id):
    data = requests.get('http://127.0.0.1:5000/venues?id='+id)
    venue = data.json()['results']
    start_hour = request.form['start_hour']
    end_hour = request.form['end_hour']
    total_price = (end_hour-start_hour)*venue['price_per_hour']
    new_booking = Booking(id=generateID(30), user_id=request.form['user_id'], venue_id=venue['id'],
                          start_hour=start_hour, end_hour=end_hour, total_price=total_price,
                          booked_at=datetime.datetime.now(), isFinished=False)
    return jsonify(new_booking.save())


@app.route('/verification', methods=['POST'])
def ktp_verification():
    try:
        if request.files:
            file = request.files['img']
            if allowed_file(file.filename):
                filepath = 'statics/image/' + file.filename
                file.save(os.path.join(filepath))
                return jsonify(id_verification(filepath))
            else:
                return jsonify({
                    'status': 400,
                    'message': 'Bad Input Parameter. Image Must be PNG, JPG, or JPEG'
                })
        else:
            return jsonify({
                'status': 400,
                'message': 'Bad Input Parameter. Image Needed'
            })
    except Exception as e:
        ret = {
            'status': 500,
            'message': e.args
        }
        return ret


if __name__ == '__main__':
    app.run()
