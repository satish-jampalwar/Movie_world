from flask_sqlalchemy import SQLAlchemy

# initialize sqlalchemy instance
db = SQLAlchemy()

# Movie model


class Movie(db.Model):
    __tablename__ = 'movies'

    tconst = db.Column(db.Text, primary_key=True)
    titleType = db.Column(db.Text)
    primaryTitle = db.Column(db.Text)
    originalTitle = db.Column(db.Text)
    isAdult = db.Column(db.Integer)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.Text)

    def serialize(self):
        return {
            'tconst': self.tconst,
            'titleType': self.titleType,
            'primaryTitle': self.primaryTitle,
            'originalTitle': self.originalTitle,
            'isAdult': self.isAdult,
            'startYear': self.startYear,
            'endYear': self.endYear,
            'runtimeMinutes': self.runtimeMinutes,
            'genres': self.genres
        }

# Persons model


class Persons(db.Model):
    __tablename__ = 'persons'

    nconst = db.Column(db.Text, primary_key=True)
    primaryName = db.Column(db.Text)
    birthYear = db.Column(db.Integer)
    deathYear = db.Column(db.Integer)
    primaryProfession = db.Column(db.String)
    knownForTitles = db.Column(db.String)

    def serialize(self):
        return {
            'nconst': self.nconst,
            'primaryName': self.primaryName,
            'birthYear': self.birthYear,
            'deathYear': self.deathYear,
            'primaryProfession': self.primaryProfession,
            'knownForTitles': self.knownForTitles
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


# end of models
