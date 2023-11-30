import mysql.connector
from mysql.connector import errorcode

get_venues_query = ("SELECT name, location, category, capacity FROM venue")

get_locations_query = ("SELECT DISTINCT location FROM venue ORDER BY location")
    
get_categories_query = ("SELECT DISTINCT category FROM venue ORDER BY category")

get_capacities_query = ("SELECT DISTINCT capacity FROM venue ORDER BY capacity")

search_query = ("SELECT name,location,category,capacity FROM venue WHERE location=%s AND category=%s AND  capacity=%s ")


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
    
    for(name, location, category, capacity) in cursor:
        venues.append({"name":name, "location":location, "category":category, "capacity":capacity})
    return venues

def get_locations():
    locations =[]
    cursor.execute(get_locations_query)

    for(location,) in cursor:
        locations.append({"location": location})
    return locations 

def get_categories():
    categories=[]
    cursor.execute(get_categories_query)

    for(category,) in cursor:
        categories.append({"category": category})
    return categories 

def get_capacities():
    capacities=[]
    cursor.execute(get_capacities_query)

    for(capacity,) in cursor:
        capacities.append({"capacity": capacity})
    return capacities 

def search(location,category,capacity):
    results = []
    cursor.execute(search_query,(location,category,capacity))

    for(name, location, category, capacity) in cursor:
        results.append({"name":name, "location":location, "category":category, "capacity":capacity})
    return results

