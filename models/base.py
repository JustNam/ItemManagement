from datetime import datetime

from db import db


class BaseModel(db.Model):
    __abstract__ = True
    __public__ = []

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).one_or_none()

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

    def to_dict(self, relations=[]):
        dict = {}
        for key in self.__public__:
            value = getattr(self, key)
            if value:
                if type(value) is datetime:
                    value = value.strftime("%m/%d/%Y, %H:%M:%S")
                dict[key] = value
        for relation in relations:
            value = getattr(self, relation)
            if value:
                dict[relation] = value.to_dict()

        return dict

    def update_from_dict(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

    def update_from_copy(self, copy):
        for key in self.__public__:
            value = getattr(copy, key)
            if value:
                setattr(self, key, value)
