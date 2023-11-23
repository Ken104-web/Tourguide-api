from flask_restx import Resource, Namespace
from .models import User
from .extensions import db, api
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required 
from .api_models import req_signup_model,update_profile_model, profile_details_model,search_model
from api_keys import api_key
sign_ns = Namespace("sign", description="handle search")
search_ns = Namespace('search', description="search for destinations")
import requests

@sign_ns.route('')
class SignIn(Resource):
    @sign_ns.expect(req_signup_model)
    def post(self):

        sign_data = sign_ns.payload

        username = sign_data['username']
        email = sign_data['email']
        password = sign_data['password']
        # confirm_password = sign_data['confirm password']

        user = User.query.filter_by(email = sign_data['email']).first()

        if not user:
            new_user = User(username=username, email=email, password_hash = password)
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.id)
            return {"message": "User registered successfully",
                    'access_token': access_token 
                }, 201
        else:
            return {'message': 'User already exists .'}, 422
         
    @jwt_required()
    @sign_ns.expect()
    @sign_ns.marshal_with(update_profile_model)
    def put(self):

        user_details = get_jwt_identity()
        user = User.query.filter_by(id = user_details["id"]).first()
        
        user.username = sign_ns.payload["username"]
        user.password_hash = sign_ns.payload["password"]
        db.session.commit()
        return user
    
    @jwt_required()
    def delete(self):
        user_details = get_jwt_identity()
        user_id = user_details.get('id')

        user = User.query.filter_by(id = user_id).first()

        if not user:
            return {"message": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {}, 204
search_ns.route('')
class Search(Resource):

    @jwt_required(optional=True)
    @search_ns.expect(search_model)
    def get(self):
        query = ['query']
        destination = get_activity(query)

        return destination, 200
def get_activity(query):
    url = f"https://travel-info-api.p.rapidapi.com/country-activities?country={query}"

    headers = {
        "X-RapidAPI-Key": api_key,
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    results = []
    try:
        for i in data:
            title = i['title']
            activity = i['activity']
            results.append({"destination": title, "activity":activity})
    except KeyError:
        if r.status_code == 429 or int(r.status_code) == 429:
            print (data)
            print('(tour_api) - Rate limit exceeded')
        else:
                print("(tour_api) -  Error while processing your query")
    return results








    