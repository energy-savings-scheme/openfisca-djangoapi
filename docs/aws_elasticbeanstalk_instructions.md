## Deploying to AWS ElasticBeanstalk (EB) :earth_americas:

These instructions will help you:
1) Setup the EB command line interface (`EB CLI`)
2) Understand AWS credentials
3) Create a new EB application
4) Create new environment(s) for this app
5) Deploy updates to these environments

***

#### Ensure you have installed the AWS CLI and the EB CLI :computer:
- See: https://aws.amazon.com/cli/
- See: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html

#### Supply your AWS credentials in order to execute any commands :id:
- these credentials refer to your `aws_access_key_id` and `aws_secret_access_key` which you can create by logging into the [AWS IAM portal](https://console.aws.amazon.com/iam/home)

```
# To initialise your credentials in the AWS CLI on your computer, run the following command:
$ aws configure

# Enter your `aws_access_key_id` and `aws_secret_access_key` when prompted.
```

#### Create the EB application :wrench:
```
$ eb init -p docker <desired_application_name> -i
# Answer the prompts...
```


#### Create and deploy an environment :seedling:
You may have multiple environments (e.g. staging and production, or maybe even multiple environments for multiple OpenFisca rulesets...)
```
$ eb create <desired_environment_name> -v -i t3.micro -s

# `-i t3.micro`: refers to an AWS compute instance. This is cheapest CPU, and is sufficient for development and staging environments.
# `-s`: tells AWS to make this a `single` instance - i.e. one which only uses 1 CPU, and does not auto-scale.

# After a few minutes, the status report should show:
  2021-03-04 02:33:11    INFO    Instance deployment completed successfully.
  2021-03-04 02:33:24    INFO    Application available at <desired_environment_name>.asd-asdfghj.ap-southeast-2.elasticbeanstalk.com.
  2021-03-04 02:33:24    INFO    Successfully launched environment: <desired_environment_name>
```

#### Launch the environment :star:
```
$ eb open
```


