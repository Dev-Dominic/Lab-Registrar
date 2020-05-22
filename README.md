# Lab Registrar

## Setup

It is required that both a node and flask server is ran at the same time. Node
is used to render the Vuejs framework components, while the flask server is used
to server API data.

### Environment Variables

**Note:** These should be set in .env file in project directory, these are **not optional**

- BASEDIR: Absolute Path to Lab-Registrar project folder
- APP: path to app BASEDIR\app
- DEBUG: sets flask debug mode
- SECRET_KEY: randomly generated secret key
- DB_NAME: name of postgresql test database
- DB_USER: name of user that has access to test database
_ DB_USER: user password
- DATABASE_URI: postgresql database uri

**.flaskenv**

- FLASK_ENVIRONMENT: This can either be development or production
- FLASK_APP: This is were flask run start the flask web application
- FLASK_DEBUG: Toggles debug mode for flask application

**Virtual Environment**
```bash

    $ python -m venv <venv-directory-name>
    $ source venv/bin/activate (Linux/Unix/MacOs)
    $ venv\Scripts\activate (Windows)

```

**Installing Dependencies and running Flask**
<br>
*Ensure virtual environment is activated*
```bash

    (venv) $ pip install -r requirements.txt
    (venv) $ flask run

```

**Installing Dependencies and running VueJs**
<br>
*Should be done in a different terminal instance*
```bash

    npm install
    npm run serve

```

**Generate Database**

Generates a test database and populates the database with the necessary tables
with data.

```bash

   (venv) $ python scripts/generate_testdb.py
   (venv) $ flask db upgrade
   (venv) $ python scripts/populate.py

```
