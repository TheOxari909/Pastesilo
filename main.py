from flask import Flask, render_template, request, redirect, url_for
import string
import random
from os import path

app = Flask(__name__) 

letters = string.ascii_letters + string.digits
def get_random_id():
    id = "".join(random.choice(letters) for i in range(6))
    while path.isfile(f"text/{id}") == True:
        id = "".join(random.choice(letters) for i in range(6))
    return id

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_data().decode("utf-8")
    data = data.removeprefix("text=")
    id = get_random_id()
    with open(f"text/{id}.txt", "w") as f:
        f.write(data)
    return redirect(url_for("text", id=id), code=302)

@app.route("/id/<id>")
def text(id):
    try:
        with open(f"text/{id}.txt", "r") as f:
            data = f.read()
    except:
        return render_template("404.html"), 404
    return render_template(f"text.html", data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if (__name__ == '__main__'):
    app.run(debug =True)