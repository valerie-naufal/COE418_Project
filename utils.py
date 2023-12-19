import mysql.connector
from mysql.connector import errorcode

get_venues_query = ("SELECT name, location, category, capacity,price,imgPath FROM venue")

get_locations_query = ("SELECT DISTINCT location FROM venue ORDER BY location")
    
get_categories_query = ("SELECT DISTINCT category FROM venue ORDER BY category")

get_capacities_query = ("SELECT DISTINCT capacity FROM venue ORDER BY capacity")

search_query = ("SELECT name,location,category,capacity,price,imgPath FROM venue WHERE location=%s AND category=%s AND  capacity>=%s ")

list_query = ("INSERT INTO venue(name,capacity,location,category,ownerId,price,imgPath) values(%s,%s,%s,%s,%s,%s,%s)")

owner_signIn = ("SELECT COUNT(*) AS count FROM owner WHERE email=%s AND password=%s ")

ownerID_query = ("SELECT ownerId FROM owner WHERE email=%s ")

custID_query = ("SELECT custId FROM customer WHERE email=%s ")

venueInfo_query = ("SELECT venueID,price FROM venue WHERE name=%s ")

cust_signIn = ("SELECT COUNT(*) AS count FROM customer WHERE email=%s AND password=%s ")

owner_create = ("INSERT INTO owner(firstName,lastName,phoneNb,email,password) values(%s,%s,%s,%s,%s)")

customer_create = ("INSERT INTO customer(firstName,lastName,phoneNb,email,password) values(%s,%s,%s,%s,%s)")

insertEvent_query = ("INSERT INTO event(date,photographerID,cateringID,entertainmentID,plannerID) values(%s,%s,%s,%s,%s)")

book_query = ("INSERT INTO book(eventID,venueID,custID,date,starttime,nbHours,total) value((select eventID from event where date=%s),%s,%s,%s,%s,%s,%s);")

get_event_query = ("SELECT E.eventID,V.name,B.date,total, E.photographerID, E.cateringID, E.entertainmentID, E.plannerID FROM event E, venue V, book B WHERE B.venueID=V.venueID AND E.eventID=B.eventID AND custID=%s")

get_venues_profile = ("SELECT venueID,name,location,category,capacity,price FROM venue WHERE ownerID=%s")

cancel_event =("DELETE FROM event WHERE eventID=%s" )

cancel_venue = ("DELETE FROM venue WHERE venueID=%s" )

update_venue = ("UPDATE venue SET name=%s, location=%s, category=%s, capacity=%s, price=%s WHERE venueID=%s")

try:
    cnx = mysql.connector.MySQLConnection(user='root', password='root',
                                host='127.0.0.1',
                                database='venue_db')
    
except:
    print("Could not connect")

def get_venues():
    venues = []
    cursor = cnx.cursor()
    cursor.execute(get_venues_query)
    
    for(name, location, category, capacity,price,imgPath) in cursor:
        venues.append({"name":name, "location":location, "category":category, "capacity":capacity,"price":price,"imgPath":imgPath})

    cursor.close()
    return venues

def get_event(email):
    events =[]
    cursor = cnx.cursor()
    custID = get_custID(email)
    cursor.execute(get_event_query,(custID,))
    for (eventID,name,date,total, photographerID, cateringID, entertainmentID, plannerID) in cursor:
        events.append({"eventID":eventID,"name":name,"date":date,"total":total, "photographerID": photographerID, "cateringID":cateringID, "entertainmentID":entertainmentID, "plannerID":plannerID})
    
    cursor.close()
    return events

def get_venue_profile(email):
    venue =[]
    cursor = cnx.cursor()
    ownerID = get_owner_Id(email)
    cursor.execute(get_venues_profile,(ownerID,))
    for (venueID,name,location,category,capacity,price) in cursor:
        venue.append({"venueID":venueID,"name":name,"location":location,"category":category,"capacity":capacity,"price":price})
    
    cursor.close()
    return venue

def cancelEvent(eventID):
    cursor = cnx.cursor()
    cursor.execute(cancel_event,(eventID,))
    cnx.commit()
    cursor.close()

def deleteVenue(venueID):
    cursor = cnx.cursor()
    cursor.execute(cancel_venue,(venueID,))
    cnx.commit()
    cursor.close()

def updateVenue(venueID, name, location, category, capacity, price):
    cursor = cnx.cursor()
    cursor.execute(update_venue, (name, location, category, capacity, price, venueID))
    cnx.commit()
    cursor.close()

def get_dropdowns():
    locations =[]
    cursor = cnx.cursor()
    cursor.execute(get_locations_query)

    for(location,) in cursor:
        locations.append(location)
    cursor.close()

    categories=[]
    cursor = cnx.cursor()
    cursor.execute(get_categories_query)

    for(category,) in cursor:
        categories.append(category)
    cursor.close() 

    capacities=[]
    cursor = cnx.cursor()
    cursor.execute(get_capacities_query)

    for(capacity,) in cursor:
        capacities.append(capacity)
    cursor.close()

    return {"locations": locations, "categories": categories, "capacities": capacities}

def search(location,category,capacity):
    results = []
    cursor = cnx.cursor()
    cursor.execute(search_query,(location,category,capacity))

    for(name, location, category, capacity,price,imgPath) in cursor:
        results.append({"name":name, "location":location, "category":category, "capacity":capacity,"price":price,"imgPath":imgPath})
    cursor.close()
    return results

def reserve(date,photographer,catering,entertainment,planner,starttime,nbHours,venue_name,email):
    cursor = cnx.cursor()
    venueID,price = get_venueInfo(venue_name)
    custID = get_custID(email)
    total = float(nbHours)*float(price)
    cursor.execute(insertEvent_query,(date,photographer,catering,entertainment,planner))
    cnx.commit()
    cursor.execute(book_query,(date,venueID,custID,date,starttime,nbHours,total))
    cnx.commit()
    cursor.close()

def get_custID(email):
    ID = ""
    cursor = cnx.cursor()
    cursor.execute(custID_query,(email,))
    for(custId,) in cursor:
        ID = custId
    cursor.close()
    return ID

def get_venueInfo(name):
    ID = ""
    price = ""
    cursor = cnx.cursor()
    cursor.execute(venueInfo_query,(name,))
    for(venueId,price) in cursor:
        ID = venueId
        price = price
    cursor.close()
    return ID,price

def get_owner_Id(email):
    ID = ""
    cursor = cnx.cursor()
    cursor.execute(ownerID_query,(email,))
    for(ownerId,) in cursor:
        ID = ownerId
    cursor.close()
    return ID

def listVenue(name,capacity,location,category,email,price,imgPath):
    ownerId = get_owner_Id(email)
    cursor = cnx.cursor()
    cursor.execute(list_query,(name,capacity,location,category,ownerId,price,imgPath))
    cnx.commit()
    cursor.close()

def signIn(email,password,user_mode):
    cursor = cnx.cursor()
    if user_mode=="OWNER":
        cursor.execute(owner_signIn,(email,password))
    else :
        cursor.execute(cust_signIn,(email,password))

    for(count,) in cursor :
        if count ==1 :
            cursor.close()
            return "signedIn"
        else :
            cursor.close()
            return "error"
        
def createAccount(firstName,lastName,phoneNb,email,password,userMode):
    cursor = cnx.cursor()
    if userMode == "owner":
        cursor.execute(owner_create,(firstName,lastName,phoneNb,email,password))
        cnx.commit()
    else :
        cursor.execute(customer_create,(firstName,lastName,phoneNb,email,password))
        cnx.commit()
        
    cursor.close()

