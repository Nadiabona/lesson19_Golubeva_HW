from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):

    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        request_json = request.json #получили запрос
        user = user_service.create(request_json)
        return '', 201, {"location": f"/users/{user.id}"}

@user_ns.route("/password")
class UpdateUserPasswordViews(Resource):
    def put(self):
        request_json = request.json
        email = request_json.get("email")
        old_password = request_json.get("password_1")
        new_password = request_json.get("password_1")

        user = user_service.get_by_email(email)

        if user_service.compare_password(user.password, old_password):
            user.password = user_service.make_password_hash(new_password)
            result = UserSchema().dump(user)
            user_service.update(result)

        else:
            print("Paswwword is not changed")

        return "", 201


@user_ns.route('/<int:rid>')
class UserView(Resource):
    def get(self, rid):
        r = user_service.get_one(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def patch(self, rid):
        request_json = request.json
        if "id" not in request_json:
            request_json["id"] = rid
        user_service.update(request_json)
        return "", 204

    def delete(self, rid):
        r = user_service.get_one(rid)
        user_service.delete(rid)
        return "", 204

