from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')


class AnalysisSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class CategorySchema(ma.Schema):
    analyzes = ma.Nested(AnalysisSchema(many=True))

    class Meta:
        fields = ('id', 'name', 'analyzes')


categories_schema = CategorySchema(many=True)


class DoctorOrderSchema(ma.Schema):
    id = fields.Integer(attribute='doctor.id')
    name = fields.String(attribute='doctor.username')

    class Meta:
        fields = ('id', 'name')


class OrderSchema(ma.Schema):
    analysis = ma.Nested(AnalysisSchema())
    doctors = ma.Nested(DoctorOrderSchema(many=True))

    class Meta:
        fields = ('id', 'result', 'analysis', 'doctors')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
