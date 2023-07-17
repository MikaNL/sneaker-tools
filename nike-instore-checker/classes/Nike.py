import requests, datetime
from .UserAgent import UserAgent

class Nike:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en;q=0.9',
            'dnt': '1',
            'origin': 'https://www.nike.com',
            'referer': 'https://www.nike.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent.get(),
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }

    def convertTimestamp(self, datestring):
        datestring = datestring.replace('T', ' ')
        datestring = datestring.replace('Z', '')
        datestring = datestring.replace('.000', '')
        date = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        return f"<t:{int(date.timestamp())}:R>"

    def formatCoordinates(self, longitude, latitude):
        if '.' in longitude and '.' in latitude:
            longitude = longitude[:longitude.index('.') + 3]
            latitude = latitude[:latitude.index('.') + 3]
        return longitude, latitude

    def getStoreDetails(self, longitude, latitude, max_distance):
        longitude, latitude = self.formatCoordinates(longitude, latitude)
        url = f"https://api.nike.com/store/store_locations/v1?language=nl-NL&search=%28%28%28brand%3D%3DNIKE%20and%20facilityType%3D%3DNIKE_OWNED_STORE%20or%20facilityType%3D%3DFRANCHISEE_PARTNER_STORE%20or%20facilityType%3D%3DMONO_BRAND_NON_FRANCHISEE_PARTNER_STORE%20and%20%28region%21%3DGREATER_CHINA%29%29%20and%20%28businessConcept%21%3DEMPLOYEE_STORE%20and%20businessConcept%21%3DBRAND_POP_UP%29%29%20and%20%28coordinates%3DgeoProximity%3D%7B%22maxDistance%22%3A%20{max_distance}%2C%20%22measurementUnits%22%3A%20%22km%22%2C%22latitude%22%3A%20{latitude}%2C%20%22longitude%22%3A%20{longitude}%7D%29%29"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        if len(data['objects']) == 0:
            return None
        stores = []
        for store in data['objects']:
            stores.append([store['id'], store['name'], store['address']['country'], f"https://www.nike.com/nl/retail/s/{store['slug']}"])
        return stores
    
    def getAvailability(self, store_id, pid):
        url = f"https://api.nike.com/deliver/available_gtins/v3?filter=styleColor({pid})&filter=storeId({store_id})&filter=method(INSTORE)"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        data = response.json()
        if len(data['objects']) == 0:
            return None
        sizes = []
        for availability in data['objects']:
            sizes.append([availability['gtin'], availability['level'], self.convertTimestamp(availability['modificationDate'])])
        return sizes
    
    def getProductDetails(self, pid):
        url = f"https://api.nike.com/product_feed/threads/v2?filter=language(nl)&filter=marketplace(NL)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({pid})"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        product = data['objects'][0]
        slug = f"https://nike.com/nl/t/{product['publishedContent']['properties']['seo']['slug']}/{pid.upper()}"
        image = product['productInfo'][0]['imageUrls']['productImageUrl']
        name = f"{product['productInfo'][0]['productContent']['title']} {product['productInfo'][0]['productContent']['colorDescription']}"
        return name, slug, image

    def getSize(self, gtin, pid):
        url = f"https://api.nike.com/product_feed/threads/v2?filter=language(nl)&filter=marketplace(NL)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({pid})"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        product = data['objects'][0]
        for size in product['productInfo'][0]['skus']:
            if size['gtin'] == gtin:
                return size['countrySpecifications'][0]['localizedSize']
            
    def getFooterLinks(self, pid):
        pid = pid.upper()
        stockX = f"[StockX](https://stockx.com/search?s={pid})"
        goat = f"[GOAT](https://www.goat.com/search?query={pid})"
        nikeApp = f"[Nike App](http://atc.yeet.ai/redirect?link=mynike://x-callback-url/product-details?style-color={pid}&redirect=true&platform=ios%60)"
        snkrs = f"[SNKRS](http://atc.yeet.ai/redirect?link=SNKRS://product/{pid})"
        return " | ".join([nikeApp, snkrs, stockX, goat])