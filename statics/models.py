from flask_sqlalchemy import SQLAlchemy
from statics.db_config import db, sess


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.VARCHAR, unique=True, primary_key=True)
    nama = db.Column(db.VARCHAR, nullable=False)
    email = db.Column(db.VARCHAR, unique=True, nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    phone = db.Column(db.VARCHAR)
    registered_at = db.Column(db.TIMESTAMP)

    def save(self):
        try:
            sess.add(self)
            sess.commit()
            res = {
                'status': 201,
                'message': "New User Created",
                'results': {
                    'id': self.id,
                    'nama': self.nama,
                    'email': self.email,
                    'password': self.password,
                    'phone': self.password,
                    'registered_at': self.registered_at
                }
            }
            return res
        except Exception as e:
            ret = {
                'status': 500,
                'message': e.args
            }
            return ret


class Bebep(db.Model):
    __tablename__ = "Bebep"
    id = db.Column(db.VARCHAR, primary_key=True, unique=True)
    user_id = db.Column(db.VARCHAR, unique=False, nullable=False)
    balance = db.Column(db.NUMERIC, nullable=False, default=0)

    def save(self):
        try:
            sess.add(self)
            sess.commit()
            res = {
                'status': 201,
                'message': "New Bebep Account Created",
                'results': {
                    'id': self.id,
                    'user_id': self.user_id,
                    'balance': self.balance
                }
            }
            return res
        except Exception as e:
            ret = {
                'status': 500,
                'message': e.args
            }
            return ret


class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.VARCHAR, primary_key=True, unique=True)
    image_path = db.Column(db.VARCHAR, nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    address = db.Column(db.VARCHAR, nullable=False)
    price_per_hour = db.Column(db.NUMERIC, nullable=False)
    open_hour = db.Column(db.TIME, nullable=False)
    close_hour = db.Column(db.TIME, nullable=False)
    registered_at = db.Column(db.TIMESTAMP, nullable=False)

    def save(self):
        try:
            sess.add(self)
            sess.commit()
            res = {
                'status': 201,
                'message': "New Venue Created",
                'results': {
                    'id': self.id,
                    'image_path': self.image_path,
                    'name': self.name,
                    'address': self.address,
                    'price_per_hour': self.price_per_hour,
                    'open_hour': self.open_hour,
                    'close_hour': self.close_hour,
                    'registered_at': self.registered_at
                }
            }
            return res
        except Exception as e:
            ret = {
                'status': 500,
                'message': e.args
            }
            return ret


class Booking(db.Model):
    __table_name__ = "Booking"
    id = db.Column(db.VARCHAR, primary_key=True, unique=True)
    user_id = db.Column(db.VARCHAR, nullable=False)
    venue_id = db.Column(db.VARCHAR, nullable=False)
    start_hour = db.Column(db.TIME, nullable=False)
    end_hour = db.Column(db.TIME, nullable=False)
    total_price = db.Column(db.NUMERIC, nullable=False)
    booked_at = db.Column(db.TIMESTAMP, nullable=False)
    isFinished = db.Column(db.BOOLEAN, nullable=False)

    def save(self):
        try:
            sess.add(self)
            sess.commit()
            res = {
                'status': 201,
                'message': "New Booking Created",
                'results': {
                    'id': self.id,
                    'user_id': self.user_id,
                    'venue_id': self.venue_id,
                    'start_hour': self.start_hour,
                    'end_hour': self.end_hour,
                    'total_price': self.total_price,
                    'booked_at': self.booked_at,
                    'isFinished': self.isFinished
                }
            }
            return res
        except Exception as e:
            ret = {
                'status': 500,
                'message': e.args
            }
            return ret


class BookingHistory(db.Model):
    __tablename__ = "BookingHistory"
    id = db.Column(db.VARCHAR, primary_key=True, unique=True)
    user_id = db.Column(db.VARCHAR, nullable=False)
    booking_id = db.Column(db.VARCHAR, nullable=False)

    def save(self):
        try:
            sess.add(self)
            sess.commit()
            res = {
                'status': 201,
                'message': "New Booking History Created",
                'results': {
                    'id': self.id,
                    'user_id': self.user_id,
                    'booking_id': self.booking_id,
                }
            }
            return res
        except Exception as e:
            ret = {
                'status': 500,
                'message': e.args
            }
            return ret


def get(model):
    try:
        res = []
        if model == "User":
            hasils = sess.query(User).all()
            for hasil in hasils:
                data = {
                    'id': hasil.id,
                    'nama': hasil.nama,
                    'email': hasil.email,
                    'phone': hasil.phone,
                    'registered_at': hasil.registered_at
                }
                res.append(data)
            ret = {
                'status': 200,
                'message': "These Are the Registered Users",
                'results': res
            }
        elif model == "Bebep":
            hasils = sess.query(Bebep).all()
            for hasil in hasils:
                data = {
                    'id': hasil.id,
                    'user_id': hasil.user_id,
                    'balance': hasil.balance
                }
                res.append(data)
            ret = {
                'status': 200,
                'message': "These Are the Registered Bebep Account",
                'results': res
            }
        elif model == "Venue":
            hasils = sess.query(Venue).all()
            for hasil in hasils:
                data = {
                    'id': hasil.id,
                    'image_path': hasil.image_path,
                    'name': hasil.name,
                    'address': hasil.address,
                    'price_per_hour': hasil.price_per_hour,
                    'open_hour': hasil.open_hour,
                    'close_hour': hasil.close_hour,
                    'registered_at': hasil.registered_at
                }
                res.append(data)
            ret = {
                'status': 200,
                'message': "These Are the Registered Bebep Account",
                'results': res
            }
        elif model == "Booking":
            hasils = sess.query(Booking).all()
            for hasil in hasils:
                data = {
                    'id': hasil.id,
                    'user_id': hasil.user_id,
                    'venue_id': hasil.venue_id,
                    'start_hour': hasil.start_hour,
                    'end_hour': hasil.end_hour,
                    'total_price': hasil.total_price,
                    'booked_at': hasil.booked_at,
                    'isFinished': hasil.isFinished
                }
                res.append(data)
            ret = {
                'status': 200,
                'message': "These Are the Registered Bebep Account",
                'results': res
            }
        elif model == "BookingHistory":
            hasils = sess.query(BookingHistory).all()
            for hasil in hasils:
                data = {
                    'id': hasil.id,
                    'user_id': hasil.user_id,
                    'booking_id': hasil.booking_id,
                }
                res.append(data)
            ret = {
                'status': 200,
                'message': "These Are the Registered Bebep Account",
                'results': res
            }
        else:
            ret = {
                'status': 400,
                'message': "Bad Parameter",
                'results': res
            }
        return ret
    except Exception as e:
        ret = {
            'status': 500,
            'message': e.args
        }
        return ret

def topup_bebep(user_id, balance):
    try:
        selected_account = sess.query(Bebep).filter(Bebep.user_id == user_id).first()
        if selected_account is not None:
            new_balance = selected_account.balance + balance
            data = {
                'balance': new_balance
            }
            edited_account = sess.query.filter(Bebep.user_id == user_id).update(data,synchronize_session=False)
            sess.commit()
            if edited_account == 1:
                ret = {
                    'status': 200,
                    'message': 'Data updated! Your Bebep balance is '+new_balance+" now!"
                }
            else:
                ret = {
                    'status': 500,
                    'message': "Something's went wrong with our server. Please try again later!"
                }
            return ret
        else:
            ret = {
                'status': 200,
                'message': "Bebep Account is not found"
            }
            return ret
    except Exception as e:
        ret = {
            'status': 200,
            'message': e.args,
        }
        return ret
