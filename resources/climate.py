from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.climate import ClimateModel
from sqlalchemy.sql import func
from db import db

class Climate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This fießld cannot be left blank!"
                        )
    parser.add_argument('rainfall',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('temperature',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, _id):
        identification = ClimateModel.find_by_id(_id)
        if identification:
            return identification.json()
        return {'message': 'ID not found'}, 404

    def post(self, _id):
        if ClimateModel.find_by_id(_id):
            return {'message': "An item with this id '{}' already exists.".format(_id)}, 400

        data = Climate.parser.parse_args()

        identification = ClimateModel(_id, **data)

        try:
            identification.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return identification.json(), 201


    @jwt_required()
    def delete(self, _id):
        deletion = ClimateModel.find_by_id(_id)
        if deletion:
            deletion.delete_from_db()

        return {'message': 'Item deleted'}

class ClimateList(Resource):

    def get(self):
        return {'climate': [_id.json() for _id in ClimateModel.query.all()]}

class ClimatePredict(Resource):
    def get(self):
        rainfall_avg = db.session.query(func.avg(ClimateModel.rainfall)).scalar()
        temperature_avg = db.session.query(func.avg(ClimateModel.temperature)).scalar()

        return {'Average rainfal for today': rainfall_avg, 'Average temperature for today': temperature_avg}
