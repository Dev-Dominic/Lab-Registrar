# Final Presentation Diagrams

## Package Diagram

1. api
    - common (endpoints that are not specific to either web or local)
    - web (contains all the web API accesiable endpoints)
    - local (contains all the local API accesiable endpoints)

2. classes
    - controllers
    - models

3. web
    - node_modules
    - public
    - src
        - components
        - plugins
        - router

**Dependencies**

- controllers => models

- api => controllers

- web => api

## Component Diagram

1. Database Management
    - models
    - controllers

2. API

3. web

## Deployment Diagram

1. Heroku webserver, Artefacts:
    - VueJs web-front:
        - package.json
        - package-lock.json
        - vue.config.js
        - babel.config.js
    - flask api
        - .env
        - .flaskenv
        - requirements.txt
        - app/__init__.py
    - migrations
        - alembic.ini
        - env.py
        - versions

2. Postgreql Database addon

3. AWS webserver hosting uploaded static files

4. <<device>> IOT device (smartphones, laptops, desktops):
    - Web Browser
