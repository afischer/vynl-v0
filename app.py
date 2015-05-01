from flask import Flask, render_template
import random
import string

app = Flask(__name__)

def genID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))

@app.route("/")
def index():
    return render_template("index.html", partyID=genID())

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/party")
def party():
    return render_template("party.html")

@app.route("/party/<partyID>")
def genParty(partyID):
    return render_template("party.html", partyID=partyID)

# TEMP
@app.route("/search.json")
def search():
    return render_template("search.json")


if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
