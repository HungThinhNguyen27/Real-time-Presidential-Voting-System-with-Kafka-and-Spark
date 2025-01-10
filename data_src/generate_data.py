import random
import requests
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import RẠNDOMUSER_URL

PARTIES = ["Republican", "Democratic"]
random.seed(42)

trump_data = {
    "login": {"uuid": uuid.uuid4()},
    "name": {"first": "Donald", "last": "Trump"},
    "party_affiliation": PARTIES[0],
    "picture": {"large": "https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg"},
    "biography": "Donald Trump served as the 45th President of the United States.",
    "campaign_platform": "Make America Great Again."
}

harris_data = {
    "login": {"uuid": uuid.uuid4()},
    "name": {"first": "Kamala", "last": "Harris"},
    "party_affiliation": PARTIES[1],
    "picture": {"large": "https://www.whitehouse.gov/wp-content/uploads/2021/04/V20210305LJ-0043-cropped.jpg"},
    "biography": "Kamala Harris is the Vice President of the United States and the first female VP.",
    "campaign_platform": "Building a better future for all Americans."
}

def generate_voter_data():
    response = requests.get(RẠNDOMUSER_URL)
    if response.status_code == 200:
        user_data = response.json()['results'][0]
        return {
            "voter_id": user_data['login']['uuid'],
            "voter_name": f"{user_data['name']['first']} {user_data['name']['last']}",
            "date_of_birth": user_data['dob']['date'],
            "age": user_data['dob']['age'],  
            "gender": user_data['gender'],
            "nationality": user_data['nat'],
            "registration_number": user_data['login']['username'],
            "address": {
                "street": f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}",
                "city": user_data['location']['city'],
                "state": user_data['location']['state'],
                "country": user_data['location']['country'],
                "postcode": user_data['location']['postcode']
            },
            "email": user_data['email'],
            "phone_number": user_data['phone'],
            "cell_number": user_data['cell'],
            "picture": user_data['picture']['large'],
            "registered_age": user_data['registered']['age']
        }
    else:
        return "Error fetching data"


def create_candidate_data(user_data):
    return {
        "candidate_id": str(user_data['login']['uuid']),
        "candidate_name": f"{user_data['name']['first']} {user_data['name']['last']}",
        "party_affiliation": user_data['party_affiliation'],
        "biography": user_data.get('biography', "A brief bio of the candidate."),
        "campaign_platform": user_data.get('campaign_platform', "Key campaign promises or platform."),
        "photo_url": user_data['picture']['large']
    }


    
# print(create_candidate_data(trump_data))
# print(create_candidate_data(harris_data))
# print(generate_voter_data())

