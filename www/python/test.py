import datetime, urllib2, json

class test:

    Windesheim_API = "http://roosterplusprod.cloudapp.net/api/"


    #gets the first lesson of a day
    def get_schoolStartTime(self, date):
        rooster = self.get_rooster('ICTM1g')
        todays_classes = []

        for l in rooster:
            #loop over all classes in semester
            if l['roosterdatum'] == date:
                #match all classes on the  day
                todays_classes.append(l)

        #order classes by date
        todays_classes = sorted(todays_classes, key=lambda lesson: lesson['starttijd'])
        #return earliest date
        if len(todays_classes[0]) > 0:
            return todays_classes[0]['starttijd']

        #returns none if there are no classes on the day
        return None

        #gets the current les rooster for a klas
    def get_rooster(self, klas):
        return self.get_data(self.Windesheim_API + "Klas/%s/les" % klas)

        #gets json from a page, used for interacting with API's
    def get_data(self, link, *data):
            if data:
                for k,v in data.items():
                    link += k + '=' + str(v) + "&"

                link = link[:-1]


            contents = urllib2.urlopen(link).read()
            js = json.loads(contents.decode('utf-8'))

            return js

t = test()
print(t.get_schoolStartTime(datetime.datetime.now().strftime("%Y-%m-%dT00:00:00Z")))
