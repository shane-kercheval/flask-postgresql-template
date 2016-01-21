from flask import flash, request, redirect, url_for
from flask import render_template
from app_factory import app, db
from models import User
from forms import LoginForm, RegistrationForm


@app.before_request
def before_request():
    """Connect to the database before each request."""
    # g = global object Flask uses for passing information to views/modules.
    # g.db = db
    # g.db.connect()
    pass


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    # g.db.close()
    return response


@app.route('/')
def home(name="default", test="default"):
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        add_to_database(User(email=form.email.data,
                             password=form.password.data))
        flash('registered')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login valid", category="success")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash("login not valid", category="fail")
    return render_template('login.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('internal_server_error.html', error=error), 500


def add_to_database(object):
    db.session.add(object)
    db.session.commit()

if __name__ == '__main__':
    print("DATABASE_URL: "+app.config['SQLALCHEMY_DATABASE_URI'])
    print("DEBUG: "+str(app.config['DEBUG']))
    app.run()
"""
When the Python interpreter reads a source file, it executes all of the code
found in it. Before executing the code, it will define a few special
variables. For example, if the python interpreter is running that module
(the source file) as the main program, it sets the special __name__ variable
to have a value "__main__". If this file is being imported from another
module, __name__ will be set to the module's name.

In the case of your script, let's assume that it's executing as the main
function, e.g. you said something like

python threading_example.py

on the command line. After setting up the special variables, it will execute
the import statement and load those modules. It will then evaluate the def
block, creating a function object and creating a variable called myfunction
that points to the function object. It will then read the if statement and
see that __name__ does equal "__main__", so it will execute the block shown
there.

One of the reasons for doing this is that sometimes you write a module
(a .py file) where it can be executed directly. Alternatively, it can also be
imported and used in another module. By doing the main check, you can have
that code only execute when you want to run the module as a program and not
have it execute when someone just wants to import your module and call your
functions themselves.
http://stackoverflow.com/questions/419163/what-does-if-name-main-do
"""
