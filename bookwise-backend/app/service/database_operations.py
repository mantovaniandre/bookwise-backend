from service.database import db


class DatabaseOperations:
    def add(self):
        db.session.add(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()
