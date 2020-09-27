import os
import requests
from bs4 import BeautifulSoup as soup
import sys
import re

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def twitter(num):
    session = requests.sessions.Session()
    req = session.get('https://twitter.com/account/begin_password_reset').text
    html = soup(req, features="html.parser")

    profiles = []

    token = html.find("input", {"name": "authenticity_token"}).get('value')

    response = session.post("https://twitter.com/account/begin_password_reset",
        data = {"authenticity_token": token, "account_identifier": num})

    if response.status_code == 200:
        if True:
            soups = soup(response.content.decode('utf-8'), 'html.parser')
            try:
                name = soups.findAll('strong')
                for names in name:
                    profiles.append(str(names))
                profiles.pop(0)
                name = remove_tags(",".join(profiles))
            except:
                pass

            print("[+] Found Twitter Users : ", len(profiles))

            if len(profiles) != 0:

                print("[+] Found Twitter email :", name)
            
            else:
                pass

        else:
            print("[!] No Twitter user is associated with " + num)