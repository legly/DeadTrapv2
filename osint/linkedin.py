import requests
from bs4 import BeautifulSoup

def linkedin(area, ctr = 0):
    while ctr < 150:
        query = 'https://google.com/search?q=site:linkedin.com/in+AND+"{}"&start='.format(area) +str(ctr)
        profile_urls = []
        response = requests.get(query)
        soup = BeautifulSoup(response.text,'html.parser')
        for anchor in soup.find_all('a'):
            url = anchor["href"]
            if 'https://www.linkedin.com/' in url:
                url = url[7:url.find('&')]
                profile_urls.append([url])
                print("[+] Possible linkedin accounts based on geolocations :", url)
        ctr += 10