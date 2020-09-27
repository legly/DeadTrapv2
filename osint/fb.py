import os
import requests
from PIL import Image
from bs4 import BeautifulSoup
import sys
import re

def image(name, email_or_num, soup, img_link = False):

    img_links = soup.findAll('img')

    for i in img_links:

        if "profile" in i['src']:
            img_link = i['src'][:-2]+"500"

        if not os.path.isdir('recent_search'):
            os.mkdir('recent_search')

    img_path = "recent_search/" + \
    name.replace(' ', '-')+"__"+email_or_num+"_.jpg"

    img_data = requests.get(img_link).content if (img_link != False) else 0

    if img_data != 0:
        img = open(img_path, mode="wb")
        img.write(img_data)
        img.close()
        print("Profile image Saved in : ", img_path)

def emails(soup):
    try:
        emails = soup.findAll('div', {'class':'bi bj'})

        if len(emails) != 0:

            print("Found user emails or numbers :")

            for i in emails:

                print('\t\t'+i.text)

    except Exception as err:
        print(err)

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def is_valid(num):
    URL = "https://mbasic.facebook.com/login/identify/?ctx=recover" 
    payload = {'email': num, 'did_submit': 'Search'}
    profiles = []

    req = requests.post(URL, data=payload)
    if req.status_code == 200:

        if True:
            soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
            try:
                name = soup.findAll('strong')
                for names in name:
                    profiles.append(str(names))
                name = remove_tags(",".join(profiles))
            except IndexError:
                try:
                    name = soup.findAll('div', {'class': 'p v w'})
                    for names in name:
                        profiles.append(str(names))
                    name = remove_tags(",".join(profiles))
                except:
                    sys.exit()
            
            image(name, num, soup)

            print("[+] Found Facebook Users : ", len(profiles))

            if len(profiles) != 0:

                print("[+] Found Facebook Usernames:", name)
                emails(soup)
            else:
                pass
        else:
            print("[!] No Facebook user is associated with " + num)
    else:
        print("Check your internet Connection")
