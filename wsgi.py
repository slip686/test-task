from api import app, docs
from api.handlers import vehicles

docs.register(vehicles.get_all_vehicles)
docs.register(vehicles.get_vehicle_by_id)
docs.register(vehicles.get_vehicle_track_by_id)

if __name__ == '__main__':
    app.run()