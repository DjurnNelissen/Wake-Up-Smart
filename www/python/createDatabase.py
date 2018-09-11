import mysql.connector as mariadb
import getopt, sys

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
        'kleur_primary': 'red',
        'kleur_secondary': 'white'
       }

settingsTableName = 'settings'
databaseName = 'WakeUp'

Database_Settings = {
    'user': 'ghostwolf',
    'password': '',
    'host': 'localhost',
    'database': '%s' % databaseName,
    'raise_on_warnings': True
}

def parse_arguments():
    try:
        getopt.getopt(sys.argv[:1],'u:p:d:t:h')
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
        elif opt == '-h':
            print("-h For this help menu.")
            print("-u <USER> to set the user used to connect to the database.")
            print("-p <PASSWORD> to set the password used to connect to the database.")
            print("-d <DATABASE> to set the database used.")
            print("-t <TABLE> to set the table thats being created")
            sys.exit(2)

parse_arguments()

#for database connection
try:
    #tries to connect to your mariaDB with the given settings, The ** acts as a short cut to pass the right arguments from the
    #Database_Settings dictionary we setup earlier
    mariadb_connection = mariadb.connect(**Database_Settings)
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
cursor = mariadb_connection.cursor()

#creates a settings table in the database
sql = "CREATE TABLE %s" % settingsTableName
cursor.execute(sql)
mariadb_connection.commit()

for k,v in keys.items():
    sql = "INSERT INTO settings (setting, value) VALUES ('%s','%s')" % (str(k),str(v))
    cursor.execute(sql)
    mariadb_connection.commit()
