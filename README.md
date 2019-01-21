# Items Catalog

Items Catalog is a web application that connects to a SQlite3 database and lets you browse a catalog
of items. Sort them by Category. It also features a third party authentication system (Google +).
Once authenticated users can manage their own Items (Create, Read, Update, Delete (CRUD)).

## Requirements to run it

  - You may be in a linux environment/image. Like [Here](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/bc938915-0f7e-4550-a48f-82241ab649e3/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91)
  - Or any other python environment (Mac/Windows)

## Instructions to run it
-   Install all the packages with their specified version in requirements.txt. You can do.
`sudo pip install -r requirements.txt`
-   You must initialized the database by running `python populate_items.py`. This will create the Categories and a few items examples. You will be able to add your afterwords.
-   The project uses third party authentication system. In order to use it you must create a project at
    [https://console.developers.google.com/](https://console.developers.google.com/).
    Enables the Google + API for web apps. Generate the credentials to use. Download them to a file named `client_secrets.json` and place it in the root directory, at the same level of your `app.py`. The file should look like this:
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