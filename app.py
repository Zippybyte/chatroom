from flask import Flask, render_template, redirect, session, request, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
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

socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")



"""
Plans:
Make a lobby system so that people can input a string and have them "host" that room and also have people join them.
make speed

How does a lobby system work?
well it has to be in /room
so how does a link to that work?
YOU CAN CHECK THE URL Sooooooooooooo, just have room exist then when someone connects you take the url 
and parse the data after /room/ then I can use that data and connect them to the room!

TODO: 
figure out how to make a lobby system

"""

# Lobby
@app.route("/", methods=["GET", "POST"])
def username():

    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return error("Must input a username", 400)
        elif type(username) != str:
            return error("Username must be text", 400)

        return redirect("/lobby")

    else:
        return render_template("username.html")

# Lobby so that users can connect to rooms
@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    if request.method == "POST":
        
        roomname = request.form.get("room")

        if len(roomname) <= 0:
            return error("Room name must not be empty") 
        elif type(roomname) != str:
            return error("Room name must be a made of letters", 400)

        return redirect(url_for("room", roomname=roomname))
    else:
        return render_template("lobby.html")

# If the user goes directly to /room redirect them to lobby
@app.route("/room")
def no_room():
    return redirect("/lobby")

# Rooms where the user will use the most
@app.route("/room/<string:roomname>")
def room(roomname):



    return 'The room name is: ' + roomname

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