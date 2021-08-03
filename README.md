# MT-Test
MT test
Installation

Pip install -r requirements.txt

Change database settings from setting.py
'NAME': 'Studen_records',
'USER': 'root',
'PASSWORD': 'password',
'HOST': 'localhost',

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
