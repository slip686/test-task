from api import ma
from api.models.track_point_model import TrackPointModel

from marshmallow import fields
from marshmallow_sqlalchemy.convert import ModelConverter
from geoalchemy2.elements import WKTElement as WKTGeographyElement
from geoalchemy2.shape import to_shape


class GeographySerializationField(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'point':
                return {'latitude': to_shape(value).x,
                        'longitude': to_shape(value).y}
            else:
                return None

    def _deserialize(self, value, attr, data):
        if value is None:
            return value
        else:
            if attr == 'point':
                return WKTGeographyElement(
                    'POINT({0} {1})'.format(str(value.get('longitude')), str(value.get('latitude'))))
            else:
                return None


class PointSchema(ma.SQLAlchemySchema):
    id = fields.Field(attribute='id')
    point = GeographySerializationField(attribute='point')
    speed = fields.Field(attribute='speed')
    gps_time = fields.Field(attribute='gps_time')
    vehicle_id = fields.Field(attribute='vehicle_id')

    class Meta:
        model = TrackPointModel
        model_converter = ModelConverter


point_schema = PointSchema()
point_schemas = PointSchema(many=True)
