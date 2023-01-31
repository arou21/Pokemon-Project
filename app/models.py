from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

# create models from out ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_name =  db.Column(db.String(45), nullable=True)
    battle_points = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    # post = db.relationship("Post", backref='author', lazy=True)

    def __init__(self, first_name, last_name, user_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_name = user_name
        self.password = password
        
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Pokemon_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    base_experince = db.Column(db.Integer, nullable=False, unique=True)
    ability = db.Column(db.String(45), nullable=False, unique=True)
    health = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    # post = db.relationship("Post", backref='author', lazy=True)

    def __init__(self, name, base_experince, ability, health, attack, defense):
        self.name = name
        self.base_experince = base_experince
        self.health = health
        self.attack = attack
        self.defense = defense
        self.ability = ability

    def saveToDB(self):
        exists = Pokemon_table.query.filter_by(name=self.name).first()
        if not exists:
            db.session.add(self)
            db.session.commit()

class caught_pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_type = db.Column(db.String(45), nullable=False, unique=False)
    user_id = db.Column(db.Integer, nullable=False, unique=False)
    shiny = db.Column(db.Boolean, nullable=False, unique=False)

    def __init__(self, pokemon_type, user_id, shiny):
        self.pokemon_type = pokemon_type
        self.user_id = user_id
        self.shiny = shiny

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    


        
#this can be removed
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     img_url = db.Column(db.String, nullable=False)
#     caption = db.Column(db.String(1000))
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __init__(self, first_name, last_name, email, password):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password = password

    # end of remove