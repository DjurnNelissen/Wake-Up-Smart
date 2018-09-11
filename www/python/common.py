import datetime, json
import mysql.connector as mariadb
from mysql.connector import errorcode
import urllib2

class common:

    #api links
    OV_API = 'https://api.9292.nl/0.1'
    Google_API = "http://maps.googleapis.com/maps/api/distancematrix/json?"
    Windesheim_API = "http://roosterplusprod.cloudapp.net/api/"

    #variables
    mariadb_connection = None
    cursor = None

    #database variables
    DB_Settings = {
        'user': 'ghostwolf',
        'password': '',
        'host': 'localhost',
        'database': 'SenseHatData',
        'raise_on_warnings': True
    }

    #location variables
    Windesheim_OV_location = "zwolle_hogeschool-windesheim-loc-campus"

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
        return val

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
        self.cursor = self.mariadb_connection.cursor()


    #gets the current les rooster for a klas
    def get_rooster(self, klas):
        return self.get_data(self.Windesheim_API + "Klas/%s/les" % klas)

    #gets json from a page, used for interacting with API's
    def get_data(self, link, **data):
        if data:

            for k,v in data['data'].items():
                link += k + '=' + str(v) + "&"

            link = link[:-1]


        contents = urllib2.urlopen(link).read()
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
        if todays_classes[0]:
            return todays_classes[0]['starttijd']
        #returns none if there are no classes on the day
        return None

    #get the time you have to leave for travel with OV
    def get_OV_departureTime(self):
        link = self.OV_API + "/journeys?"
        sett = self.get_settings()
        t = self.get_schoolStartTime(datetime.datetime.now())
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
        OV_enabled = self.get_setting_value('OV')
        if OV_enabled:
            t = self.get_OV_departureTime() #- datetime.timedelta(minutes=int(Snooze))
            return t

    #updates a setting in the database, creates a new field if it doesnt exist
    def update_setting(setting, value):
        sql = "INSERT INTO settings (setting, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE " % (setting, value)
        #executes the sql
        err = self.execute_sql(sql)
        if err:
            #if there is an error it will return the error
            return err
        #else it returns none
        return None
