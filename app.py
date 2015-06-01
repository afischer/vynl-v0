from flask import Flask, render_template, redirect,request, jsonify, Response
from flask.ext.socketio import SocketIO, join_room, leave_room, emit
import random
import string
import party as p

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@app.route("/api/parties/<party_id>",
           methods=["GET", "POST", "PATCH", "DELETE"])
def apiParty(party_id):
    newParty = p.Party(party_id)
    if request.method == "GET":
        return jsonify({"songs": newParty.getOrdered()})
    elif request.method == "POST":
        print "POST"
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
        print rec["videoID"]
        newParty.removeSong(rec["videoID"])


def genID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))


@app.route("/")
def index():
    return render_template("index.html", partyID=genID())


@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
  return render_template("contact.html")

@app.route("/party")
def party():
    return render_template("party.html")


@app.route("/party/<partyID>")
def genParty(partyID):
    if (len(partyID) == 8):
        return render_template("party.html", partyID=partyID)
    else:
        return '<h1>404</h1>', 404


@app.route("/<partyID>")
def redirParty(partyID):
    if (len(partyID) == 8):
        partyURL = "/party/" + partyID
        return redirect(partyURL, code=303)
    else:
        return '<h1>404</h1>', 404

@socketio.on('connect', namespace='/party')
def test_connect():
    print "connected"
    emit('connect', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/party')
def test_disconnect():
    print "client disconnected"

@socketio.on('join', namespace='/party')
def on_join(data):
    room = data['room']
    join_room(room)
    newParty = p.Party(room)
    print "joined room: " + room
    emit('join', {"songs": newParty.getOrdered()})


@socketio.on('leave', namespace='/party')
def on_leave(data):
    room = data['room']
    leave_room(room)
    print "nigga left room: " + room


@socketio.on('addSong', namespace='/party')
def addSong(data):
    partyID = data['room']
    song = data['song']
    newParty = p.Party(partyID)
    print "adding song: ", song, " to room: " + partyID
    newParty.addSong(song["songID"], song["albumarturl"], song["songname"], song["songartist"])
    emit('addSong', song, room=partyID)


@socketio.on('voteSong', namespace="/party")
def voteSong(data):
    partyID = data['room']
    song = data['song']
    vote = data['vote']
    newParty = p.Party(partyID)
    print "vote: ", vote, " for song: ", song, " to room: " + partyID
    if vote == 1:
        newParty.upVote(song["songID"])
    elif vote == -1:
        newParty.downVote(song["songID"])
    emit('updateSongs', {newParty.getOrdered()}, room=partyID)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=8000)
