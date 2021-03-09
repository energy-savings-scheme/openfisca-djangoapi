# openfisca-djangoapi

A database and Django webserver layer for serving OpenFisca rulesets

## Serving Locally and Deploying

#### Serving locally
This repo can be served in two ways:
1) Serve with Docker :heavy_check_mark:
   - [See instructions](#serve-with-docker) :blue_book:
3) Serve with a local development environment :warning:
   - Not recommended! :warning:
   - Instructions in [local_deployment.md](docs/local_deployment.md) 


#### Deploying
- This app can be deployed in a number of ways, we'll leave that up to you :wink:
- But, here are some considerations
   - This app uses a sqlite3 database. SQLite runs in memory, and backs up its data store in files on disk. Therefore, deployment environments which have ephemeral filesystems (such as Heroku) are not suitable.
   - The authors of this repo use AWS ElasticBeanstalk, because it supports deploying from Docker images, and has a persistent filesystem. AWS ElasticBeanstalk requires a few additional config files, located at `/.ebextensions` and `/.platform`. Additional info on ElasticBeanstalk can be found at [aws_elasticbeanstalk_instructions.md](docs/aws_elasticbeanstalk_instructions.md).
 
## Serve with Docker

> We recommend you use Docker for local development **and** deployment. This ensures parity between development and production environments.

Install docker and docker-compose on your machine (if you don't already have it installed):
- docker: https://docs.docker.com/get-docker/
- docker-compose: https://docs.docker.com/compose/install/

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

Setup database:

```
$ docker-compose run app setup_db
$ docker-compose run app fetch_data
```

Launch:

```
$ docker-compose up app
```

_Now your django app is available on http://localhost:8000_

### Container commands

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

## Serve with a local development environment
Alternatively you can create a local development environment on which to launch this app.

To do this, follow these instructions: [local_deployment.md](docs/local_deployment.md).


## Awesome resources

See [additional_resources.md](docs/additional_resources.md) to learn more about all the different components used in this repository.

