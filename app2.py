import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_addr']
        height = request.form['height_num']

        return render_template('success.html')


app.run(debug=True)
