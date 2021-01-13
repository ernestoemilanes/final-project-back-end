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
    nf_total_fat = db.Column(db.String(250), unique=False, nullable=False)
    nf_trans_fatty_acid = db.Column(db.String(250), unique=False, nullable=False)
    nf_cholesterol = db.Column(db.String(250), unique=False, nullable=False)
    nf_vitamin_a_dv = db.Column(db.String(250), unique=False, nullable=False)
    nf_vitamin_c_dv = db.Column(db.String(250), unique=False, nullable=False)
    nf_calcium_dv = db.Column(db.String(250), unique=False, nullable=False)
    nf_iron_dv = db.Column(db.String(250), unique=False, nullable=False)
    nf_serving_size_unit = db.Column(db.String(250), unique=False, nullable=False)
    nf_serving_size_qty = db.Column(db.String(250), unique=False, nullable=False)
    nf_total_carbohydrate = db.Column(db.String(250), unique=False, nullable=False)
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
            "nf_dietary_fiber": self.nf_dietary_fiber,
            "nf_total_fat": self.nf_total_fat,
            'nf_trans_fatty_acid': self.nf_trans_fatty_acid,
            'nf_cholesterol': self.nf_cholesterol,
            'nf_vitamin_a_dv': self.nf_vitamin_a_dv,
            'nf_vitamin_c_dv' : self.nf_vitamin_c_dv,
            'nf_calcium_dv': self.nf_calcium_dv,
            'nf_iron_dv': self.nf_iron_dv,
            'nf_total_carbohydrate': self.nf_total_carbohydrate,
            #! still needs in frontend
            'nf_serving_size_unit': self.nf_serving_size_unit,
            'nf_serving_size_qty': self.nf_serving_size_qty
            # do not serialize the password, its a security breach
        }