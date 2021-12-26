from flask import request, render_template

def error(message, code):
    return render_template("error.html", message=message, code=code)