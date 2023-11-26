from flask_restx import Resource, Namespace
from .models import User
from .extensions import db
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required 
from .api_models import req_signup_model,update_profile_model,req_search_model
from .api_keys import api_key
import requests


sign_ns = Namespace("sign", description="handle search")
search_ns = Namespace("search", description="search for destinations")


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
ns = Namespace("home")

@search_ns.route("")
class Search(Resource):
    @jwt_required(optional=True)
    @search_ns.expect(req_search_model)
    def post(self):
        query = request.json.get('query')
        destination = get_all_activities(query)
        return destination, 200

def get_activities(query):
 
    url = f"https://travel-info-api.p.rapidapi.com/country-activities?country={query}"

    headers = {
        "X-RapidAPI-Key": api_key,
    }
    r = requests.get(url, headers=headers)

    data = r.json()
    # print (data)
    results = []
    for i in data['data']['activities']:
        # print (i)
        title = i['title']
        activity = i['activity']
        results.append({"destination": title, "activity": activity})

    if r.status_code == 429:
            print('(tour_api) - Rate limit reached')
    else:
        print("(tour_api) -  Error while processing your query")
    return results

def get_images(query):
    url = f"https://travel-info-api.p.rapidapi.com/country?country={query}"
    
    headers = {
            "X-RapidAPI-Key": api_key,
        }
    r =requests.get(url, headers=headers)
    data = r.json()

    results = []
    for i in data['data']['country_images']:
        images = i['imageUrl']
        results.append({'images':images})
    if r.status_code == 429:        
        print('(tour_api) - Rate limit exceeded')
    else:  
        print("(tour_api) -  Error while processing your query")
    return results


def get_all_activities(query):
    activities = get_activities(query=query)
    images = get_images(query=query)
    results = activities + images
    id = 1 
    for result in results:
        result.update({"id": id})
        id += 1
    return results


    







   











    