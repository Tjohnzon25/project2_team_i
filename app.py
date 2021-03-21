from flask import Flask, render_template, request, url_for, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/account.db'
db = SQLAlchemy(app)


class User(db.Model):
    """This is the user class to hold info about each user and store into a database"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    wishlist = db.relationship("Wishlist", backref='user')


class Wishlist(db.Model):
    """Wishlist Class: hold info about each item in the wishlist"""
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    wishlist_name = db.Column(db.String(40), unique=True, nullable=False)
    content = db.relationship("Content", backref='wishlist')
    user_id = db.Column(db.Integer, ForeignKey('user.id'))


class Content(db.Model):
    """ Holds all content to the specific wishlist """
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    wishlist_id = db.Column(db.Integer, ForeignKey('wishlist.id'))


"""
    -How to add to DB:
        user1 = User(username="Bob", password="Dillan")
        db.session.add(user1)
        db.session.commit()
            
            -ADDS THE WISHLIST TO THE USER-
        wishlist1 = Wishlist(wishlist_name="One", content="Chili", user=user1)
        db.session.add(wishlist1)
        db.session.commit()

            -ADDS THE CONTENT TO THE WISHLIST-
        content = Content(content="Chili", wishlist=wishlist1)
        db.session.add(content)
        db.session.commit()

        can also:
            some_user = User.query.filter_by(username="Timmy").first()
            wishlist2 = Wishlist(wishlist_name="Two", content="Beans", user=some_user)
"""

def wishlist_serializer(wishlist):
    return{
        'id': wishlist.id,
        'user_name': wishlist.wishlist_name,
        'content': wishlist.content
    }


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    request_method = request.method
    if request.method == 'POST':
        first_name = request.form['username']
        print('-----------')
        print(request.form)
        print('-----------')
        return redirect(url_for('name', first_name=first_name))
    return render_template('login.html', request_method=request_method)


@app.route('/name/<string:first_name>', methods=['GET', 'POST'])
def name(first_name):
    request_method = request.method
    if request.method == 'POST':
        log_out = request.form['log_out_button']
        print('-----------')
        print(request.form)
        print('-----------')
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


@app.route('/api')
def index():
    return jsonify([*map(wishlist_serializer, Wishlist.query.all())])


if __name__ == '__main__':
    app.run()
