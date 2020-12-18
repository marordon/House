import requests
import pprint
from bs4 import BeautifulSoup

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
    url = 'https://www.zillow.com/homes/78727_rb/'
    r = s.get(url, headers=req_headers)

soup = BeautifulSoup(r.text, 'lxml')


print(soup.contents)

# prices = soup.find_all('section', class_='list-card-price')
# print(prices)
# for price in prices:
#     print(price, end='\n'*2)
price = soup.find('span', {'class': 'zsg-photo-card-price'}).text
info = soup.find('span', {'class': 'zsg-photo-card-info'}).text
address = soup.find('span', {'itemprop': 'address'}).text

print(price)

