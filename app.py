from flask import Flask, render_template, request, url_for, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Query
#from forms import Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/wishlist.db'
app.config['SECRET_KEY'] = 'password'
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
    content = db.Column(db.String(50), unique=True, nullable=False)
    wishlist_id = db.Column(db.Integer, ForeignKey('wishlist.id'))


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    request_method = request.method
    if request.method == 'POST':
        if request.form['button'] == "Log In":
            return redirect(url_for('login'))
        elif request.form['button'] == "Create Account":
            return redirect(url_for('createaccount'))
    return render_template('index.html')


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    todo_form = Todo()
    if todo_form.validate_on_submit():
        print(todo_form.content.data)
        return redirect('/')
    return render_template('todo.html', form=todo_form)


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

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        newUser = User(username=new_username, password=new_password)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for("login")
    else:     
        return render_template('createAccount.html')

@app.route('/admin')
def admin():
    data_wishlist = Wishlist.query.all()
    return render_template('adminView.html', data_wishlist=data_wishlist)

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/wishlist') # could be the admin page to show all users, wishlists, and content
def wishlist():
    data_wishlist = Wishlist.query.all()
    data_content = Content.query.all()
    return render_template('wishlist.html', data_wishlist=data_wishlist, data_content=data_content)


@app.route('/userwishlist', methods=["GET", "POST"])
def user_wishlist():

    # make it so that it only is for the user that is logged in (when tyler finishes)

    if request.method == "POST":
        new_wishlist_name = request.form.get("new_wishlist_name")

        # checks if the entry is empty or blank space
        if new_wishlist_name and new_wishlist_name.strip(): 
            newWishlist = Wishlist(wishlist_name=new_wishlist_name, user_id=1) #change user_id later when login is done
            db.session.add(newWishlist)
            db.session.commit()
        
    data_users = User.query.all()
    data_wishlist = Wishlist.query.all()
    return render_template('user_wishlists.html', data_users=data_users, data_wishlist=data_wishlist)


@app.route('/display_content.html', methods=["GET", "POST"])
def display_content():

    if request.method == "POST":
        new_content = request.form.get("new_content")

        check_content = Content.query.all()
        check_wishlist = Wishlist.query.all()

        if new_content and new_content.strip():
            
            check = True

            for theContent in check_content: #make sure to only do this in the specific wishlist
                if new_content == theContent.content:
                    check = False

            if check:
                newContent = Content(content=new_content, wishlist_id=1) #change wishlist_id when login is done
                db.session.add(newContent)
                db.session.commit()

    # check if the data is NULL before printing (maybe dont have to)
    data_wishlist = Wishlist.query.all()
    data_content = Content.query.all()

    return render_template('display_content.html', data_wishlist=data_wishlist, data_content=data_content)

        
if __name__ == '__main__':
    app.run()
