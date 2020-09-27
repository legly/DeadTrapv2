import requests
from bs4 import BeautifulSoup
import hashlib
import json
import sys

def api_generate():

    r = requests.get('https://numverify.com/')
    soup = BeautifulSoup(r.text, "html5lib")
    for tag in soup.find_all("input", type="hidden"):
        if tag['name'] == "scl_request_secret":
            secret = tag['value']
            break

    return secret

def numverifyScan(num, secret=api_generate()):

    api = hashlib.md5((num + secret).encode('utf-8')).hexdigest()

    print('\n[*] Running Numverify scan...\n')

    response = requests.get("https://numverify.com/php_helper_scripts/phone_api.php?secret_key={}&number={}".format(api, num))

    if response.content == "Unauthorized" or response.status_code != 200:
        print(( "[!] Unauthorized request"))

    numverifyScan.data = json.loads(response.content)

    if numverifyScan.data["valid"] == False:
        print(( "[!] Please specify a valid phone number. Example: +14158586273"))
        sys.exit()

    InternationalNumber = '({}){}'.format(numverifyScan.data["country_prefix"], numverifyScan.data["local_format"])

    print("Country Prefix: {}".format(numverifyScan.data["country_prefix"]))
    print("Number: {}".format(numverifyScan.data["local_format"]))
    print("Country: {}".format(numverifyScan.data["country_name"]))
    print("Country Code: {}".format(numverifyScan.data["country_code"]))
    print("Location: {}".format(numverifyScan.data["location"]))
    print("Carrier: {}".format(numverifyScan.data["carrier"]))
    print("Line type: {}".format(numverifyScan.data["line_type"]))