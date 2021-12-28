from flask import Flask, render_template, redirect, session, request, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from tempfile import mkdtemp
from werkzeug.exceptions import ClientDisconnected, default_exceptions, HTTPException, InternalServerError

from helpers import error

app = Flask(__name__)
app.config["SECRET_KEY"] = "b\xe9\xa5\x1cO\xea,K\x86\x88\xdd\xb9o\xa6\xd1*\x03"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000") # TODO: remove cors_allowed_origins in the finished state



"""
Plans:

Room system
How do I know what room and name is?
You use local storage to know.

Make Speed

TODO: 
Room html
App room code

change username to not be a page and instead just exist in room.html somehow
figure out how to display a page and then display a different page while staying on the same url

"""

# Lobby
@app.route("/", methods=["GET", "POST"])
def lobby():
    if request.method == "POST":
        
        roomname = request.form.get("room") 
        # FIGURE OUT HOW TO CHECK IF USER HAS A NAME in local storage then send them to room or username depending

        if len(roomname) <= 0:
            return error("Room name must not be empty") 
        elif type(roomname) != str:
            return error("Room name must be a made of letters", 400)

        

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
            return error("Username must be less than 20 characters long")

        return redirect(url_for("room", roomname=roomname))
    else:
        return render_template("username.html")

# If the user goes directly to /room or /username redirect them to lobby
@app.route("/username")
@app.route("/room")
def no_room():
    return redirect(url_for("lobby"))

# Makes a room
@app.route("/room/<string:roomname>")
def room(roomname):
    return render_template("room.html", roomname=roomname)

socketio.on("connect")
def connect():
    emit("server_connect", "Server connected")

socketio.on("client_join")
def client_join():

    # TODO
    emit()

socketio.on("disconnect")
def disconnect():
    # TODO
    emit("opponent_disconnect")

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