from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import utils

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "27eduCBA09"
Session(app)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/explore')
def explore():
    venues = utils.get_venues()
    return render_template('explore.html', venuesList=venues)

@app.get('/createAccount')
def createPage():
    return render_template('createAccount.html')

@app.post('/createAccount')
def createAccount():
    print("account created")
    return redirect("/")

@app.get('/listVenue')
def listPage():
    return render_template('listVenue.html')

@app.post('/listVenue')
def listVenue():
    print("in post listVenue")
    name = request.form["name"]
    location = request.form["location"]
    category = request.form["category"]
    capacity = request.form["capacity"]
    utils.listVenue(name,capacity,location,category,session["email"])
    return redirect("/")

# POST Method to handle user sign in
@app.post('/signIn')
def signInPost():
    data = request.get_json()
    # Based on user mode selector in Sign In Form
    if(data["userMode"] == True):
        status = utils.signIn(data["email"],data["password"],"OWNER")
        print(status)
        if status == "signedIn":
            print("inside if")
            session["user_mode"] = "OWNER"
            session["email"] = data["email"]
            return "signedIn"
        else :
            print("inside else")
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

if __name__ == "__main__":
    print("Server Starting ...")
    app.run(host="0.0.0.0")