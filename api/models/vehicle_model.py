from api import db


class VehicleModel(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True, unique=True)
    vehicle_points = db.relationship('TrackPointModel', backref='vehicle_points', lazy='dynamic')

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
