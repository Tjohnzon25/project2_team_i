from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/account.db'
db = SQLAlchemy(app)

"""
    HOW TO USE THE DATABASE:
    -Create the User holding the information
    -Then: db.session.add(User)
    -Then: db.commit()
    
    How to get all the information from the db: users = User.query.all(0
"""

class User(db.Model):
    """This is the user class to hold info about each user and store into a database"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    # wishlist = db.relationship('Wishlist', backref='user', lazy="dynamic")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User('{self.username,}', '{self.password}')"


# class Wishlist(db.Model):
#     """Wishlist Class: hold info about each item in the wishlist"""
#     __tablename__ = "wishlist"
#     id = db.Column(db.Integer, primary_key=True)
#     wishlist_name = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)  # this would be the item in the wishlist
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # to connect the wishlist to the user_id
#
#     def __repr__(self):
#         return f"Post('{self.wishlist_name,}')"


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
        return render_template('profile.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run()
