from flask import Flask, render_template, redirect, session, request, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from tempfile import mkdtemp
from werkzeug.exceptions import ClientDisconnected, default_exceptions, HTTPException, InternalServerError
import sqlite3

from helpers import error

app = Flask(__name__)
app.config["SECRET_KEY"] = "b\xe9\xa5\x1cO\xea,K\x86\x88\xdd\xb9o\xa6\xd1*\x03"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("database.db")

socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000") # TODO: remove cors_allowed_origins in the finished state

rooms = {}


"""
Plans:

Room system
How do I know what room and name is?
You use local storage to know.

Okay what do I need to do?
make the chatbox so that people can talk
make the dice rolling
make the dice options that get sent by the server
make it disable when it's not your turn
make the ready button
chatbox
lobby info

HOW IN THE WORLD WOULD A USER LIST WORK?
in server
it has to update whenever someone sends them an update.
when tho
User join, name change, user disconnect

(host)
user joins 
sends to server user join and name and stuff
host then gets updated by user join. how do I know who is in the room?

when someone joins the room they send user_joined to server then
server emits back to everyone user_join they send their name to the server then

server sends back a new userlist


TODO: 
lobby info
chatbox
ready button
dice roll
dice options
disable


Room html
App room code

Zilch

"""

# Lobby
@app.route("/", methods=["GET", "POST"])
def lobby():
    if request.method == "POST":
        
        roomname = request.form.get("room") 

        if len(roomname) <= 0:
            return error("Room name must not be empty") 
        elif type(roomname) != str:
            return error("Room name must be a made of letters", 400)

        session["room"] = roomname

        return redirect(url_for("username", roomname=roomname))
    else:
        return render_template("lobby.html")

# Prompts the user for a username when entering or creating a room
@app.route("/room/<string:roomname>/username/", methods=["GET", "POST"])
def username(roomname):

    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return error("Must input a username", 400)
        elif type(username) != str:
            return error("Username must be text", 400)
        elif len(username) > 20:
            return error("Username must be less than 20 characters long", 400)
        elif roomname in rooms:
            if username in rooms[roomname]:
                print("E E EE EE")
                return render_template("username.html", error="Username already taken")

        session["name"] = username

        return redirect(url_for("room", roomname=roomname))
    else:
        return render_template("username.html")

# If the user goes directly to /room redirect them to lobby
@app.route("/room/")
def no_room():
    return redirect(url_for("lobby"))

# Makes a room
@app.route("/room/<string:roomname>/")
def room(roomname):
    if request.method == "GET":
        return render_template("room.html", roomname=roomname)
    else:
        return redirect(url_for("username", roomname=roomname))

# Basic connection
@socketio.on("connect")
def connect():
    emit("server_connect", "Server connected")

# New user joined
@socketio.on("client_join")
def client_join(data):

    join_room(data["roomname"])
    session["name"] = data["name"]
    session["room"] = data["roomname"]

    if data["roomname"] in rooms:
        rooms[data["roomname"]].append(data["name"])
    else:
        rooms[data["roomname"]] = []
        rooms[data["roomname"]].append(data["name"])
    emit("server_message", {"msgtype": "user_join", "message": data["name"] + " has joined",  "name": data["name"], "userlist": rooms[data["roomname"]]}, to=data["roomname"])

# Message through chatbox
@socketio.on("client_message")
def client_message(data):
    emit("server_message", {"msgtype": "user_message", "message": data["message"], "name": data["name"]}, to=data["roomname"])

# User requested a name change
@socketio.on("name_change")
def name_change(data):

    username = data["new_name"]

    # These should only activate if they mess with the javascript
    if not username:
        emit("name_change_confirm", "New name cannot be nothing" )
        return False
    elif type(username) != str:
        emit("name_change_confirm", "New name must be text")
        return False
    elif len(username) > 20:
        emit("name_change_confirm", "New name must be less than 20 characters long")
        return False    
    elif username in rooms[data["roomname"]]:
        emit("name_change_confirm", "New name must not be the same as another user")
    # New name is within parameters
    else:
        session["name"] = username

        for name, i in zip(rooms[data["roomname"]], range(len(rooms[data["roomname"]]))):
            if name == data["old_name"]:
                rooms[data["roomname"]][i] = username

        emit("name_change_confirm", "allowed")
        emit("server_message", {"msgtype": "name_change", "message": '"'+ data["old_name"] + '" has changed their name to "' + data["new_name"] + '"',
         "old_name": data["old_name"], "new_name": data["new_name"], "userlist": rooms[data["roomname"]]}, to=data["roomname"])

# User disconnected
@socketio.on("disconnect")
def disconnect():
    if session.get("room") in rooms:
        rooms[session.get("room")].remove(session.get("name"))

    leave_room(session.get("room"))
    emit("server_message", {"msgtype": "user_disconnect", "message": session.get("name") + " has disconnected", "name": session.get("name"), "userlist": rooms[session.get("room")]}, to=session.get("room"))

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# Run the app
if __name__ == "__main__":
    socketio.run(app)