from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    user_intakes = db.relationship('UserIntake', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_intakes": list(map(lambda x: x.serialize(), self.user_intakes))

            # do not serialize the password, its a security breach
        }

class UserIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(250), unique=False, nullable=False)
    nf_calories = db.Column(db.String(250), unique=False, nullable=False)
    nf_calories_from_fat = db.Column(db.String(250), unique=False, nullable=False)
    nf_protein = db.Column(db.String(250), unique=False, nullable=False)
    nf_saturated_fats = db.Column(db.String(250), unique=False, nullable=False)
    nf_sugars = db.Column(db.String(250), unique=False, nullable=False)
    nf_sodium = db.Column(db.String(250), unique=False, nullable=False)
    nf_dietary_fiber = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
    nullable=False)
    

    def __repr__(self):
        return '<UserIntake %r>' % self.item_name

    def serialize(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "nf_calories": self.nf_calories,
            "nf_calories_from_fat": self.nf_calories_from_fat,
            "nf_protein": self.nf_protein,
            "nf_saturated_fats": self.nf_saturated_fats,
            "nf_sugars": self.nf_sugars,
            "nf_sodium": self.nf_sodium,
            "nf_dietary_fiber": self.nf_dietary_fiber
            # do not serialize the password, its a security breach
        }