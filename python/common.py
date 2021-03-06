import datetime, json, time
import mysql.connector as mariadb
from mysql.connector import errorcode
import urllib2

class common:

    #api links
    OV_API = 'https://api.9292.nl/0.1'
    Google_API = "http://maps.googleapis.com/maps/api/distancematrix/json?"
    Windesheim_API = "http://roosterplusprod.cloudapp.net/api/"

    Windesheim_API_cooldown = 10 #ensures x seconds between each API call, from this instance
    Last_Windesheim_API_call = 0

    #variables
    mariadb_connection = None
    cursor = None

    #database variables
    DB_Settings = {
        'user': 'smartAlarm',
        'password': '',
        'host': 'localhost',
        'database': 'WakeUp',
        'raise_on_warnings': True,
        'use_unicode': True,
        'charset': "utf8"
    }

    #location variables
    Windesheim_OV_location = "zwolle_hogeschool-windesheim-loc-campus"

    #creates database connection upon creation
    def __init__(self):
        self.connect_to_database()

    #updates the settings used to connect to the database
    def set_database_settings(self, settings):
        self.DB_Settings = settings
        self.connect_to_database()

    #returns the entire settings table from the database
    def get_settings(self):
        #checks if there is an database connection
        self.check_database_connection()
        #creates an sql string
        sql = "SELECT setting, value FROM settings"
        #executes the sql string
        err = self.execute_sql(sql)
        if err:
            return err
        #fetches the result from the sql
        val = self.cursor.fetchall()
        encoded = [[s.encode('utf8') for s in t] for t in val]
        result = {}

        for k,v in encoded:
            result[k] = v

        return result

    def check_database_connection(self):
        #checks of there is an database connection
        if self.mariadb_connection == None or self.cursor == None:
            self.connect_to_database()

    #gets the value of a setting from the database
    def get_setting_value(self, setting):
        self.check_database_connection()

        sql = "SELECT value FROM settings WHERE setting='%s'" % setting

        err = self.execute_sql(sql)
        if err:
            return err
        val = self.cursor.fetchone()

        return val[0].encode('utf8')

    #connects the common module to the database
    def connect_to_database(self):
        try:
            self.mariadb_connection = mariadb.connect(**self.DB_Settings)
        except mariadb.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return ("Error: {}".format(err))
        self.mariadb_connection.text_factory = str
        self.cursor = self.mariadb_connection.cursor(buffered=True)


    #gets the current les rooster for a klas
    def get_rooster(self, klas):
        t = time.time()
        #ensures that x seconds have passed since last api call
        if not t >= self.Last_Windesheim_API_call + self.Windesheim_API_cooldown:
            #if not wait till x secods have actually passed
            time.sleep(self.Last_Windesheim_API_call + self.Windesheim_API_cooldown - t)
        self.Last_Windesheim_API_call = time.time()
        return self.get_data(self.Windesheim_API + "Klas/%s/les" % klas)

    #gets json from a page, used for interacting with API's
    def get_data(self, link, **data):
        if data:
            #adds each data item to the end of the link as a query
            for k,v in data['data'].items():
                link += k + '=' + str(v) + "&"
            #removes the last '&' thats left over
            link = link[:-1]

        contents = urllib2.urlopen(link).read()
        #returns the result in JSON format
        js = json.loads(contents.decode('utf-8'))

        return js

    #gets the first lesson of a day
    def get_schoolStartTime(self, date):
        rooster = self.get_rooster(self.get_setting_value('klas'))
        todays_classes = []
        date = date.strftime("%Y-%m-%dT00:00:00Z")
        for l in rooster:
            #loop over all classes in semester
            if l['roosterdatum'] == date:
                #match all classes on the  day
                todays_classes.append(l)

        #order classes by date
        todays_classes = sorted(todays_classes, key=lambda lesson: lesson['starttijd'])
        #return earliest date
        if len(todays_classes) > 0:
            return todays_classes[0]['starttijd']
        #returns none if there are no classes on the day
        return None

    #get the time you have to leave for travel with OV
    def get_OV_departureTime(self):
        link = self.OV_API + "/journeys?"
        sett = self.get_settings()
        t = self.get_schoolStartTime(datetime.datetime.now())
        if not t:
            return None
        t = str(t)
        t = t[:-3]
        t = datetime.datetime.fromtimestamp(float(t)).strftime("%Y-%m-%dT%H%M")

        TravelSettings = {
            'before': 1,
            'sequence': 1,
            'byBus': sett['byBus'],
            'byFerry': sett['byFerry'],
            'bySubway': sett['bySubway'],
            'byTram': sett['byTram'],
            'byTrain': sett['byTrain'],
            'lang': 'nl-NL',
            'from': sett['woonplaats'],
            'dateTime': t, #get school start time for today
            'searchType': 'arrival',
            'interchangeTime': 'standard',
            'after': 5,
            'to': self.Windesheim_OV_location,
            'realtime': True
        }

        journey = self.get_data(link,data=TravelSettings)
        return journey['journeys'][0]['departure']

    #executes an SQL string, returns error if one occured else returns none
    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
        except mariadb.Error as err:
            return err
        return None

    #calculates the time the alarm has to trigger
    def get_alarmTime(self):
        Snooze = self.get_setting_value('snoozeBuffer')
        v = self.get_setting_value('vervoer')
        if v == 'OV':
            t = self.get_OV_departureTime() #- datetime.timedelta(minutes=int(Snooze))
            self.update_setting('alarmTijd',t) # adds the alarm time to the database
            return t

        #needs other functions to support google distancematrix

        return None

    #updates a setting in the database, creates a new field if it doesnt exist
    def update_setting(self, setting, value):
        sql = "UPDATE settings SET value='%s' WHERE setting='%s'" % (value, setting)
        #executes the sql
        err = self.execute_sql(sql)
        if err:
            #if there is an error it will return the error
            return err
        #else it returns none
        self.mariadb_connection.commit()
        return None

    def set_API_cooldown(self, cd):
        if cd < 2:
            cd = 2
        self.Windesheim_API_cooldown = cd

    def close_database_connection (self):
        self.cursor.close()
        self.mariadb_connection.close()
