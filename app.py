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
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = str(u.uuid4())
    if d: print "connect:",sessionid
    emit('connect', {'data': sessionid})

@socketio.on('getID', namespace='/party')
def getID(data):
    if 'id' in session:
        sessionid = session['id']
    else:
        if 'sessionid' in data:
            sessionid = data['sessionid']
        else:
            sessionid = str(u.uuid4())
    if d: print "getID: ", sessionid
    emit('getID', {'id': sessionid})


@socketio.on('disconnect', namespace='/party')
def test_disconnect():
    if d: print "client disconnected"

@socketio.on('makeParty', namespace='/party')
def makeParty(data):
    if d: print session.keys()
    if d: print 'id' not in session.keys()
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = data['sessionid']
    if d: print "makeParty:", sessionid
    room = data['room'].upper()

    if p.partyExists(room):
        emit('makeParty', {'error': 'room already exists'})
    else:
        newParty = p.Party(room, sessionid)
        if d: print "user: " + sessionid + "created party: " + room
        url = 'http://vynl.party/party/' + room
        emit('makeParty', {'id': sessionid})

@socketio.on('join', namespace='/party')
def on_join(data):
    #vote = data['vote']
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = data['sessionid']
    if d: print "onjoin:", sessionid
    room = data['room'].upper()
    if not p.partyExists(room):
        if d: print "room does not exist: " + room
        emit('join', {"error": "Party Does Not Exist"})
    else:
        join_room(room)
        newParty = p.Party(room)
        dj = newParty.getDJ()
        if d: print "joined room: " + room
        emit('join', {"songs": newParty.getOrdered(sessionid),
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
    newParty = p.Party(partyID)
    if d: print "adding song: ", song, " to room: " + partyID
    newParty.addSong(song["songID"], song["albumarturl"], song["songname"], song["songartist"])
    emit('addSong',{})
    emit('notifySongUpdate', {"data": True}, room=partyID)


@socketio.on('getSongs', namespace='/party')
def getSong(data):
    if d: print "updating songs"
    partyID = data['room'].upper()
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = data['sessionid']
    newParty = p.Party(partyID)
    thang=newParty.getOrdered(sessionid)
    dj=newParty.getDJ();
    if d: print thang
    emit('updateSongs', {"songs":thang,"dj":dj })


@socketio.on('voteSong', namespace="/party")
def voteSong(data):
    partyID = data['room'].upper()
    song = data['song']
    vote=data['vote']
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = data['sessionid']
    newParty = p.Party(partyID)
    if d: print "user: ", sessionid, " vote: ", vote, " for song: ", song, " to room: " + partyID
    if vote == 1:
        newParty.upVote(song["songID"], sessionid)
    elif vote == -1:
        newParty.downVote(song["songID"], sessionid)
    emit('notifySongUpdate', {"data": True}, room=partyID)


@socketio.on('deleteSong', namespace="/party")
def deleteSong(data):
    partyID = data['room'].upper()
    song = data['song']
    if 'id' in session:
        sessionid = session['id']
    else:
        sessionid = data['sessionid']
    newParty = p.Party(partyID)
    dj = newParty.getDJ()
    if dj == sessionid:
        if d: print "user: ", sessionid, " deleting song: ", song["songID"], " to room: ", partyID
        newParty.removeSong(song["songID"])
        emit('notifySongUpdate', {"data": True}, room=partyID)
        emit('success', {'data': "Deleted Song"})
    else:
        if d: print "user: ", sessionid, " is not a dj: ", dj
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
