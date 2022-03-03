<!-- ABOUT THE PROJECT -->
## About The Project
`connected` app is a service that checks whether two "developers" are fully connected.

Given a pair of developer handles they are considered connected if:
● They follow each other on Twitter.
● They have at least a Github organization in common.

<!-- GETTING STARTED -->
## Getting Started
***
You can use docker and/or Makefile to run the project.
### Prerequisites
In order to run the project you will need the following:
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/)
* [GNU Make](https://www.gnu.org/software/make/)

## How to run the project
***
1. Rewrite **.env.example** to your own **.env** with the necessary credentials.
2. Execute make up to bring all the project up to life:
```bash
make up
```
3. Navigate [local-connected](http://localhost:8000/docs#/) to check docs
and try the API

## Run test suite
***
Execute ```make test``` to run all the tests

## Additional tools
Execute ```make psql``` to have psql terminal to postgres
Execute ```make bash``` to have shell into app service.
