###Docker

### To create Docker Image for our project
docker-compose run web sh -c "django-admin startproject todolist ."

### To run the web application
docker-compose up

### To access admin panel, first migrate and create a user...
docker-compose run web sh -c "python manage.py makemigrations"

docker-compose run web sh -c "python manage.py migrate"

docker-compose run web sh -c "python manage.py createsuperuser"


### To start a todo application
docker-compose run web sh -c "python manage.py startapp todo"