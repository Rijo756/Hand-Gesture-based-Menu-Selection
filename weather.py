import requests, json


class weather_api:
    def __init__(self):
        #giving the details for the API call
        self.city = "Aachen"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.apikey = "3466d44537b6ecc032254062efd68bea"

        self.url = self.base_url + "appid=" + self.apikey + "&q="

    def get_temp(self,city = "Aachen"):
        #This function will get the city and return the temperature of the
        #   city after an api call
        self.city = city
        self.url = self.url + city
        
        #get method of requests module
        self.response = requests.get(self.url)

        #json object format data
        x = self.response.json()
        with open('data.txt', 'w') as outfile:
            json.dump(x, outfile)

        #check for error and return
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            temp = (int(current_temperature) - 273)
            return temp
        else:
            return "Could not get at the moment"

    def get_coordinates(self,city = "Aachen"):
        #This function will get the city and return the coordinates of the
        #   city after an api call
        self.city = city
        self.url = self.url + city
        
        #get method of requests module
        self.response = requests.get(self.url)

        #json object format data
        x = self.response.json()
        with open('data.txt', 'w') as outfile:
            json.dump(x, outfile)

        #check for the error and return
        if x["cod"] != "404":
            y = x["coord"]
            long = y["lon"]
            lat = y["lat"]
            cordinates = "Long:"+str(long) + " Lat:" + str(lat)
            return cordinates
        else:
            return "Could not get at the moment"

