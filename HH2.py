import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import datetime
import math
import numpy as np
from sympy import *


class ZillowScraper():
    soldResults = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'zguid=23|%24d14f0059-d03b-4422-9f57-5862fcd13490; _ga=GA1.2.1741285320.1590755697; zjs_user_id=null; zjs_anonymous_id=%22d14f0059-d03b-4422-9f57-5862fcd13490%22; __gads=ID=1050523ba93d593d:T=1590755700:S=ALNI_MZlJJ_xqSbd51oJisV_HY4g017Ehw; _gcl_au=1.1.2000298647.1590755705; KruxPixel=true; _fbp=fb.1.1590755705919.1815197270; _pxvid=d6c5ec75-a1a8-11ea-b8a9-0242ac120009; KruxAddition=true; JSESSIONID=3E7EBDB1F8931DF7D0DE9992546AE0B3; zgsession=1|200e23e0-9534-4d27-931f-caa3de6b483b; _gid=GA1.2.1328942480.1590858452; _gat=1; DoubleClickSession=true; GASession=true; _uetsid=fdde22d5-862a-8a7d-93e4-a16c574edf91; _pin_unauth=YzUyOGQ2OGMtMmQ3YS00NGZkLTg3MmEtOGJlODM1YWMwMTA1; _px3=026336d3721eec42bcdec3278ad2d3ac2014d5e65707b21624fb2e743d9a89be:mq3WRz2RNL5PBIvbYNHCxq5VfXHXy2YKC+8Lqn97pIw8MiKppH7Cx7AjKzbAFi1zcehKGY36aIgsnE9NiPKwlw==:1000:4U1o3ogIQ0KzfyMd2QYEFGDnD1augezy5bJlzEn9ZHE89B2uEIxDg8BmsGj8szPwyIz1Yv15S2V0TV5P+0jCFisfGk92XM4DM7K13GCtNr0HXhNGftVBFxVrCv8ApRphw/Qwj7AcagCh9i6FPiQGLFruxVASJXLsNpFeWimekVY=; AWSALB=ZKAGBcH2BwM6D1bRKOPynbOqyclySGz5U/fZB+wO3MYQ91UR9A5rFVtFsmjOkrMASUJguhtsJRZDM7IlBiWVT/pGw2S0BjxgEZmpFPrBZEqU2lWTE2NMArtecZD2; AWSALBCORS=ZKAGBcH2BwM6D1bRKOPynbOqyclySGz5U/fZB+wO3MYQ91UR9A5rFVtFsmjOkrMASUJguhtsJRZDM7IlBiWVT/pGw2S0BjxgEZmpFPrBZEqU2lWTE2NMArtecZD2; search=6|1593450465587%7Crect%3D40.843698984643765%252C-73.50417109960938%252C40.567821651427245%252C-74.45174190039063%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D0%26lt%3Dfsbo%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print('Successful read' if response.status_code == 200 else response.status_code)
        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        if deck is not None:
            for card in deck.contents:
                script = card.find('script', {'type': 'application/ld+json'})
                if script:
                    script_json = json.loads(script.contents[0])
                    #print(script_json)
                    try:
                        self.soldResults.append({
                            'latitude': script_json['geo']['latitude'],
                            'longitude': script_json['geo']['longitude'],
                            'floorSize': script_json['floorSize']['value'],
                            'url': script_json['url'],
                            'price': card.find('div', {'class': 'list-card-price'}).text,
                            'date' : time.mktime(datetime.datetime.strptime(card.find('div', {'list-card-variable-text list-card-img-overlay'}).text.replace("Sold ",""),"%m/%d/%Y").timetuple()),
                        })
                    except Exception as e:
                        print(e)
        else:
            print("DECK has no contents!")

    def sort(self):
        print('sort')
        #print(self.soldResults)
        n = len(self.soldResults)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.soldResults[j].get('latitude') > self.soldResults[j + 1].get('latitude'):
                    self.soldResults[j], self.soldResults[j + 1] = self.soldResults[j + 1], self.soldResults[j]
                elif self.soldResults[j].get('latitude') == self.soldResults[j + 1].get('latitude') and self.soldResults[j].get('longitude') > self.soldResults[j + 1].get('longitude'):
                    self.soldResults[j], self.soldResults[j + 1] = self.soldResults[j + 1], self.soldResults[j]

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.soldResults[0].keys())
            writer.writeheader()

            for row in self.soldResults:
                writer.writerow(row)

    def run(self):
        url = 'https://www.zillow.com/homes/Austin,-TX_rb/'

        for page in range(0, 21):
            params = {
                'searchQueryState':'{"pagination":{"currentPage": %s},"usersSearchTerm":"Austin, TX","mapBounds":{"west":-99.63965637109375,"east":-95.93177062890625,"south":29.663474938668408,"north":30.920371008240462},"mapZoom":8,"regionSelection":[{"regionId":10221,"regionType":6}],"isMapVisible":true,"filterState":{"price":{"min":1},"pmf":{"value":false},"fore":{"value":false},"ah":{"value":true},"sort":{"value":"globalrelevanceex"},"auc":{"value":false},"nc":{"value":false},"rs":{"value":true},"fsbo":{"value":false},"cmsn":{"value":false},"pf":{"value":false},"fsba":{"value":false}},"isListVisible":true}'% page
                #{"usersSearchTerm":
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        #print(self.soldResults)
        #self.sort()
        #print(self.soldResults)
        self.to_csv()

    def rescale(self,value,min,max):
        return (value-min)/(max-min)


    def dist_sort(self,long,lat,time):
        for r in self.soldResults:
            rLong = self.normalize_long(r.get('longitude'))
            rLat = self.normalize_lat(r.get('latitude'))
            rTime = self.normalize_time(r.get('date'))
            r['nLong'] = rLong
            r['nLat'] = rLat
            r['nTime'] = rTime
            # print('long: '+str(rLong))
            # print('lat: ' + str(rLat))
            # print('time: ' + str(rTime))
            # r['distance'] =math.sqrt((time - rTime)**2 + (lat - rLat)**2 +(long - rLong)**2)
            r['distance'] = math.sqrt((lat - rLat) ** 2 + (long - rLong) ** 2)
        self.soldResults.sort(key = get_dist)
        # for r in self.soldResults:
        #     print(r.get('distance'))

    def normalize(self, x, max, min):
        return (x - min)/(max -min)

    def normalize_long(self,long):
        return self.normalize(float(long),-95.93177062890625,-99.63965637109375)

    def normalize_lat(self,lat):
        return self.normalize(float(lat), 30.920371008240462, 29.663474938668408)

    def normalize_time(self,t):
        return self.normalize(float(t), time.mktime(datetime.date.today().timetuple()),
                           time.mktime((datetime.date.today() - datetime.timedelta(days=720)).timetuple()))

    def find_xyz(self, long, lat,time):
        # print(str(long)+" "+str(lat)+" "+str(time))
        p1 = self.convert_to_point(self.soldResults[0])
        #print(p1)
        p2 = self.convert_to_point(self.soldResults[1])
        #print(p2)
        p3 = self.convert_to_point(self.soldResults[2])
        #print(p3)

        l1 = self.create_line(p1,p2)
        #print(l1)
        l2 = self.create_line(p2, p3)
        #print(l2)
        l3 = self.create_line(p3, p1)
        #print(l3)

        l1['t']=(long - l1['x']) / l1['a']
        px1=self.find_point(l1,p1,p2)
        #print(px1)

        l2['t'] = (long - l2['x']) / l2['a']
        px2 = self.find_point(l2,p2,p3)
        #print(px2)

        l3['t'] = (long - l3['x']) / l3['a']
        px3 = self.find_point(l3,p3,p1)
        #print(px3)

        lx1 = self.create_line(px1, px2)
        #print(lx1)
        #lx2 = self.create_line(px2, px3)
        # print(lx2)
        #lx3 = self.create_line(px3, px1)
        # print(lx3)

        p = {}
        p['x'] = long
        p['y'] = lat
        p['z'] = time


        lp = self.create_line(px3, p)

        M_rref = self.line_intersection(lx1,lp)

        lx1['t'] = M_rref.col(-1)[0]
        print('p from lx1')
        pp = self.find_point(lx1,px1,px2)
        print('p from lp')
        p['value']=0
        lp['t'] = M_rref.col(-1)[1]
        pp2 = self.find_point(lp, px3, p)

        lp['t'] = (time - lp['z']) / lp['c']
        pFinal = self.find_point(lp,px3,pp)
        print(pFinal)

        return pFinal['value']

    def line_intersection(self,l1,l2):
        M = Matrix([[l1['a'], -l2['a'], l2['x']-l1['x']],
                           [l1['b'], -l2['b'], l2['y']-l1['y']],
                           [l1['c'], -l2['c'], l2['z']-l1['z']]])
        # print("Matrix : {} ".format(M))

        M_rref,M_pc = M.rref()

        # print("The Row echelon form of matrix M and the pivot columns : {}".format(M_rref))

        return M_rref

    def convert_to_point(self,r):
        p={}
        p['x'] = r['nLong']
        p['y'] = r['nLat']
        p['z'] = r['nTime']
        p['value'] = float(r['price'].strip('$').replace(',','').replace('M',''))
        # print(p)
        return p

    def find_point(self,l1,p1,p2):
        p = {}
        p['x'] = l1['x'] + l1['t'] * l1['a']
        p['y'] = l1['y'] + l1['t'] * l1['b']
        p['z'] = l1['z'] + l1['t'] * l1['c']
        p['value'] = p1['value'] + ((p1['value']-p2['value'])/self.getDist(p1,p2))*self.getDist(p1,p)
        # print(p)
        return p

    def create_line(self,p1,p2):
        l1 = {}
        l1['x'] = p1['x']
        l1['y'] = p1['y']
        l1['z'] = p1['z']
        l1['x2'] = p2['x']
        l1['y2'] = p2['y']
        l1['z2'] = p2['z']
        l1['a'] = l1['x2'] - l1['x']
        l1['b'] = l1['y2'] - l1['y']
        l1['c'] = l1['z2'] - l1['z']
        return l1

    def lineToP1(self,line):
        p = {}
        p['x'] = line['x']
        p['y'] = line['y']
        p['z'] = line['z']
        return p;
    def lineToP2(self,line):
        p = {}
        p['x'] = line['x2']
        p['y'] = line['y2']
        p['z'] = line['z2']
        return p;

    def getDistL(self,line):
        return math.sqrt((line['x'] - line['x2']) ** 2 + (line['y'] - line['y2']) ** 2 + (
            line['z'] - line['z2']) ** 2)

    def getDist(self,p1,p2):
        return math.sqrt((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2 + (
            p1['z'] - p2['z']) ** 2)

    # def create_plane(self):
    #     p0 = self.soldResults
    #     ux, uy, uz = u = [x1 - x0, y1 - y0, z1 - z0]
    #     vx, vy, vz = v = [x2 - x0, y2 - y0, z2 - z0]
    #     #create equation of plane, then create a lambda that outputs time value, return that,
    #     #use the lambda with location input (long, lat) use the resulting time value to create a point
    #     #calculate a distance between any point and the new point. use the distance to find the value of that location
    #     #create a line between this point and

    def getValue(self, long, lat, time):

        long = self.normalize_long(long)
        lat = self.normalize_lat(lat)
        time = self.normalize_time(time)

        self.dist_sort(long, lat, time);
        value = self.find_xyz(long, lat, time)
        # print()
        print(value)

def get_dist(elem):
    return elem.get('distance')

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()

    for i in range(1,13):
        print(str(i)+("/1/2020"))
        scraper.getValue(-97.690907,30.418700,time.mktime(datetime.datetime.strptime(str(i)+("/1/2020"),"%m/%d/%Y").timetuple()))
    # scraper.getValue(-97.690907,30.418700,time.mktime(datetime.datetime.strptime("5/1/2020","%m/%d/%Y").timetuple()))
