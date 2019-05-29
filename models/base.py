from db import db

from utilities import convert_column_to_string


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create_from_dict(cls, dictionary):
        return cls(**dictionary)

    def to_dict(self, cls):
        dictionary = {
            convert_column_to_string(column): getattr(self, convert_column_to_string(column))
            for column in cls.__table__.columns
        }
        return dictionary

    def update_from_dict(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
