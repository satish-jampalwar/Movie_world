from flask import Flask, request, jsonify
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import Movie, Persons, User, db

# Initialize Flask and SQLAlchemy
app = Flask(__name__)


# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/satishj/Music/PythonAssignment/MovieWorld/movieworld.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# JWT secret key for authentication
app.config['JWT_SECRET_KEY'] = "MOVIE##WORLD@@**123"
jwt = JWTManager(app)

# Loading users data from a local JSON file
with open('users.json') as f:
    users = json.load(f)

# login api to check available users from db


@app.route('/login', methods=['POST'])
def login():
    params = request.json

    authenticated_users = User.query.filter(
        (User.email == params['email']) & (User.password == params['password'])).one_or_none()
    print('showing user from match...')
    if authenticated_users is not None:
        # generate request token for authenticated users
        access_token = create_access_token(identity=params['email'])
        return jsonify({"status": True, "message": "Login Success", "token": access_token}), 200

    return jsonify({"status": False, "message": "Authentication Failed"}), 401


# Get movies list with search params
@app.route('/getmovies')
@jwt_required()
def getMovies():
    params = request.args
    filter_query = Movie.query

    if "genre" in params:
        filter_query = filter_query.filter(
            Movie.genres.contains(params["genre"].lower()))
    if "year" in params:
        filter_query = filter_query.filter(Movie.startYear == params["year"])
    if "type" in params:
        filter_query = filter_query.filter(
            Movie.titleType == params["type"].lower())

    # querying with filters above to get one or more records

    movies = filter_query.all()

    # serialize data before sending response
    return jsonify({
        "status": True,
        "message": "Movies Fetched successfully",
        "data": [movie.serialize() for movie in movies],
        "count": len(movies)
    })

# Get user list by params


@app.route('/getusers')
@jwt_required()
def getUsers():
    params = request.args
    query = Persons.query

    if "movie" in params:
        query = query.filter(
            Persons.knownForTitles.contains(params["movie"].lower()))
    if "profession" in params:
        query = query.filter(Persons.primaryProfession.contains(
            params["profession"].lower()))

    # querying with filters above to get one or more records
    persons = query.all()

    # serialize data before sending response
    return jsonify({
        "status": True,
        "message": "Users Fetched successfully",
        "data": [person.serialize() for person in persons],
        "total": len(persons)
    })


# showing list of all available users
@app.route('/getAllUsers')
@jwt_required()
def getAllUsers():
    users = User.query.all()
    return jsonify({
        "status": True,
        "message": "Users Fetched successfully",
        "data": [user.serialize() for user in users],
        "total": len(users)
    })


# Home route
@app.route('/')
def home():
    return 'Running flask home!'


# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
