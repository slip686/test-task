from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
app.config.from_object(Config)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='TEST-TASK',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0',

    ),
    'APISPEC_SWAGGER_URL': '/docs_json',
    'APISPEC_SWAGGER_UI_URL': '/docs'
})


db = SQLAlchemy(app)
ma = Marshmallow(app)
ctx = app.app_context()
ctx.push()
docs = FlaskApiSpec(app)

from api.models.track_point_model import TrackPointModel
from api.models.vehicle_model import VehicleModel

db.create_all()




