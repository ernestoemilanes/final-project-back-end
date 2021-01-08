from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }

class UserIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    item_name = db.Column(db.String(250), unique=False, nullable=False)
    nf_calories = db.Column(db.String(250), unique=False, nullable=False)
    nf_calories_from_fat = db.Column(db.String(250), unique=False, nullable=False)
    nf_protein = db.Column(db.String(250), unique=False, nullable=False)
    nf_fats = db.Column(db.String(250), unique=False, nullable=False)
    nf_saturated_fats = db.Column(db.String(250), unique=False, nullable=False)
    nf_sugars = db.Column(db.String(250), unique=False, nullable=False)
    nf_sodium = db.Column(db.String(250), unique=False, nullable=False)
    nf_dietary_fiber = db.Column(db.String(250), unique=False, nullable=False)
    

    def __repr__(self):
        return '<UserIntake %r>' % self.product_name

    def serialize(self):
        return {
            "id": self.id,
            "product_name": self.product_name
            # do not serialize the password, its a security breach
        }