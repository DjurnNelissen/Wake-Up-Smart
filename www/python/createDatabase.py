import mysql.connector as mariadb
import getopt, sys
from mysql.connector import errorcode

#default database settings
keys = {
        'woonplaats': 'huns',
        'byBus': True,
        'byTrain': True,
        'byFerry': True,
        'klas': 'ICTM1g',
        'bySubway': True,
        'byTram': True,
        'snoozeBuffer': 15,
        'OV': True,
        'voornaam': '',
        'alarmVolume': 100,
        'playlist': '',
        'kleur_primary': '#4286f4',
        'kleur_secondary': '#26a83c',
        'alarmTijd': '',
        'achternaam': '',
        'geslacht': '',
        'adres': '',
        'huisnummmer': '',
        'postcode': '',
        'straat': ''
       }

mariadb_connection = None
cursor = None

settingsTableName = 'settings'
databaseName = 'WakeUp'
databaseUser = 'smartAlarm'
defaultPass = "smartWake"

Database_Settings = {
    'user': '',
    'password': '',
    'host': 'localhost',
    'raise_on_warnings': True
}

def parse_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'u:p:d:t:hH:')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            Database_Settings['user'] = arg
        elif opt == '-p':
            Database_Settings['password'] = arg
        elif opt == '-d':
            Database_Settings['database'] = arg
        elif opt == '-s':
            settingsTableName = arg
        elif opt == '-H':
            Database_Settings['host'] = arg
        elif opt == '-h':
            print("-h For this help menu.")
            print("-u <USER> to set the user used to connect to the database.")
            print("-p <PASSWORD> to set the password used to connect to the database.")
            print("-d <DATABASE> to set the database used.")
            print("-H <HOST> to set the host ip")
            print("-t <TABLE> to set the table thats being created")
            sys.exit(2)

parse_arguments()

#for database connection
def connect_to_database(DatabaseSettings):
    try:
    #tries to connect to your mariaDB with the given settings, The ** acts as a short cut to pass the right arguments from the
    #Database_Settings dictionary we setup earlier
        global mariadb_connection
        mariadb_connection = mariadb.connect(**DatabaseSettings)
# if the try statements gets an error this part is executed
    except mariadb.Error as err:
    #checks if the error is an access denied error
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
    #checks if the error is a Database does not exist error
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
    #if an other error occured it will just dump the entire error
        else:
            print("Error: {}".format(err))
    #stops the program
        sys.exit(2)

    #creates the cursor
    global cursor
    cursor = mariadb_connection.cursor()

def execute_sql(sql):
    print(sql)
    try:
        cursor.execute(sql)
    except mariadb.Error as err:
        print("Error: {}".format(err))
        #sys.exit(2)
    #if no error commit the change to the database
    mariadb_connection.commit()

connect_to_database(Database_Settings)

#create new database
sql = "CREATE DATABASE IF NOT EXISTS %s " % databaseName
execute_sql(sql)

#close current connection
cursor.close()
mariadb_connection.close()

#connect to the new database
Database_Settings['database'] = databaseName
connect_to_database(Database_Settings)

#add new user to who can only read/write this new database
sql = "CREATE USER '%s'@'localhost'" % databaseUser
execute_sql(sql)

#grants our user PRIVILEGES
sql = "GRANT ALL PRIVILEGES ON %s . * TO '%s'@'localhost'" % (databaseName, databaseUser)
execute_sql(sql)

#creates a settings table in the database
sql = "CREATE TABLE %s (ID int NOT NULL AUTO_INCREMENT, setting VARCHAR(255), value VARCHAR(255), PRIMARY KEY (ID))" % settingsTableName
execute_sql(sql)

#add default settings to table
for k,v in keys.items():
    sql = "INSERT INTO settings (setting, value) VALUES ('%s','%s')" % (str(k),str(v))
    execute_sql(sql)

print("Done...")
