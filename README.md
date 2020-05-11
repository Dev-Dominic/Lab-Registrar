# Lab Registrar

## Setup

### Environment Variables 

**Note:** These should be set in .env file, these are **not optional**

- BASEDIR: Absolute Path to Lab-Registrar project folder
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
    $ . venv\Scripts\activate (Windows)

```

**Installing Dependencies and running Flask**
<br>
*Ensure virtual environment is activated*
```bash
    
    (venv) $ pip install -r requirements.txt
    (venv) $ flask run 

```

