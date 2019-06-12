from app import db


class BaseModel(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).one_or_none()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_copy(self, copy):
        for key in self.__public__:
            value = getattr(copy, key)
            if value:
                setattr(self, key, value)
