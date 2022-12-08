from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace("auth")

@auth_ns.route("/register")
class RegisterView(Resource):
    def post(self):
        request_json = request.json
        email = request_json.get("email")
        password = request_json.get("password")

        if None in [email, password]:
            return "", 401

        request_json["favorite_genre"] = 1
        user_service.create(request_json)

        return "User created", 201



@auth_ns.route("/login")
class AuthView(Resource):
    def post(self):
        request_json = request.json
        email = request_json.get("email")
        password = request_json.get("password")

        if None in [email, password]:
            return "", 401

        tokens = auth_service.generate_token(email, password)
        return tokens, 201

    def put(self):
        request_json = request.json
        access_token = request_json.get('access_token')
        refresh_token = request_json.get('refresh_token')
        valid = auth_service.valid_token(access_token, refresh_token)
        if not valid:
            return "Invalid token", 400

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 201