import requests, json

class Geocode:
    def __init__(self, address):
        self.address = address
        self.url = 'https://geocode.maps.co/search?q=' + self.quoteAddress()

    def quoteAddress(self):
        self.address = self.address.replace(' ', '%20')
        return self.address
    
    def getCoordinates(self):
        response = requests.get(self.url)
        data = response.json()
        if len(data) == 0:
            return None, None
        longitude = data[0]['lon']
        latitude = data[0]['lat']
        return longitude, latitude