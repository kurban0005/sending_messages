run:
	python main/manage.py runserver

bot:
	python main/manage.py run_bot

test:
	python main/manage.py test

migrate:
	python main/manage.py makemigrations main_app
	python main/manage.py makemigrations users_app
	python main/manage.py makemigrations
	python main/manage.py migrate


freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

collectstatic:
	python main/manage.py collectstatic

flush:
	python main/manage.py flush

superuser:
	python main/manage.py createsuperuser


