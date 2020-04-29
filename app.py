import random
import string
import datetime
import requests

from flask import Flask, jsonify, request

from statics.models import User, Bebep, Booking, get, get_by_id, topup_bebep

app = Flask(__name__)
app.secret_key = "GB981UA7YT91"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


def generateID(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


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


if __name__ == '__main__':
    app.run()
