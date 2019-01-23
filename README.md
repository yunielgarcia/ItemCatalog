# Items Catalog

Items Catalog is a web application that connects to a Postresql database and lets you browse a catalog
of items. Sort them by Category. It also features a third party authentication system (Google +).
Once authenticated users can manage their own Items (Create, Read, Update, Delete (CRUD)).

## Project Details
  - ip address: 52.206.14.6
  - ssh port: 2200
  - Hosted url: http://52.206.14.6.xip.io/

## Software Summary
Ubuntu packages:
-   apache2 [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=apache2&searchon=names)
-   libapache2-mod-wsgi [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=libapache2-mod-wsgi&searchon=names)
-   python-flask [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=python-flask&searchon=names)
-   postgresql [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=postgresql&searchon=names)
-   python-psycopg2 [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=python-psycopg2&searchon=names)
-   libpq-dev [here](https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=libpq-dev&searchon=names)

Python packages:
bleach==3.0.2
certifi==2018.11.29
chardet==3.0.4
Click==7.0
Flask==1.0.2
Flask-HTTPAuth==3.2.4
Flask-Login==0.4.1
Flask-SQLAlchemy==2.3.2
httplib2==0.12.0
idna==2.8
itsdangerous==1.1.0
Jinja2==2.10
MarkupSafe==1.1.0
oauth2client==4.1.3
packaging==18.0
passlib==1.7.1
psycopg2==2.6.1
psycopg2-binary==2.7.6.1
pyasn1==0.4.4
pyasn1-modules==0.2.2
pyparsing==2.3.0
redis==3.0.1
requests==2.21.0
rsa==4.0
six==1.12.0
SQLAlchemy==1.2.15
urllib3==1.24.1
webencodings==0.5.1
Werkzeug==0.14.1

```
{
    "web": {
        "client_id": "YOUR_CLIENT_ID",
        "project_id": "PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://www.googleapis.com/oauth2/v3/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uris": [
            "http://localhost:5000/gconnect",
            "http://localhost:5000/login"
        ],
        "javascript_origins": [
            "http://localhost:5000"
        ]
    }
}
```
-   note from above you should include in the project at the developer console for that project the correct **javascript_origins** and **redirect_uris**
-   Now you can run the project by executing in the console `python app.py`. This will serve the app at http://localhost:5000

License
----

MIT


**Free Software, Hell Yeah!**