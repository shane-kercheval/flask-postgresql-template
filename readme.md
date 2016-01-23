Flask Template (Postgres & Heroku)
==================================

Note
----
- while this is designed to use Postgres and run on Heroku, I assume it can run on other platforms and use other database technologies with basic modifications.
- development was done on OS X

Getting Started
---------------
- download source, commit to whatever git repository you set up (assumes GitHub)
    - you may need to change
        - runtime.txt
        - Procfile.txt

**postgres**
- install http://postgresapp.com (OS X)
- run export command in terminal

        export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin

- start postgresapp to make sure it works and the server starts
- open psql from app
- in psql terminal, create the database you want to use in the site, config defaults the db url to example_site. USE:

        CREATE DATABASE example_site;
        \connect example_site;

- the DATABASE_URL value in config.py is defaulted so that if none exists, it returns 'example_site'
- So, when pushed to Heroku you must install the [postgres add-on](https://elements.heroku.com/addons/heroku-postgresql) and set the config value (mentioned below); depending on the order of steps, it's possible that Heroku auto-detects postgres and installs it for you.

**venv:**
- start venv using os x terminal

        source path-to-ven/bin/activate

- update venv to requirements using

        pip install -r requirements.txt

- any time you update venv via pip, save to requirements using

        pip freeze > requirements.txt

- if you get "Error: pg_config executable not found."
    - run this in terminal and retry: "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"

**running, tests, and initial data**
- run tests locally using terminal command:

        python -m unittest tests/test_app.py

- add data to database using terminal command:

        python initialize_db.py

- confirm data is in database using following command in psql terminal window

        select * from users;

- run locally using terminal command:

        python app.py

- in browser, go to http://127.0.0.1:5000/ ... you should see the site
- commit/push to git repository

**heroku**
- sign up for [heroku](https://www.heroku.com/) account
- download/install Heroku Toolbelt: https://devcenter.heroku.com/articles/getting-started-with-python#set-up
- log in to Heroku via toolbelt/terminal:

        heroku login

- create heroku app
    - terminal cd path-to-project
    - create app command: 
    
        heroku create [app name] 
        e.g. 'heroku create flask-postgresql-template'
    
- Heroku has an excellent ["Getting Started" Guide](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).
- Heroku recognizes the app as a Python app by the existence of a requirements.txt file in the root directory. For your own apps, you can create one by running pip freeze.
- you can use GitHub and Heroku at the same time; adding the 'remote' from the setup tutorial above doesn't overwrite git, it adds another
- once you have hadded 'heroku' remote, deploy code:

        git push heroku master

- ensure it worked:

        heroku open

- this should have automatically added postgres add-in to your app (Heroku auto-detects the requirement), but verify on heroku dashboard
    - Heroku automatically adds DATABASE_URL to the config settings which makes it available to os.evnironment
- add the following config config var to your Heroku app (either via command or heroku website)

        config name: APP_SETTINGS
        config value: config.ProductionConfig 

- try running Heroku locally with 

        heroku local

- optionally connect heroku to github to enable automatic deployments

- to run a different computer, follow same steps, then enable the deployment using

        heroku git:remote -a [heroku app name]
        e.g. "heroku git:remote -a flask-postgresql-template"

- then do:

        git push heroku master
        heroku open

Migrations
----------
- as your database changes, you need to migrate the changes to other (e.g. production) databases
- view remote heroku database using:

        heroku pg:psql --app flask-postgresql-template DATABASE

-may have to run "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"

- Alembic automatically creates/tracks database migration records from the changes in the SQLAchemy models, and allows us to upgrade/downgrade to specific versions.
- Flask-Migrate ([official documentation](https://flask-migrate.readthedocs.org/en/latest/)) is an extension created for SQLAlchemy that works with Flask Script / Alembic; *MigrateCommand added to manage.py*

- to see the migration command options, use:

        python manage.py db

- to start tracking database changes, use:

        python manage.py db init

- the previous command creates /migrations/ folder
- create the initial migration: (causes Alembic to scan SQLAlchemy all table/column changes)

        python manage.py db migrate -m "initial migration"

- make sure to do this with an empty local database, if there are existing tables, they won't be added to the migration
- to apply migration to another database, run

        python manage.py db upgrade

- view migration history:

        python manage.py db history

- when switching computers, blow away the database (drop all tables) and do 'upgrade' and then 'migrate'

- push db provisions to heroku, using:

        heroku run python manage.py db upgrade --app [APP]
        e.g. heroku run python manage.py db upgrade --app flask-postgresql-template

-**MAKE SURE ALL MIGRATIONS/CODE-CHANGES ARE PUSHED TO REMOTE BEFORE RUNNING, THIS RUNS OFF OF REMOTE SOURCES**


Authentication
--------------
- user authentication (login/register) is implemented using flask-login
    - documentation: https://flask-login.readthedocs.org/en/latest/
- technically, the classes we would want to [implement a few required methods and properties](http://flask-login.readthedocs.org/en/latest/#your-user-class)
    - but flask-login gives us [UserMixin](https://flask-login.readthedocs.org/en/latest/#flask.ext.login.UserMixin) which does this for us
    - I have not overrided the default UserMixin implementation
- I am currently enabling 'remember me' functionality by including 'remember=True' in the login_user call, in app.py
- **I don't know the specifics of HTTPS/SSL requirements, but Heroku says ['SSL Endpoint [paid add-on] is only useful for custom domains. All default appname.herokuapp.com domains are already SSL-enabled and can be accessed by using https, for example, https://appname.herokuapp.com.'](https://devcenter.heroku.com/articles/ssl-endpoint) **
    - I assume there is a way to redirect HTTP to HTTPS if needed, but have not investigated yet

Advanced Logging
---------------
- install 'papertrail' add-on
- open the heroku dashboard - "heroku addons:open papertrail"

MISC Notes
----------
- in models.py, we need to store passwords as LargeBinary. Seems unique to Postgres. 
