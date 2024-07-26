#import os
#from URLDecoder.decoder import URLDecoder
import time
import json
import requests
from urllib.parse import parse_qs

# function to convert x-www.form-urlencoded to json
# def convertUrlencode(url_encoded_string):
#     decoder = URLDecoder()
#     dict_object = decoder.to_dict(url_encoded_string)
#     print('dict_object:', dict_object)


# def main(params):
#   convertUrlencode(params)

#   return {
#         "headers": {
#             "Content-Type": "application/json",
#         },
#         "statusCode": 200,
#         "body": params,
#   }


def create_cpd_token_40(iamURL, username, password):
    data = json.dumps({"username": username, "password": password}).encode("utf-8")
    url = "{}/icp4d-api/v1/authorize".format(iamURL)
    headers = {}
    headers["content-type"] = "application/json"
    #headers["charset"] = "UTF-8"
    iamToken = None
    response = None
    # print("data: " + data)
    for i in range(10):
        try:
            response = requests.post(url, headers=headers, data=data, verify=False)
            # print(json.dumps(response.json(), indent=2))
            return response.json()["token"]
        except:
            print("Failed to get CP4D IAM Token, retrying {}/10 times..., response code={}".format((i+1), response.status_code))
            time.sleep(5)

    # The second pass.
    # url = "{}/v1/preauth/validateAuth".format(platformURL)
    # headers = {}
    # headers["username"] = username
    # headers["iam-token"] = iamToken

    # for i in range(10):
    #     try:
    #         response = requests.get(url, headers=headers, verify=False)
    #         return response.json()["token"]
    #     except:
    #         print("Failed to get CP4D Token, retrying {}/10 times..., response code={}".format((i+1), response.status_code))
    #         time.sleep(5)

def main(params):
#   convertUrlencode(params)
#   print("body")
  body = params["__ce_body"]
#   print(body)
  body_json = {x.split('=')[0]:(x.split('=')[1]) for x in body.split("&")}
#   print("parsed")
  username = body_json["username"]
  password = body_json["password"]
  url = "https://cpd-cpd.apps.mah-us-east-cpd485-01.dataandaidemo.com"
  access_token = create_cpd_token_40(iamURL=url, username=username, password=password)

  return {
        "headers": {
            "Content-Type": "application/json",
            "statusCode": 200
        },
        "body": {
            "access_token": access_token,
            "expires": 3600
        }
  }
