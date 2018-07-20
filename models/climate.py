from db import db
import datetime

class ClimateModel(db.Model):
    __tablename__ = 'climate'

    _id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(40))
    rainfall = db.Column(db.Integer)
    temperature = db.Column(db.Integer)

    def __init__(self, _id, date, rainfall, temperature):
        self._id = _id
        self.date = date
        self.rainfall = rainfall
        self.temperature = temperature

    def json(self):
        return {'_id': self._id, 'date': self.date, 'rainfall': self.rainfall, 'temperature': self.temperature}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
