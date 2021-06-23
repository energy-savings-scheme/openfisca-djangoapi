# openfisca-djangoapi

A database and Django webserver layer for serving OpenFisca rulesets

## Serving Locally and Deploying

#### Serving locally
This repo can be served in two ways:
1) Serve with a local development environment :heavy_check_mark:
   - Instructions in [local_deployment.md](docs/local_deployment.md)
2) Serve with Docker
   - Not recommended (this functionality is currently broken :warning:) :warning:
   - Instructions in [docker_deployment.md](docs/docker_deployment.md) 


#### Deploying
- This app can be deployed in a number of ways, we'll leave that up to you :wink:
- But, here are some considerations
   - This app uses a sqlite3 database. SQLite runs in memory, and backs up its data store in files on disk. Thus, a persistent filesystem is required - and platforms with ephemeral filesystems (such as Heroku) are not suitable.
   - The authors of this repo use AWS ElasticBeanstalk, because it has a persistent filesystem. AWS ElasticBeanstalk requires a few additional config files, located at `/.ebextensions` and `/.platform`. Additional info on ElasticBeanstalk can be found at [aws_elasticbeanstalk_instructions.md](docs/aws_elasticbeanstalk_instructions.md).
 

## Serve with a local development environment (recommended)
We recommend you build and serve this Django application locally.

To do this, follow these instructions: [local_deployment.md](docs/local_deployment.md).

## Serve with Docker
Not recommended (this functionality is currently broken :warning:)

To do this, follow these instructions: [docker_deployment.md](docs/docker_deployment.md).


## Awesome resources

See [additional_resources.md](docs/additional_resources.md) to learn more about all the different components used in this repository.
