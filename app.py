from flask import Flask, render_template, redirect,request, jsonify, Response, sessions,session, url_for, send_from_directory
from flask.ext.socketio import SocketIO, join_room, leave_room, emit
import random
import string
import party as p
import uuid as u
import logging
from logging.handlers import RotatingFileHandler
import argparse
import sys
from flask_sitemap import Sitemap
from oauth2client import client, crypt

## Parse CL Options
'''
parser = argparse.ArgumentParser(description='Vynl.party backend routing.')

parser.add_argument('-d', '--debug',
                  dest="debug",
                  default=False,
                  action="store_true",
                  )
parser.add_argument('-p',
                  action="store",
                  dest="port",
                  type=int,
                  default="8000",
                  help="Specify port"
                  )
parser.add_argument('-V','--version',
                  action='version',
                  version="Vynl - %(prog)s 0.0.1",
                  help="Log version and exit"
                  )

args = parser.parse_args()
d = args.debug
'''

d = False
## Flask App ##
app = Flask(__name__)
ext = Sitemap(app=app)
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True
#######Comment next line out when testing
app.config['SERVER_NAME']='vynl.party'
#app.config['SECRET_KEY'] = 'secret'
with open('secret.txt','r') as f:
    app.secret_key =f.readline().strip("\n")
    apiKey=f.readline().strip("\n")
socketio = SocketIO(app)

@app.route("/api/parties/<party_id>",
           methods=["GET", "POST", "PATCH", "DELETE"])
def apiParty(party_id):
    party_id=party_id.upper()
    newParty = p.Party(party_id)
    if request.method == "GET":
        return jsonify({"songs": newParty.getOrdered()})
    elif request.method == "POST":
        if d: print "POST"
        rec = request.get_json()
        newParty.addSong(rec["videoID"], rec["title"], rec["artist"])
        return jsonify({"success": True})
    elif request.method == "PATCH":
        rec = request.get_json()
        if rec["upvote"]:
            newParty.upVote(rec["videoID"])
        else:
            newParty.downVote(rec["videoID"])
        return jsonify({"success": True})
    elif request.method == "DELETE":
        rec = request.get_json()
        if d: print rec["videoID"]
        newParty.removeSong(rec["videoID"])


def genID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))


@app.route("/")
def index():
    if 'id' not in session.keys():
        session['id']=str(u.uuid4())
    x=genID()
    while p.partyExists(x):
        x=genID()
    return render_template("index.html", partyID=x, debug=d)

'''
@app.route("/base")
def base():
    return render_template("base.html")
'''

@app.route("/about")
def about():
    return render_template("about.html")

'''
@app.route("/contact")
def contact():
  return render_template("contact.html")
'''
@app.route("/party")
def party():
    return render_template("party.html")

@app.route("/login", methods=['GET',"POST"])
def login():
    print "loginnn"
    if request.method=='POST':
        print "it's a post"
        idtoken=request.form.get('idtoken')
        try:
            idinfo = client.verify_id_token(idtoken, '673195807989-euva4oi2v80e1t6q1g3sig5sohbcgbiq.apps.googleusercontent.com')
            if idinfo['aud'] not in ['673195807989-euva4oi2v80e1t6q1g3sig5sohbcgbiq.apps.googleusercontent.com']:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            print "hallelujah"
        except crypt.AppIdentityError:
            # Invalid token
            print 'error'
        userid = idinfo['sub']
        return flask.jsonify(**idinfo)
    return render_template("login.html")

@app.route("/party/<partyID>")
def genParty(partyID):
    partyID=partyID.upper()
    if (len(partyID) == 8):
        if 'id' not in session.keys():
            session['id']=str(u.uuid4())
        return render_template("party.html", partyID=partyID,key=apiKey)
    else:
        return '<h1>404</h1>', 404

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/<partyID>")
def redirParty(partyID):
    partyID=partyID.upper()
    if (len(partyID) == 8):
        if 'id' not in session.keys():
            session['id']=str(u.uuid4())
        partyURL = "/party/" + partyID
        return redirect(partyURL, code=303)
    else:
        return '<h1>404</h1>', 404

@socketio.on('connect', namespace='/party')
def test_connect():
    if d: print "connected"
    if 'id' not in session.keys():
        session['id']=str(u.uuid4())
    if d: print "connect:",session['id']
    emit('connect', {'data': session['id']})

@socketio.on('getID', namespace='/party')
def getID(data):
	if 'id' not in session.keys():
		session['id']=str(u.uuid4())
	if d: print "getID: ", session['id']
	emit('getID', {'id': session['id']})


@socketio.on('disconnect', namespace='/party')
def test_disconnect():
    if d: print "client disconnected"

@socketio.on('makeParty', namespace='/party')
def makeParty(data):
    if d: print session.keys()
    if d: print 'id' not in session.keys()
    if 'id' not in session.keys():
        session['id']=str(u.uuid4())
    if d: print "makeParty:", session['id']
    room = data['room'].upper()
    ip = session['id']
    newParty = p.Party(room, ip)
    if d: print "user: " + ip + "created party: " + room
    url = 'http://vynl.party/party/' + room
    emit('makeParty', {'id': session['id']})

@socketio.on('join', namespace='/party')
def on_join(data):
    #vote = data['vote']
    if 'id' not in session.keys():
        session['id']=str(u.uuid4())
    if d: print "onjoin:", session['id']
    room = data['room'].upper()
    ipAddress =session['id']
    join_room(room)
    newParty = p.Party(room)
    dj = newParty.getDJ()
    if d: print "joined room: " + room
    emit('join', {"songs": newParty.getOrdered(ipAddress),
                  "dj": dj, "current":newParty.getPlaying()})


@socketio.on('leave', namespace='/party')
def on_leave(data):
    room = data['room'].upper()
    leave_room(room)
    if d: print "broski left room: " + room


@socketio.on('addSong', namespace='/party')
def addSong(data):
    #app.logger.error(data)
    partyID = data['room'].upper()
    song = data['song']
    ipAddress = session['id']
    newParty = p.Party(partyID)
    if d: print "adding song: ", song, " to room: " + partyID
    newParty.addSong(song["songID"], song["albumarturl"], song["songname"], song["songartist"])
    emit('addSong',{})
    emit('notifySongUpdate', {"data": True}, room=partyID)


@socketio.on('getSongs', namespace='/party')
def getSong(data):
    if d: print "updating songs"
    partyID = data['room'].upper()
    ipAddress = session['id']
    newParty = p.Party(partyID)
    thang=newParty.getOrdered(ipAddress)
    dj=newParty.getDJ();
    if d: print thang
    emit('updateSongs', {"songs":thang,"dj":dj })


@socketio.on('voteSong', namespace="/party")
def voteSong(data):
    partyID = data['room'].upper()
    song = data['song']
    vote=data['vote']
    ipAddress = session['id']
    newParty = p.Party(partyID)
    if d: print "user: ", ipAddress, " vote: ", vote, " for song: ", song, " to room: " + partyID
    if vote == 1:
        newParty.upVote(song["songID"], ipAddress)
    elif vote == -1:
        newParty.downVote(song["songID"], ipAddress)
    emit('notifySongUpdate', {"data": True}, room=partyID)


@socketio.on('deleteSong', namespace="/party")
def deleteSong(data):
    partyID = data['room'].upper()
    song = data['song']
    ipAddress = session['id']
    newParty = p.Party(partyID)
    dj = newParty.getDJ()
    if dj == ipAddress:
        if d: print "user: ", ipAddress, " deleting song: ", song["songID"], " to room: ", partyID
        newParty.removeSong(song["songID"])
        emit('notifySongUpdate', {"data": True}, room=partyID)
        emit('success', {'data': "Deleted Song"})
    else:
        if d: print "user: ", ipAddress, " is not a dj: ", dj
        emit('error', {'data': "You are not the dj. You cannot Delete songs"});


@socketio.on('playSong', namespace="/party")
def playingSong(data):
    partyID = data['room'].upper()
    song = data['song']
    newParty = p.Party(partyID)
    newParty.playSong(song["songID"])
    if d: print "playing song: ", song, " in room: ", partyID
    emit('playSong', {"song": song}, room=partyID)
    emit('notifySongUpdate', {"data": True}, room=partyID)

def app_main(port=8000, debug=False):
    d=debug
    if d: print " * Starting in debug mode"
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    if d: app.debug=True
    print " *****************************************"
    print " *                                       *"
    print " * Vynl Server successfully initialized! *"
    print " *                                       *"
    print " *****************************************"
    socketio.run(app, host='0.0.0.0', port=port)



if __name__ == "__main__":
    d=True
    if d: print " * Starting in debug mode"
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    if d: app.debug=True
    print " *****************************************"
    print " *                                       *"
    print " * Vynl Server successfully initialized! *"
    print " *                                       *"
    print " *****************************************"
    socketio.run(app, host='0.0.0.0', port=8000)
