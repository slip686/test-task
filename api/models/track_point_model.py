import geoalchemy2.elements
from geoalchemy2 import Geometry

from api import db
from api.models.vehicle_model import VehicleModel


class TrackPointModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(Geometry(geometry_type='POINT', srid=4326))
    speed = db.Column(db.Integer)
    gps_time = db.Column(db.DateTime(timezone=True))
    vehicle_id = db.Column(db.Integer, db.ForeignKey(VehicleModel.vehicle_id))

    def __init__(self, id, point, speed, gps_time, vehicle_id):
        self.id = id
        self.point = geoalchemy2.elements.WKBElement(point)
        self.speed = speed
        self.gps_time = gps_time
        self.vehicle_id = vehicle_id
