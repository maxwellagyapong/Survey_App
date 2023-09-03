# Survey APP
Survey Application

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Commands](#commands)
* [App endpoints](#app-endpoints)
* [Link to public repo](#public-repo)
* [API Documentation](#api-documentation)


## General info
Django survey application with the following as main features:

* Survey create/edit page for Survey Admin
* Survey listings page for Survey Admin
* Survey instance page, for Survey Participants to complete and submit
* Survey data tabulation page for Survey Admin to view all Survey Participants submissions.


## Technologies
* Python
* Django
* PostgreSQL
* Docker

### Setup
## Installation on Linux and Mac OS
* [Follow the guide here](https://help.github.com/articles/fork-a-repo) on how to clone or fork a repo
* [Follow the guide here](https://docs.docker.com/engine/install/) on how to install and run docker
* To run application with docker
```
docker-compose up --build
```
  
* Copy the IP address provided once your server has completed building the site. (It will say something like >> Serving at http://0.0.0.0:8000).
* Open the address in the browser

## Commands
Open docker bash with 
```
docker ps
docker exec -it <CONTAINER_NAME> bash
```
In our case, default container name is "survey"
* To run migrations
```
python manage.py makemigrations 
python manage.py migrate

```
* To run automated tests
```
python manage.py test

```

## App Endpoints
* /survey/welcome/ - SA dashboard - returns a list of all surveys created by SA
* /survey/create/ - create a new survey
* /survey/{survey_name}/ - survey form - take survey, returns a single survey
* /survey/{survey_name}/update/ - update a survey(change survey name)
* /survey/{survey_name}/delete/ - delete a survey
* /survey/{survey_name}/result/ - view survey result
* /survey/{survey_name}/text/ - add a text input question
* /survey/{survey_name}/text/{question_id} - update a text input question
* survey/{survey_name}/number/ - add a number input question
* survey/{survey_name}/number/{question_id} - update a number input question 
* survey/{survey_name}/image/ - add an image input question
* survey/{survey_name}/image/{question_id} - update an image input question
* survey/{survey_name}/file/ - add a file input question
* survey/{survey_name}/file/{question_id} - update a file input question
* survey/{survey_name}/single/ - add a single select question
* survey/{survey_name}/single/{question_id} - update a single select question
* survey/{survey_name}/single/{question_id}/{option} - add an option to a single select quesiton
* survey/{survey_name}/single/{question_id}/{option}/{option_id} - update a single select option
* /account/login/ - login to see SA dashboard
* /account/logout/ - logout of SA dashboard