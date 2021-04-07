import datetime
import pytz

class dayntime:
    def __init__(self):
        self.zone = pytz.timezone("US/Eastern")

    def set_timezone(self,zone="Berlin"):
        #A function to set the timezones according to
        #  selected city
        if zone == "Chicago":
            self.zone = pytz.timezone("US/Eastern")
        elif zone == "Berlin":
            self.zone = pytz.timezone("Europe/Berlin")
        elif zone == "London":
            self.zone = pytz.timezone("Europe/London")
        elif zone == "Delhi":
            self.zone = pytz.timezone("Asia/Calcutta")
        elif zone == "Sydney":
            self.zone = pytz.timezone("Australia/Sydney")
            

    def getdate(self):
        #A function to return the current date according to
        #   the set time zone
        d = datetime.datetime.now()
        d_aware =  d.astimezone(self.zone)
        return d_aware.strftime("%B %d, %Y")


    def gettime(self):
        #A function to return the current time according to
        #   the set time zone
        d = datetime.datetime.now()
        d_aware =  d.astimezone(self.zone)
        return d_aware.strftime("%H : %M : %S")


