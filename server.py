from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import utils, os
from datetime import datetime

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "27eduCBA09"
Session(app)


@app.route('/')
def home():
    return render_template('main.html')

@app.get('/myProfile')
def myprofile():
    return render_template('myProfile.html')

@app.route('/explore')
def explore():
    venues = utils.get_venues()
    return render_template('explore.html', venuesList=venues)

@app.get('/createAccount')
def createPage():
    return render_template('createAccount.html')

@app.post('/createAccount')
def createAccount():
    firstName = request.form["firstName"]
    lastName = request.form["lastName"]
    phoneNb = request.form["phoneNb"]
    email = request.form["email"]
    password = request.form["password"]
    userMode = request.form["userMode"]
    utils.createAccount(firstName,lastName,phoneNb,email,password,userMode)
    return redirect("/")

@app.get('/listVenue')
def listPage():
    if session["email"]:
        return render_template('listVenue.html')
    else:
        redirect("/")

@app.post('/listVenue')
def listVenue():
    print("in post listVenue")
    name = request.form["name"]
    location = request.form["location"]
    category = request.form["category"]
    capacity = request.form["capacity"]
    price = request.form["price"]
    image = request.files["imgPath"]
    file_fullName = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(file_fullName)
    imgPath = "/static/images/" + image.filename
    utils.listVenue(name,capacity,location,category,session["email"],price,imgPath)
    return redirect("/")

# POST Method to handle user sign in
@app.post('/signIn')
def signInPost():
    data = request.get_json()
    # Based on user mode selector in Sign In Form
    if(data["userMode"] == True):
        status = utils.signIn(data["email"],data["password"],"OWNER")
        if status == "signedIn":
            session["user_mode"] = "OWNER"
            session["email"] = data["email"]
            return "signedIn"
        else :
            return "error"
        
    else:
        status = utils.signIn(data["email"],data["password"],"CUSTOMER")
        if status == "signedIn":
            session["user_mode"] = "CUSTOMER"
            session["email"] = data["email"]
            return "signedIn"
        else :
            return "error"


# GET Method to check logIn status
@app.get('/loggedIn')
def loggedIn():
    if session.get("email") != None:
        return {"loggedIn": True}
    else:
        return {"loggedIn": False}

# POST METHOD to handle user sign out
@app.post("/signOut")
def signOut():
    session["email"] = None
    session["user_mode"] = None
    return "signedOut"

# GET method to populate dropdowns
@app.get("/dropdowns")
def dropdowns():
    dropdowns = utils.get_dropdowns()
    return dropdowns

@app.post("/search")
def search_route():
    data = request.get_json()
    results = utils.search(data["location"], data["category"],data["capacity"])
    return results

@app.post("/reserve")
def reserve_route():

    date_time = request.form["datetime"]
    date_parsed = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    date = str(date_parsed.year) + "-" + str(date_parsed.month) + "-" + str(date_parsed.day)
    starttime = str(date_parsed.hour) + ":" + str(date_parsed.minute) 
    photographer = None if  request.form["photographer"]=="0" else request.form["photographer"]
    catering = None if  request.form["catering"]=="0" else request.form["catering"]
    entertainment = None if  request.form["entertainment"]=="0" else request.form["entertainment"]
    planner = None if  request.form["planner"]=="0" else request.form["planner"]
    nbHours = request.form["nbHours"]
    venue_name = request.form["venue_name"]
    email = session["email"]
    utils.reserve(date,photographer,catering,entertainment,planner,starttime,nbHours,venue_name,email)
    return redirect("/")

if __name__ == "__main__":
    print("Server Starting ...")
    app.run(host="0.0.0.0")