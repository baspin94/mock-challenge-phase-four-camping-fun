from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", backref=("camper"))

    @validates("age")
    def validate_age(self, key, age):
        if not 8 <= age <= 18:
            raise ValueError("Age must be between 8 and 18")
        return age


    def __repr__(self):
        return f"ID: {self.id} Name: {self.name} Age: {self.age}"



class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", backref=("activity"))

    def __repr__(self):
        return f"Name: {self.name} Difficulty: {self.difficulty}"



class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f"Time: {self.time} Camper ID: {self.camper_id} Activity ID: {self.activity_id}"


    @validates("time")
    def validate_time(self, key, time):
        if time not in range(24):
            raise ValueError("Time must be between 0 and 23")
        return time





