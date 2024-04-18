from flask import abort
from sqlalchemy import desc

from api import app
from api.models.vehicle_model import VehicleModel
from api.schemas.point import point_schema, point_schemas
from api.models.track_point_model import TrackPointModel
from geojson import MultiPoint
from flask_apispec import doc


@app.route('/vehicles', provide_automatic_options=False)
@doc(description='Api for vehicles.', tags=['Vehicles'],
     summary='Returns list with all vehicles last point.')
def get_all_vehicles():
    vehicles = VehicleModel.query.all()
    points = []
    for vehicle in vehicles:
        points.append(point_schema.dump(vehicle.vehicle_points.order_by(desc(TrackPointModel.gps_time)).first()))
    return points, 200


@app.route('/vehicles/<int:vehicle_id>', provide_automatic_options=False)
@doc(description='Api for vehicles.', tags=['Vehicles'], summary='Returns list of points for specified vehicle id',
     responses={404: {'Description': 'Vehicle not found'}, 200: {'Description': 'OK'}})
def get_vehicle_by_id(vehicle_id):
    vehicle = VehicleModel.query.get(vehicle_id)
    if vehicle is None:
        abort(404, description=f"Vehicle with id={vehicle_id} not found")
    points = point_schemas.dump(vehicle.vehicle_points.order_by(TrackPointModel.gps_time))
    return points, 200


#


@app.route('/vehicles/<int:vehicle_id>/track', provide_automatic_options=False)
@doc(description='Api for vehicles.', tags=['Vehicles'], summary='Returns GEOJSON MultiPoint for specified vehicle id',
     responses={404: {'Description': 'Vehicle not found'}, 200: {'Description': 'OK'}})
def get_vehicle_track_by_id(vehicle_id):
    vehicle = VehicleModel.query.get(vehicle_id)
    if vehicle is None:
        abort(404, description=f"Vehicle with id={vehicle_id} not found")
    points = point_schemas.dump(vehicle.vehicle_points.order_by(TrackPointModel.gps_time))
    track = MultiPoint([(point.get("point").get('longitude'), point.get("point").get('latitude')) for point in points])
    return track, 200
