import random
import string
import datetime
import requests
import os
import json
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask, jsonify, request

from statics.models import User, Bebep, Booking, get, get_by_id, topup_bebep, isVerified
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
        new_user = User(id=request.form['id'], nama=request.form['nama'], email=request.form['email'],
                        phone=request.form['phone'], registered_at=datetime.datetime.now())
        return jsonify(new_user.save())


@app.route('/bebep', methods=['POST', 'PUT'])
def process_bebep():
    try:
        if isVerified(request.form['user_id']):
            if request.method == 'POST':
                new_bebep_account = Bebep(id=generateID(30), user_id=request.form['user_id'], balance=0)
                return jsonify(new_bebep_account.save())
            elif request.method == 'PUT':
                return jsonify(topup_bebep(user_id=request.form['user_id'], balance=request.form['balance']))
        else:
            return jsonify({
                'status': 403,
                'message': 'Verify account to use Bebep'
            })
    except Exception as e:
        ret = {
            'status': 500,
            'message': e.args
        }
        return ret


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
                if not os.path.exists('statics/image/'):
                    # make a directory if it doesn't exist
                    os.makedirs('statics/image/')
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


@app.route('/bookings', methods=['GET', 'POST'])
def process_booking():
    if request.method == 'GET':
        if request.args.get('user'):
            return jsonify(get_by_id(request.args.get('user'), "Booking"))
        else:
            return jsonify(get("Booking"))
    elif request.method == 'POST':
        new_booking = Booking(id=generateID(30), user_id=request.form['user_id'], venue_id=request.form['venue_id'],
                              start_hour=request.form['start_hour'], end_hour=request.form['end_hour'],
                              total_price=request.form['total_price'], booked_at=datetime.datetime.now(),
                              isFinished=bool(request.form['isFinished']))
        return jsonify(new_booking.save())
    

@app.route('/venues', methods=['GET','POST'])
def process_venue():
    if request.method == 'GET':
        if request.args.get('id'):
            return jsonify(get_by_id(request.args.get('id'), "Venue"))
        else:
            return jsonify(get("Booking"))

#
# @app.route('/covid-19', methods=['GET'])
# def covid_data():
#     datas = requests.get('https://api.kawalcorona.com/indonesia/provinsi')
#     ind = np.arange(1)
#     width = 0.5
#     count = 0
#     province = []
#     death = []
#     confirmed = []
#     recovered = []
#     for key in datas.json():
#         province.append(key['attributes']['Provinsi'])
#         death.append(key['attributes']['Kasus_Meni'])
#         confirmed.append(key['attributes']['Kasus_Posi'])
#         recovered.append(key['attributes']['Kasus_Semb'])
#         count +=1
#         if count == 5:
#             break
#     i=0
#     while i < 5:
#         plt.bar(ind, confirmed[i], width, label="Positif COVID-19")
#         plt.bar(ind+width, death[i], width, label="Meninggal")
#         plt.bar(ind+width*2, recovered[i], label="Sembuh")
#         plt.ylabel("Jumlah")
#
#         plt.title("Kasus COVID-19 Indonesia")
#         plt.xlabel(province[i])
#         plt.legend(loc='best')
#         plt.show()
#         i += 1
#     return jsonify(datas.json())


if __name__ == '__main__':
    app.run()
