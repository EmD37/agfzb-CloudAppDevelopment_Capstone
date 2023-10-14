import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time


def get_request(url, **kwargs):  
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc['state'],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    if json_result:
        dealer_doc = json_result[0]
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            state=dealer_doc["state"],
            zip=dealer_doc["zip"]
        )
    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)

    if json_result:
        for review in json_result:
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'],
                                        review=review['review'], purchase_date=review['purchase_date'],
                                        car_make=review['car_make'], car_model=review['car_model'],
                                        car_year=review['car_year'], id=review['id'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

def analyze_review_sentiments(dealerReview):
    api_key = "c7yBI6Of-SgUFtLpSduWHMxmDl-qRoRdVLbBPUGE6G9g"
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/e0c16288-89eb-48a6-a03e-822abd34b9ec"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2023-10-14',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerReview + 'hello hello hello',features=Features(sentiment=SentimentOptions(targets=[dealerReview + 'hello hello hello']))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return label
