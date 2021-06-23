## Install and run locally with Docker :house_with_garden:

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

#### Install docker and docker-compose

Install docker and docker-compose on your machine (if you don't already have it installed):
- docker: https://docs.docker.com/get-docker/
- docker-compose: https://docs.docker.com/compose/install/


#### Build the Docker image

Check config parameters:
```
# Some config params are seting in the `docker-compose.yml` file
# The most relevant are the `app->environment` variables such as "OPENFISCA_API_URL" and "PORT"
# Change these as necessary.

```
Init project:

```
$ cd openfisca-djangoapi
$ docker-compose build
```

#### Setup the Django database using Docker

Setup database:

```
$ docker-compose run app setup_db
$ docker-compose run app fetch_data
```


#### Serve the Django application using Docker

Launch:

```
$ docker-compose up app
```

_Now your django app is available on http://localhost:8000_


### ADDITIONAL FUNCTIONALITY

#### Docker Container commands

You can run Django and bash command in the Docker container:

```
$ docker-compose run app <command>
```

Available commands:

| Command  | Description                                                                     |
| -------- | ------------------------------------------------------------------------------- |
| dev      | Start a normal Django development server                                        |
| bash     | Start a bash shell                                                              |
| manage   | Start manage.py                                                                 |
| setup_db | Setup the initial database. Any existing DB will be destroyed first.
| fetch_data | Ingests OpenFisca ruleset. Configure _$OPENFISCA_API_URL_ in docker-compose.yml |
| lint     | Run pylint                                                                      |
| python   | Run a python command                                                            |
| shell    | Start a Django Python shell                                                     |
| uwsgi    | Run uwsgi server                                                                |
| help     | Show this message                                                               |

#### Example: Create a Django superuser (to access the admin portal)

```
$ docker-compose run app manage createsuperuser
```

