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
    return ""

@app.get('/listVenue')
def listPage():
    return render_template('listVenue.html')

@app.post('/listVenue')
def listVenue():
    print("venue created")
    return ""

# POST Method to handle user sign in
@app.post('/signIn')
def signInPost():
    print("in sign in")
    data = request.get_json()
    session["email"] = data["email"]
    # Based on user mode selector in Sign In Form
    if(data["userMode"] == True):
        session["user_mode"] = "OWNER"
    else:
        session["user_mode"] = "CUSTOMER"

    return "signedIn"

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




if __name__ == "__main__":
    print("Server Starting ...")
    app.run(host="0.0.0.0")