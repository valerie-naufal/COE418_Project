import mysql.connector
from mysql.connector import errorcode

get_venues_query = ("SELECT name, location, type, capacity FROM venue")
    
try:
    cnx = mysql.connector.MySQLConnection(user='root', password='root',
                                host='127.0.0.1',
                                database='venue_db')
    cursor = cnx.cursor()

except:
    print("Could not connect")
    
def get_venues():
    venues = []
    cursor.execute(get_venues_query)
    
    for(name, location, type, capacity) in cursor:
        venues.append({"name":name, "location":location, "type":type, "capacity":capacity})
    return venues
