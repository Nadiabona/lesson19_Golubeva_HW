from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from decorators import auth_required, admin_required
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    #@auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        status = request.args.get("status")
        page = request.args.get("page")

        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status":status,
            "page": page
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    #@admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:rid>')
class MovieView(Resource):
    #@auth_required
    def get(self, rid):
        b = movie_service.get_one(rid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    #@admin_required
    def put(self, rid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        movie_service.update(req_json)
        return "", 204

    #@admin_required
    def delete(self, rid):
        movie_service.delete(rid)
        return "", 204
