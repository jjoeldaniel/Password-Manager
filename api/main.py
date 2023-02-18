from flask import Flask, request, redirect, render_template, url_for
import db
app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def get_account():
    # if the combo doesnt exist
    username = request.get_json()["username"]
    password = request.get_json()["password"]

    print(username)
    print(password)
    if db.user_is_registered(username):
        return redirect(url_for('web.html'))
    else:
        return redirect(url_for('signup.html'))
        # password = request.get_json()["password"]


# web pages

@app.route('/add', methods=['POST'])
def add_web():
    return render_template("add.html")
