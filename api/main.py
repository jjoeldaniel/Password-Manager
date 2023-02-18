from flask import Flask, request, redirect, render_template, url_for
import db
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def get_account():

    username = request.get_json()["username"]
    password = request.get_json()["password"]

    if db.user_is_registered(username):

        # validate password
        if db.validate_password(username, password):
            return render_template('web.html')
        else:
            # password is incorrect
            return render_template('index.html')

    else:
        return render_template('signup.html')


@app.route('/add', methods=['POST'])
def add_web():
    return render_template("add.html")
