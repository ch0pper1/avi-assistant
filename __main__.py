#import os
#from URLDecoder.decoder import URLDecoder
import base64
import time
import json
import re
import requests
import urllib.parse

def create_cpd_token_40(iamURL, username, password):
    data = json.dumps({"username": username, "password": password}).encode("utf-8")
    url = "{}/icp4d-api/v1/authorize".format(iamURL)
    headers = {}
    headers["content-type"] = "application/json"
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

def main(params):
  body = params["__ce_body"]
  # body_json = {x.split('=')[0]:(x.split('=')[1]) for x in body.split("&")}
  body_json = urllib.parse.parse_qs(body)
  #   print(body_json)
  username = body_json["username"][0]
  #   print(json.dumps(body_json["password"][0]))
  password = ""
  if (re.match(r'^(?:[A-Za-z0-9+/]{7})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)$', body_json["password"][0])):
    password = base64.b64decode(body_json["password"][0]).decode('ascii')
  else:
    password = body_json["password"][0]
  url = "https://cpd-cpd.apps.mah-us-east-cpd485-01.dataandaidemo.com"
  #   print(password)
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
