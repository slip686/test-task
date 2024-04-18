from flask import abort
from sqlalchemy import text

from api import app, db
from api.models.vehicle_model import VehicleModel
from api.schemas.point import point_schemas
from api.models.track_point_model import TrackPointModel
from geojson import MultiPoint
from flask_apispec import doc


@app.route('/vehicles', provide_automatic_options=False)
@doc(description='Api for vehicles.', tags=['Vehicles'],
     summary='Returns list with all vehicles last point.')
def get_all_vehicles():
    query_text = text('SELECT track_point_model.id, track_point_model.point,'
                      'track_point_model.speed, track_point_model.gps_time,'
                      'track_point_model.vehicle_id FROM track_point_model '
                      'JOIN (SELECT track_point_model.vehicle_id, MAX(track_point_model.gps_time) '
                      'AS last_gps_time FROM track_point_model group by track_point_model.vehicle_id) AS t '
                      'ON track_point_model.vehicle_id = t.vehicle_id '
                      'AND track_point_model.gps_time = t.last_gps_time')
    try:
        points = db.session.execute(query_text).fetchall()
        return point_schemas.dump(TrackPointModel(*point) for point in points), 200
    except Exception:
        db.session.rollback()


@app.route('/vehicles/<int:vehicle_id>', provide_automatic_options=False)
@doc(description='Api for vehicles.', tags=['Vehicles'], summary='Returns list of points for specified vehicle id',
     responses={404: {'Description': 'Vehicle not found'}, 200: {'Description': 'OK'}})
def get_vehicle_by_id(vehicle_id):
    vehicle = VehicleModel.query.get(vehicle_id)
    if vehicle is None:
        abort(404, description=f"Vehicle with id={vehicle_id} not found")
    points = point_schemas.dump(vehicle.vehicle_points.order_by(TrackPointModel.gps_time))
    return points, 200


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
