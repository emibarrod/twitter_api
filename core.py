from ast import Raise
import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

BASE_URL = "https://api.twitter.com/2/"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r

def get_params(params):
    return {"user.fields": "{}".format(params)}

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print("Response status code: {}".format(response.status_code))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

class User:
    def __init__(self, username=None, user_id=None, url=None) -> None:
        self.url = url
        self.username = username
        self.user_id = user_id

    def get_user_url(self):

        if self.user_id:
            self.url = "{}users/{}".format(BASE_URL, self.user_id)
        elif self.username:
            self.url = "{}users/by/username/{}".format(BASE_URL, self.username)

        return self.url

    def get_username_id(self):

        params = get_params("id")
        url = "{}users/by/username/{}".format(BASE_URL, self.username)
        json_response = connect_to_endpoint(url, params)
        return json_response["data"]["id"]
    
    def get_user_data(self, params):

        if not self.url:
            self.get_user_url()
        if self.username:
            self.url = "{}users/by/username/{}".format(BASE_URL, self.username)
        elif self.user_id:
            self.url = "{}users/{}".format(BASE_URL, self.user_id)
        else:
            raise ValueError("None type object is not a valid user or username")

        params = get_params("{}".format(params))
        json_response = connect_to_endpoint(self.url, params)
        return json_response["data"]

class Follower:

    def __init__(self) -> None:
        self.url = None

    def create_followers_url(self, user):
        if user.username:
            user_id = user.get_username_id(user.username)
        self.url = "{}users/{}/followers".format(BASE_URL, user_id)
        return self.url