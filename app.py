from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Query

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/wishlist.db'
app.debug = True
db = SQLAlchemy(app)

class User(db.Model):
    """This is the user class to hold info about each user and store into a database"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    wishlist = db.relationship('Wishlist', backref='user')

class Wishlist(db.Model):
    """Wishlist Class: hold info about each item in the wishlist"""
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    wishlist_name = db.Column(db.String(40), unique=True, nullable=False)
    content = db.relationship('Content', backref='wishlist')
    user_id = db.Column(db.Integer, ForeignKey('user.id'))


class Content(db.Model):
    """ Holds all content to the specific wishlist """
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    wishlist_id = db.Column(db.Integer, ForeignKey('wishlist.id'))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/createaccount')
def createaccount():
    return render_template('createAccount.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/wishlist')
def wishlist():

    # user1 = User(username="Adam", password="Apple")
    # db.session.add(user1)
    # db.session.commit()

    # #wishlist1 = Wishlist(wishlist_name="Adam's", content="Chili", user=user1)
    # wishlist1 = Wishlist(wishlist_name="Adams's", user=user1)
    # db.session.add(wishlist1)
    # db.session.commit()

    # content1 = Content(content="Chili", wishlist=wishlist1)
    # db.session.add(content1)
    # db.session.commit()

    data_wishlist = Wishlist.query.all()
    data_content = Content.query.all()
    return render_template('wishlist.html', data_wishlist=data_wishlist, data_content=data_content)

if __name__ == '__main__':
    app.run()
