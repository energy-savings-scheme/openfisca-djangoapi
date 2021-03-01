# openfisca-djangoapi

A database and Django webserver layer for serving OpenFisca rulesets


## Install and run locally (developers)

Clone this repo:
```
$ git clone git@github.com:RamParameswaran/openfisca-djangoapi.git
$ cd openfisca-djangoapi
```

Create virtual environment (python 3.7) and install requirements
```
# We're using `virtualenvwrapper` to create the virtual env here, but you can use any other virtual env tool...
# NOTE - make sure Python 3.7 is installed on your machine!

$ mkvirtualenv openfisca-django --python=python3.7
$ pip install -r services/app/requirements.txt
```

Run the Django server locally
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

Log into the admin backend
```
# On your browser naviate to http://localhost:8000/admin/
# Enter the superuser username and password that your just created

et voila!
```


## Docker

Init project:

```
$ cd openfisca-djangoapi
$ docker-compose build
```

Setup database:

```
$ docker-compose up -d postgres
$ docker-compose run app setup_db
```

Launch:

```
$ docker-compose up app
```

Launch Nginx _(optional)_:

```
$ docker-compose up web
```

_Now your django app is available on http://localhost, but it's optional for development_

## Container commands

The image has

Run a command:

```
$ docker-compose run app <command>
```

Available commands:

| Command  | Description                                                                     |
| -------- | ------------------------------------------------------------------------------- |
| dev      | Start a normal Django development server                                        |
| bash     | Start a bash shell                                                              |
| manage   | Start manage.py                                                                 |
| setup_db | Setup the initial database. Configure _$POSTGRES_DB_NAME_ in docker-compose.yml |
| lint     | Run pylint                                                                      |
| python   | Run a python command                                                            |
| shell    | Start a Django Python shell                                                     |
| uwsgi    | Run uwsgi server                                                                |
| help     | Show this message                                                               |

### Create a Django app

```
$ docker-compose run app manage startapp myapp
```

### Create a super user

```
$ docker-compose run app manage createsuperuser
```

## Awesome resources

Useful awesome list to learn more about all the different components used in this repository.

- [Docker](https://github.com/veggiemonk/awesome-docker)
- [Django](https://gitlab.com/rosarior/awesome-django)
- [Python](https://github.com/vinta/awesome-python)
- [Nginx](https://github.com/agile6v/awesome-nginx)
- [AWS](https://github.com/donnemartin/awesome-aws)

## Useful links

- [Docker Hub Python](https://hub.docker.com/_/python/)
- [Docker Hub Postgres](https://hub.docker.com/_/postgres/)
- [Docker compose Postgres environment variables](http://stackoverflow.com/questions/29580798/docker-compose-environment-variables)
- [Quickstart: Docker Compose and Django](https://docs.docker.com/compose/django/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
