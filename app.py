from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Query

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/final.db'
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
    logged_in = db.Column(db.Integer, nullable=False)



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
        return redirect('/')
    return render_template('todo.html', form=todo_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    request_method = request.method
    if request.method == 'POST':
        #first_name = request.form['create_account_button']
        first_name = request.form['username']
        users = User.query.all()
        check = False
        for i in users:
            if(i.username == first_name):
                check = True
                i.logged_in = 1
                db.session.commit()
        if check:
            return redirect(url_for('name', first_name=first_name))
    return render_template('login.html', request_method=request_method)


@app.route('/name/<string:first_name>', methods=['GET', 'POST'])
def name(first_name):
    request_method = request.method
    if request.method == 'POST':
        if request.form['button'] == "Log Out":
            users = User.query.all()
            for i in users:
                if(i.username == first_name):
                    i.logged_in = 0
                    db.session.commit()
            return redirect(url_for('login'))
        elif request.form['button'] == "See Wishlists":
            data_users = User.query.all()
            data_wishlist = Wishlist.query.all()
            data_content = Content.query.all()
            user = first_name
            return render_template('user_wishlists.html', user=user, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content)
        elif request.form['button'] == "Create Wishlist":
            data_users = User.query.all()
            data_wishlist = Wishlist.query.all()
            return render_template('create_wishlist.html', user=first_name, data_users=data_users, data_wishlist=data_wishlist)
    return render_template('profile.html')


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        new_username = request.form['username']
        exists = db.session.query(User.username).filter_by(username=new_username).first()
        if exists == None:
            new_password = request.form['password']
            #new_password = request.form.get('password', None)
            if new_password == "":
                error_message = "Password cannot be blank"
                return render_template("createaccount.html", error_message=error_message)
            else:
                newUser = User(username=new_username, password=new_password, logged_in=0)
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for("login"))
        else:
            error_message = "User already exists"
            return render_template("createaccount.html", error_message=error_message)
    else:
        error_message = " "
        return render_template('createAccount.html', error_message=error_message)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == "POST":
        user_remove = request.form['id']
        temp_user = User.query.get(user_remove)
        db.session.delete(temp_user)
        db.session.commit()
        data_users = User.query.all()
        return render_template('adminView.html', data_users=data_users)
    else:    
        data_users = User.query.all()    
        return render_template('adminView.html', data_users=data_users)

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/wishlist')
def wishlist():
    data_wishlist = Wishlist.query.all()
    data_content = Content.query.all()
    return render_template('wishlist.html', data_wishlist=data_wishlist, data_content=data_content)


@app.route('/userwishlist', methods=["GET", "POST"])
def user_wishlist():   

    data_users = User.query.all()
    data_wishlist = Wishlist.query.all()
    data_content = Content.query.all()

    if request.method == "POST":

        theWishlist = request.form['wishlist']
        theContent = request.form['new_content']

        checkContent = False
        checkWishlist = False
        error = ""

        user = ""

        if request.form['button'] == "Go Back":
            
            allUsers = User.query.all()

            for i in allUsers:
                if i.logged_in == 1:
                    return redirect(url_for('name', first_name=i.username))

        if request.form['button'] == "Delete Content":
            for i in data_users:
                if i.logged_in == 1:
                    
                    user = i.username

                    if theWishlist == "" or theContent == "":
                        error = "Field is empty"
                        return render_template('user_wishlists.html', user=i.username, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content, error=error)

                    for j in data_wishlist:
                        if theWishlist == j.wishlist_name:
                            checkWishlist = True
                            for h in data_content:
                                if theContent == h.content:
                                    checkContent = True

            if checkWishlist == False:
                error = "Wishlist doesn't exist"
                return render_template('user_wishlists.html', user=user, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content, error=error)


            if checkContent == False:
                error = "Content doesn't exist"
                return render_template('user_wishlists.html', user=user, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content, error=error)
            else:
                content = Content.query.filter_by(content=theContent).first()
                db.session.delete(content)
                db.session.commit()

                allContent = Content.query.all()

                return render_template('user_wishlists.html', user=user, data_users=data_users, data_wishlist=data_wishlist, data_content=allContent)
        else: 

            #checks to make sure you can add the content
            for i in data_users:
                if i.logged_in == 1:

                    if theWishlist == "" or theContent == "":
                        error = "Field is empty"
                        return render_template('user_wishlists.html', user=i.username, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content, error=error)

                    for j in data_wishlist:
                        if theWishlist == j.wishlist_name:
                            checkWishlist = True
                            for h in data_content:
                                if theContent == h.content:
                                    checkContent = True

            if checkWishlist == False:
                error = "Wishlist doesn't Exist"

                # returning the right data
                for i in data_users:
                    if i.logged_in == 1:
                        return render_template('user_wishlists.html', user=i.username, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content,error=error)

            elif checkContent:
                error = "Content already exists"

                # returning the right data
                for i in data_users:
                    if i.logged_in == 1:
                        return render_template('user_wishlists.html', user=i.username, data_users=data_users, data_wishlist=data_wishlist, data_content=data_content,error=error)

            else:
                for i in data_users:
                    if i.logged_in == 1:
                        for j in data_wishlist:
                            if theWishlist == j.wishlist_name:
                                content = Content(content=theContent, wishlist_id=j.id)
                                db.session.add(content)
                                db.session.commit()

                                contents = Content.query.all()

                                return render_template('user_wishlists.html', user=i.username, data_users=data_users, data_wishlist=data_wishlist, data_content=contents)


    return render_template('user_wishlists.html', data_users=data_users, data_wishlist=data_wishlist)


@app.route('/create_wishlist', methods=["GET", "POST"])
def create_wishlist():

    if request.method == "POST":
        new_wishlist = request.form['new_wishlist']

        allUsers = User.query.all()
        allWishlists = Wishlist.query.all()
        allContent = Content.query.all()

        if request.form['button'] == "Go Back":
            for i in allUsers:
                if i.logged_in == 1:
                    return redirect(url_for('name', first_name=i.username))


        if new_wishlist == "":
            error = "Field is empty"
            return render_template('create_wishlist.html', error=error)

        error = ""

        check = True

        if request.form['button'] == "Add":

            for users in allUsers:
                if users.logged_in == 1:

                    for j in allWishlists:
                        if j.wishlist_name == new_wishlist:
                            check = False

                    if check:
                        wishlist = Wishlist(wishlist_name=new_wishlist, user_id=users.id)
                        db.session.add(wishlist)
                        db.session.commit()
                        return redirect(url_for('name', first_name=users.username))
                    else:
                        error = "Wishlist name already exists"
                        return render_template('create_wishlist.html', error=error)

        elif request.form['button'] == "Delete":

            for users in allUsers:
                if users.logged_in == 1:
                    for j in allWishlists:
                        if j.wishlist_name == new_wishlist and users.id == j.user_id:
                            for i in allContent:
                                if i.wishlist_id == j.id:
                                    db.session.delete(i)
                                    db.session.commit()
                            db.session.delete(j)
                            db.session.commit()
                            return redirect(url_for('name', first_name=users.username))

            error = "Wishlist doesn't exist"


    return render_template('create_wishlist.html', error=error)

        
if __name__ == '__main__':
    app.run()
