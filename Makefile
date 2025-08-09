run:
	python main/manage.py runserver

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

admin:
	python main/manage.py createsuperuser

chat:
	python main/manage.py run_chat

bot:
	python main/manage.py run_bot