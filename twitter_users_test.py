from projects.twitter_api.core import User

def main():
    username = "paaabloo13"
    params = "name,id,verified,username,description,url,profile_image_url"
    pablo = User(username=username)
    print(pablo.get_user_data(params))


if __name__ == "__main__":
    main()