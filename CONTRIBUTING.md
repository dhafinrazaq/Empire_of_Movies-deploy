# Contributing

## Tech Stacks

- Git
- Python
- Django
- HTML
- CSS
- Javascript
- Bootstrap
- Heroku (for deployment)
- PostgreSQL


## Local Installation
To activate a virtual enviromnent:
```bash
pipenv shell
```
To install all the requirements:
```bash
pip install -r requirements.txt
```
You may need to define .env file to declare API keys/other tokens (refer to [Where to get API keys/tokens](#where-to-get-api-keystokens)) as follows and fill the keys/tokens after the (`=`) sign (or by replacing the variables listed below on [settings.py](Empire_of_Movies/settings.py) to your keys/tokens):
```
export EMAIL_HOST_USER=
export EMAIL_HOST_PASSWORD=
export SECRET_KEY=
export DATABASE_USER=
export DATABASE_PASSWORD=
export DATABASE_NAME=
export TELEGRAM_API_KEY=
export OMDB_API_KEY=
export IMDB_API_KEY=
```
To migrate the tables on the installed apps to the database:
```bash
python manage.py migrate
```
To run the server:
```bash
python manage.py runserver
```

## Usage

Open http://127.0.0.1:8000 on browser 

## Other commands

To update the IMDb ratings of the existing movies in the Empire of Movies with the newest rating according to www.imdb.com:
```bash
python maintenance.py
```

## Problems that may be encountered

The Telegram bot might or might not be automatically ran when running the server with 
```bash
python manage.py runserver
```
If it is not ran automatically, use the command:
```bash
python bot.py
```
Other possible problem that may be faced could be solved by deleting/adding 
```python
updater.idle()
```
at the end of the [bot.py](bot.py) file

## Where to get API keys/tokens
- EMAIL_HOST_USER: Your gmail address
- EMAIL_HOST_PASSWORD: Your gmail password
- SECRET_KEY: Open python shell (`python` on terminal) and use the following commands:
```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
- DATABASE_USER: Your PostgreSQL database username
- DATABASE_PASSWORD: Your PostgreSQL database password
- DATABASE_NAME: Your PostgreSQL database name
- TELEGRAM_API_KEY: Retrieved from registering a bot on BotFather on Telegram, instructions [here](https://core.telegram.org/bots)
- OMDB_API_KEY: Retrieved from  [http://www.omdbapi.com/](http://www.omdbapi.com/)
- IMDB_API_KEY: Retrieved from  [https://rapidapi.com/IMDb-API/api/imdb-api1](https://rapidapi.com/IMDb-API/api/imdb-api1)

## Test
To run the tests defined in `test.py` on all apps:
```bash
python manage.py test
```
To run test on a specific app with name [app name]:
```bash
python manage.py test [app name]
```
For additional manual testing, refer to [the google docs](https://docs.google.com/document/d/1pOSwCdyFMAxtRub4eaxoMzqtJSn1a60-z09THcM-m1c/edit?usp=sharing). You can also add a suggestion on our manual testing by writing it on [the google docs](https://docs.google.com/document/d/1pOSwCdyFMAxtRub4eaxoMzqtJSn1a60-z09THcM-m1c/edit?usp=sharing).

## Proposing a Change
To propose a change, you can [fill an issue](https://github.com/dhafinrazaq/Empire_of_Movies-deploy/issues/new?template=FEATURE_REQUEST.md)
