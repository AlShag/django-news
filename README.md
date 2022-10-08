# Django News

## Installation and run (Ubuntu)

```bash
cd django_news

python -m venv venv

source venv/bin/activate

pip install -r -requirements.txt

python manage.py makemigrations && python manage.py migrate

python manage.py createsuperuser --username=admin --email=admin@ex.com

python manage.py runserver 

# localhost:8000 - Frontend UI,
# localhost:8000/api/ - REST API UI
```
