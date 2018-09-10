import datetime, json
import mysql.connector as mariadb

class common:

    #api links
    OV_API = 'https://api.9292.nl/0.1'
    Google_API = "http://maps.googleapis.com/maps/api/distancematrix/json?"
    Windesheim_API = "http://roosterplusprod.cloudapp.net/api/"

    #variables
    mariadb_connection = None
    cursor = None

    def get_setting_value(self, setting):

        if not self.mariadb_connection or not self.cursor:
            self.connect_to_database()

        sql = "SELECT value FROM settings WHERE setting=%s" % setting
        try:
            self.cursor.execute(sql)
        except mariadb.Error as err:
            return err

        val = self.cursor.fetchone()

        return val

    def connect_to_database(user,pass,host,db):

        Database_Settings = {
            'user': user,
            'password': pass,
            'host': host,
            'database': db,
            'raise_on_warnings': True
        }

        try:
            self.mariadb_connection = mariadb.connect(**Database_Settings)
        except mariadb.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return "Database does not exist"
            else:
                return ("Error: {}".format(err)

        self.cursor = self.mariadb_connection.cursor()
