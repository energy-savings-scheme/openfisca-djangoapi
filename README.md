# openfisca-djangoapi

A database and Django webserver layer for serving OpenFisca rulesets


## Docker

> We recommend you use Docker for local development **and** deployment. This ensures parity between development and production environments.

<em>First ensure that the `OPENFISCA_API_URL` environment variable is correctly set in the file `docker-compose.yml`</em>

Install docker and docker-compose on your machine (if you don't already have it installed):
- docker: https://docs.docker.com/get-docker/
- docker-compose: https://docs.docker.com/compose/install/

Init project:

```
$ cd openfisca-djangoapi
$ docker-compose build
```

Setup database:

```
$ docker-compose run app setup_db
$ docker-compose run app fetch_data
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

### Container commands

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

## Awesome resources

See [additional_resources.md](docs/additional_resources.md) to learn more about all the different components used in this repository.

