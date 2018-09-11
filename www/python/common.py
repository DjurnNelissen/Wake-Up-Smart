import datetime, json
import mysql.connector as mariadb
import urllib.request

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
        'database': 'SmartWake'
        'raise_on_warnings': True
    }

    #location variables
    Windesheim_OV_location = "zwolle_hogeschool-windesheim-loc-campus"

    #updates the settings used to connect to the database
    def set_database_settings(self, settings):
        self.DB_Settings = settings
        self.connect_to_database()

    #returns the entire settings table from the database
    def get_settings(self):
        #checks if there is an database connection
        if not self.mariadb_connection or not self.cursor:
            #if not  it creates a database connection
            self.connect_to_database()
        #creates an sql string
        sql = "SELECT * FROM settings"
        #executes the sql string
        err = self.execute_sql(sql)
        if err:
            return err
        #fetches the result from the sql
        val = self.cursor.fetchall()
        return val

    #gets the value of a setting from the database
    def get_setting_value(self, setting):
        #checks of there is an database connection
        if not self.mariadb_connection or not self.cursor:
            self.connect_to_database()

        sql = "SELECT value FROM settings WHERE setting=%s" % setting
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
                return ("Error: {}".format(err)

        self.cursor = self.mariadb_connection.cursor()

    #gets the current les rooster for a klas
    def get_rooster(self, klas):
        return self.get_data(Windesheim_API + "Klas/%s/les" % klas)

    #gets json from a page, used for interacting with API's
    def get_data(self, link, data):
        if data:
            for k,v in data.items():
                link += k + '=' + str(v) + "&"

            link = link[:-1]

        contents = urllib.request.urlopen(link).read()
        js = json.loads(contents.decode('utf-8'))

        return js


    # -------------------- PSEUDO CODE ---------------------------#

    #gets the first lesson of a day
    def get_schoolStartTime(self, date):
        rooster = self.get_rooster(self.get_setting_value('klas'))
        todays_classes = []
        for l in rooster:
            #loop over all classes in semester
            if l.date == date:
                #match all classes on the  day
                todays_classes.append(l)

        #order classes by date
        todays_classes = sorted(todays_classes, key=lambda lesson: lesson.date)
        #return earliest date
        if todays_classes[0]:
            return todays_classes[0].date
        #returns none if there are no classes on the day
        return None

    #get the time you have to leave for travel with OV
    def get_OV_departureTime(self):
        link = OV_API + "/journeys?"
        sett = self.get_settings()
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
            'dateTime': self.get_schoolStartTime(datetime.datetime.now()), #get school start time for today
            'searchType': 'arrival',
            'interchangeTime': 'standard',
            'after': 5,
            'to': Windesheim_OV_location,
            'realtime': True
        }

        journey = self.get_data(link,TravelSettings)
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
        OV_enabled = self.get_setting_value('OV')
        if OV_enabled:
            return self.get_OV_departureTime() - self.get_setting_value('snoozeBuffer')

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