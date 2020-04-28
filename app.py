from flask import Flask, jsonify, request
from statics.models import User, Bebep, Venue, Booking, BookingHistory, get, topup_bebep
import random, string

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
        return jsonify(get("User"))
    elif request.method == 'POST':
        new_user = User(id=generateID(30), nama=request.form['nama'], email=request.form['email'],
                        phone=request.form['phone'], registered_at=request.form['registered_at'])
        return jsonify(new_user.save())


@app.route('/bebep', methods=['POST', 'PUT'])
def process_bebep():
    if request.method == 'POST':
        new_bebep_account = Bebep(id=generateID(30), user_id=request.form['user_id'], balance=0)
        return jsonify(new_bebep_account.save())
    elif request.method == 'PUT':
        return jsonify(topup_bebep(user_id=request.form['user_id'], balance=request.form['balance']))


if __name__ == '__main__':
    app.run()
