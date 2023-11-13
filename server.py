from flask import Flask, render_template
from test import test

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('createAccount.html')


if __name__ == "__main__":
    print("Server Starting ...")
    app.run(host="0.0.0.0")