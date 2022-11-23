# Django Images App

## Description
The project is a backend REST API built with TDD (Test Driven Development) process approach.

## Live preview

https://www.youtube.com/watch?v=-L4VRQbty34

**Django Images App handles:**

* Registration part has been skipped. It is assumed that users are created via the admin panel

* User token authentication

* Uploading images in .png and .jpg format via HTTP request

* Depending on account type user is allowed to:

    * **Basic**

        * Get a link to a thumbnail that's 200px in height

    * **Premium**

        * Get a link to a thumbnail that's 200px and 400px in height
        * Get a link to originally uploaded image

    * **Enterprise**

        * Get a link to a thumbnail that's 200px and 400px in height
        * Get a link to originally uploaded image
        * Get ability to fetch a link to the binary image that expires after a number of seconds (User can specify in range between 300 and 30000 seconds. Value has to be multiplication of 300 seconds).

* Creating customized account types (Admin)

**Technology stack used to create a project:**

* **Development**

    Python, Django 4, Django Rest Framework, Docker, Celery, Redis

* **Database**

    PostgreSQL

* **Test and Lint**

    Django's unit tests, flake8 (PEP8)

* **Documentation**

    drf-spectacular, Swagger
***
## Running the app

Requirements:

macOS, Linux or Windows machine capable of running Docker (This excludes Windows 10 Home)

In terminal/bash

    git clone https://github.com/jakeinrock/Django-Images-App.git

**In project's root directory create ".env" file. There is an example ".env" file in project called ".env.sample". You can just copy-paste it's content.**

To run the app, navigate to the project's root directory and run the following command:

    docker-compose up

When the app building process is finished you can access it at:

    http://127.0.0.1:8000/

Swagger's app documentation is available at:

    http://127.0.0.1:8000/docs

***
## Navigating through the app

Creating superuser:

    docker-compose run --rm app sh -c "python manage.py createsuperuser"

Admin console is available at:

    http://127.0.0.1:8000/admin

Testing:

    docker-compose run --rm app sh -c "python manage.py test"

Flake8 (PEP8):

    docker-compose run --rm app sh -c "flake8"

There are five containers running after deploying the app:

* App
* DB
* Celery
* Celery-beat
* Redis

There is a periodic task (deleting expired links) created with Celery that is running every 5 minutes. In order to check it's logs perform:

    docker-compose logs 'celery'
    docker-compose logs 'celery-beat'

Other container's logs:

    docker-compose logs 'redis'
    docker-compose logs 'app'
    docker-compose logs 'db'


In order to check if image was succesfully added to docker container perform:

* Open terminal in your IDE
```
docker container ls
```
* Copy the containers NAME
```
docker exec -it <NAME> /bin/sh
```
* Navigate to images directory
```
cd ..
cd vol/web/media/images
```


***

## APIs
Quick overview about APIs and their endpoints.

 To get more details navigate to **/api/docs/** after deploying the app.

 * **User**

    * POST /user/token/

 * **Image**

    * GET, POST /image/

    * GET, DELETE /image/{id}/

    * POST /image/{id}/get-link/

 * **Schema**

    * POST /schema/
