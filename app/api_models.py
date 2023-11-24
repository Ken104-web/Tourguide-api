from flask_restx import fields

from .extensions import api

req_signup_model = api.model("Sign in Request", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
    # "confirm password": fields.String
})
update_profile_model = api.model("User profile Updated", {
    "username": fields.String,
    "password":fields.String
})
profile_details_model = api.model("Profile Details", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
})

req_search_model = api.model("Search destination", {
    "query": fields.String
})
