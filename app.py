from flask import Flask, render_template, redirect, session, request
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
TODO: 


"""


@app.route("/")
def index():
    return render_template("")
    
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    socketio.run(app)