labbooks
========

The repo holds our labbook software (currently used by CLUSTOF, TOFFY, TOFFY2).

## Development

### Prepare

Make sure that `Node`, `npm`, `python` and `pip` are installed:

```shell
node --version
# > v18.12
npm --version
# > 8.19
python --version
# > 3.9
pip --version
# > 22.3
```

Create a virtual environment for python somewhere on your computer where all packages are installed
and activate it:

```shell
pip python3 -m venv labbooks-env

# On Windows, run:
labbooks-env\Scripts\activate.bat

# On Unix or MacOS, run:
source labbooks-env/bin/activate
```

Install all dependencies:

```shell
pip install -r requirements.txt
npm install

# creates database with required structure
python manage.py migrate --settings=labbooks.settings_local

# create a superuser (for you!, follow instructions)
python manage.py migrate --settings=labbooks.settings_local
```

### Start

```shell
python manage.py runserver --settings=labbooks.settings_local
```

## Build & Deploy

Nowadays, projects like this are build inside containers (think of them like virtual machines but
lighter). These containers can be tested on your local machine and then copied to the server.

We are using a _service_ with 3 containers:

- Django, with all the logic
- Postgres, the database
- nginx, as an entry point and static files server

You need to learn and install Docker and Docker-Compose. Then, a simple

```shell
docker-compose up -d
```

should do the job.

## And...

- Learn how to use **git**, [this](https://github.com/drkhsh/git-auf-suedtirolerisch)
  or [that](https://github.com/danielauener/git-auf-deutsch) might help.
- [Django Docs](https://docs.djangoproject.com) are sooooo good!