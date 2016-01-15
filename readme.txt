=====SETUP=================
NOTE: development was done on OS X, there may be different installations/etc. on other systems

- download source, put in whatever git repository you set up
    - you may need to change
        - runtime.txt
        - Procfile.txt

- install http://postgresapp.com (OS X)
- run "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"
- start postgresapp to make sure it works and the server starts
- open psql from app
- in psql terminal, create the database you want to use in the site, config defaults the db url to example_site. USE:
        CREATE DATABASE example_site;
        \connect example_site;
    - defaulted DATABASE_URL os so that if none exists, it returns the above. Means it might work locally but fail when pushed to Heroku if config variable isn't set
- start venv ('source path-to-ven/bin/activate') (using os x terminal, not psql)
- update venv to requirements using 'pip install -r requirements.txt'
    - any time you update venv via pip, save to requirements using 'pip freeze > requirements.txt'
    - if you get "Error: pg_config executable not found."
        - run this in terminal and retry: "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"

- run tests locally using 'python -m unittest tests/test_app.py' in terminal
- add data to database using 'python initialize_db.py' in terminal
- confirm data is in database using 'select * from users;' in psql
- run locally using 'python app.py'
- in browser, go to 'http://127.0.0.1:5000/' ... you should see the site

- commit/push to git repository


- download/install Heroku Toolbelt: https://devcenter.heroku.com/articles/getting-started-with-python#set-up
- log in to Heroku via toolbelt/terminal: 'heroku login'
- create heroku app
    - terminal cd path-to-project
    - create app: 'heroku create [app name]' e.g. 'heroku create flask-postgresql-template'
        Heroku recognizes an app as a Python app by the existence of a requirements.txt file in the root directory. For your own apps, you can create one by running pip freeze.
        you can use GitHub and Heroku at the same time, added the remote from the setup tutorial above doesn't overwrite git, it adds another
- deploy code: 'git push heroku master'
- ensure it worked: 'heroku open'
    - this should have automatically added postgres add-in to your app, but verify on heroku dashboard
        - Heroku automatically adds DATABASE_URL to the config settings which makes it available to os.evnironment
- add APP_SETTINGS=config.ProductionConfig to config in Heroku
- try running Heroku locally with "heroku local"

- optionally connect heroku to github to enable automatic deployments

- to run a different computer, follow same steps, then enable the deployment using "heroku git:remote -a [heroku app name]"
    - e.g. "heroku git:remote -a flask-postgresql-template"
    - then do:
        git push heroku master
        heroku open

=====MIGRATIONS============
- Alembic automatically creates/tracks database migration records from the changes in the SQLAchemy models, and allows us to upgrade/downgrade to specific versions.
- Flask-Migrate is an extension created for SQLAlchemy that works iwht Flask Script / Alembic; MigrateCommand added to manage.py
- "python manage.py db" - gives command options
- "python manage.py db init" - start tracking changes
    - creates /migrations/ folder
- "python manage.py db migrate -m "initial migration"" - initial migration; causes Alembic to scan SQLAlchemy and finall all table/column changes
- to apply migration to another database, run
    - "python manage.py db upgrade"
- view history: "python manage.py db history"


- push db provisions to heroku: "heroku run python manage.py migrate"
"heroku run python manage.py db upgrade --app [APP]"
"heroku run python manage.py db upgrade --app flask-postgresql-template"
===========================
