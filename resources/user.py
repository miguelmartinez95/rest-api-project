from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema, UserRegisterSchema
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

import os
import requests
from db import db
from blocklist import BLOCKLIST
from models import UserModel

from dotenv import load_dotenv

blp = Blueprint("Users", __name__, description="Operations on users")

#Send emails MAILGUN
def send_simple_message(to, subject, body):
    #load_dotenv()
    domain = os.getenv("MAILGUN_DOMAIN")
	
    return requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"Mike <mailgun@{domain}>",
			"to": [to],
			"subject": subject,
			"text": body})


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):

        user = UserModel(
            username = user_data["username"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Problem creating the user. Is already defined?")

        send_simple_message(
            to=user.email,
            subject="Successfully signed up",
            body=f"Hi {user.username}! You have signed up to the Stores REST API"
        )

        return {"message": "User created successfully"},201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username==user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)

            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            abort(401, message="Inalvid credentials")

    
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # we can here think how much time the refresh token is valid. We can add it to the blocklist once is created (allowing only one use)
        return {"access_token": new_token}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

    
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}