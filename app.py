from flask import Flask, request, jsonify
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = "MOVIE##WORLD@@**123"
jwt = JWTManager(app)

with open('users.json') as f:
    users = json.load(f)

with open('movies.json') as f:
    movies = json.load(f)

with open('persons.json') as f:
    persons = json.load(f)


@app.route('/login', methods=['POST'])
def login():
    params = request.json

    validUser = next(
        (user for user in users if user['email'] == params['username']), None)
    if validUser and params['password'] == validUser['password']:
        access_token = create_access_token(
            identity=params['username'])
        return jsonify({"status": True, "message": "Login Success", "toekn": access_token}), 200

    return jsonify({"status": False, "message": "Authentication Failed"}), 401


# get movies list by search params
@app.route('/getmovies')
@jwt_required()
def getMovies():
    params = request.args
    movies_filtered = movies
    if "genre" in params:
        print('genre is on')
        movies_filtered = [
            movie for movie in movies_filtered if movie['genre'] == params['genre']]
    if "year" in params:
        print('year is on')
        movies_filtered = [
            movie for movie in movies_filtered if movie['year'] == params['year']]
    if "type" in params:
        print('type is on')
        movies_filtered = [
            movie for movie in movies_filtered if movie['type'] == params['type']]

    return jsonify({"status": True, "message": "Movies Fetched with success", "data": movies_filtered, })


# get user list by params
@app.route('/getusers')
@jwt_required()
def getUsers():
    params = request.args
    person_filtered = persons
    if "movie" in params:
        print('movie is on')
        person_filtered = [
            movie for movie in person_filtered if movie['movie'] == params['movie']]
    if "profession" in params:
        print('profession is on')
        person_filtered = [
            movie for movie in person_filtered if movie['profession'] == params['profession']]

    return jsonify({"status": True, "message": "Users API Called with success", "data": person_filtered, })


@app.route('/')
def home():
    return 'Running flask home!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
