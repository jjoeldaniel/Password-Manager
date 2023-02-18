from flask import Flask, request, jsonify, render_template
app = Flask(__name__, template_folder = "../templates")
import db

@app.route('/', methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def get_account():
    #if the combo doesnt exist 
    username = request.get_json()["username"]
    if(user_is_registered(username)):
        return redirect(url_for('web.html'))
    else:
        return redirect(url_for('signup.html'))
       # password = request.get_json()["password"]


# web pages

@app.route('/add', methods = ['POST'])
def add_web():
    #the 
    

       




        