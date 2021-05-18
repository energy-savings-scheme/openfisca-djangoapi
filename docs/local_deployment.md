## Install and run locally (developers) :house_with_garden:

These instructions will help you:

1. Clone the repo to your local machine
2. Create a new virtual environment to install Python dependencies
3. Initialise the sqlite3 database
4. Create a Django Superuser (for accessing the Django Admin at http://localhost:8000/admin/)
5. Ingest OpenFisca data from the specified OpenFisca API URL
6. Serve the Django Webserver locally at http://localhost:8000/

---

#### Clone this repo :alien:

```
$ git clone git@github.com:RamParameswaran/openfisca-djangoapi.git
$ cd openfisca-djangoapi
```

#### Create virtual environment (python 3.7) and install requirements

```
# We're using `virtualenvwrapper` to create the virtual env here, but you can use any other virtual env tool...
# NOTE - make sure Python 3.7 is installed on your machine!

$ mkvirtualenv openfisca-django --python=python3.7
$ pip install -r services/app/requirements.txt
```

#### Run the Django server locally :snake:

```
# First try running the Django server locally
$ python app/manage.py runserver

# The webserver should return:

System check identified no issues (0 silenced).

    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    March 01, 2021 - 03:29:31
    Django version 3.1.7, using settings 'config.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

# Next run a database migration and create an admin user
$ python app/manage.py migrate
$ python app/manage.py createsuperuser
# Enter usename and password

# Launch the webserver locally
$ python app/manage.py runserver
```

#### Ingest an OpenFisca ruleset into the database :balance_scale:

```
# By default the database will be empty. To ingest data from an OpenFisca API:

# 1) You must set the `OPENFISCA_API_URL` environment variable in a `.env` file in the project root directory
# e.g. OPENFISCA_API_URL=https://dpie-ess-dev.herokuapp.com

# 2) run the Django `fetch_all` command
$ python app/manage.py fetch_all

```

#### Log into the admin backend :thumbsup:

```
# Launch the webserver locally
$ python app/manage.py runserver

# In your browser naviate to http://localhost:8000/admin/
# Enter the superuser username and password that your just created

et voila!
```
