from flask_marshmallow import Marshmallow

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


class OrderSchema(ma.Schema):
    analysis = ma.Nested(AnalysisSchema())

    class Meta:
        fields = ('result', 'analysis')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
