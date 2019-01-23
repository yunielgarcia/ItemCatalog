import random
import string
import requests
import json
import httplib2
import os

from flask import (Flask, g, render_template,
                   redirect, make_response, request,
                   flash, url_for, jsonify)
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask_login import (LoginManager, login_user,
                         logout_user, login_required,
                         current_user)

from models import Base, Category, Item, User

app = Flask(__name__)
APPLICATION_NAME = "Items Catalog"

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(PROJECT_ROOT, 'client_secrets.json')
CLIENT_ID = json.load(open(json_url))['web']['client_id']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'showLogin'


@login_manager.user_loader
def load_user(userid):
    """
    This callback is used to reload the user object from the user ID
     stored in the session.
    """
    return session.query(User).filter_by(id=userid).one()


@app.teardown_request
def remove_session(ex=None):
    session.remove()


@app.route('/')
@app.route('/items_all/')
def show_items():
    """Show all items and all categories"""
    items = session.query(Item).order_by(asc(Item.name))
    categories = session.query(Category).all()
    return render_template('items.html', items=items, categories=categories)


@app.route('/categories/<int:category_id>/items')
def show_items_for_category(category_id):
    """
    Show items filtered by the category selected.
    :param category_id: id of the category selected
    :return: Template with its context
    """
    category_id_selected = category_id
    items = session.query(Item).filter_by(
        category_id=category_id_selected).all()
    categories = session.query(Category).all()
    return render_template('items.html',
                           items=items,
                           category_id_selected=category_id_selected,
                           categories=categories)


@app.route('/items/<int:item_id>')
def show_single_item(item_id):
    """
    Show detail page for the selected item.
    :param item_id: selected item id
    :return: template with its context
    """
    item = session.query(Item).filter_by(id=item_id).one()
    is_owner = False
    if current_user and ownership(item_id):
        is_owner = True
    return render_template('single_item.html', item=item, is_owner=is_owner)


@app.route('/items/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    """
    Creates a new Item and saves it to db.
    """

    categories = session.query(Category).all()
    if request.method == 'POST':
        if (not request.form['name'] or not request.form['description'] or not
                request.form['category']):
            flash('all field are required')
            return render_template('new_item.html', categories=categories)
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=int(request.form['category']),
            user_id=int(current_user.id))
        session.add(new_item)
        session.commit()
        flash('New %s Item Successfully Created' % new_item.name)
        return redirect(url_for('show_items'))
    else:
        return render_template('new_item.html', categories=categories)


@app.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_catalog_item(item_id):
    """
    Edits a single Item and saves it to db.
    :param item_id: selected item id
    """

    editedItem = session.query(Item).filter_by(id=item_id).one()
    categories = session.query(Category).all()
    if not ownership(item_id):
        flash('You are not the owner')
        return redirect(url_for('show_items'))
    elif request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        if current_user:
            editedItem.user_id = current_user.id
        session.add(editedItem)
        session.commit()
        flash('Catalog Item Successfully Edited')
        return redirect(url_for('show_single_item', item_id=item_id))
    else:
        return render_template('edit_catalog_item.html',
                               item=editedItem,
                               categories=categories)


@app.route('/items/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_catalog_item(item_id):
    """
    Removes a selected Item from db.
    :param item_id: selected item id
    """
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if not ownership(item_id):
        flash('You are not the owner')
    elif request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('show_items'))
    else:
        return render_template('delete_catalog_item.html', item=itemToDelete)


#  *********** AUTHENTICATION / AUTHORIZATION ***********

@app.route('/login')
def showLogin():
    """
    Create anti-forgery state token to validate requests.
    :return: Template with the STATE value
    """

    state = ''.join(generate_random_letter() for _ in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Extracts and exchanges the code present in the request by access_token
    which will then be used to retrieve user's information.
    """

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(json_url, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        login_session['credentials'] = credentials.to_json()
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        # print('error FlowExchangeError')
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    credentials.authorize(h)
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data.get('name', '')
    login_session['picture'] = data.get('picture', '')
    login_session['email'] = data.get('email', '')

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    # flask-login
    user = get_user_info(user_id)
    login_user(user)
    g.user = current_user

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style = "width: 300px;'
               ' height: 300px;'
               'border-radius: 150px;'
               '-webkit-border-radius: 150px;'
               '-moz-border-radius: 150px;"> ')
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
@login_required
def gdisconnect():
    """
    Revokes the access_token used and delete the session data.
    Logout the user.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None. Current user not connected.')
        logout_user()
        flash('Current user not connected.')
        return redirect(url_for('show_items'))
    print('In gdisconnect access token is %s' % access_token)
    print('User name is: ')
    print(login_session['username'])

    result = requests.post(url='https://accounts.google.com/o/oauth2/revoke',
                           params={
                               'token': access_token,
                               'client_id': CLIENT_ID,
                               'client_secret': 'FT0V4pxDd0DYpJO7ZVEEKho_'
                           },
                           headers={
                               'content-type':
                                   'application/x-www-form-urlencoded;'
                                   ' charset=utf-8'
                           })

    print('result is ')
    print(result)
    if result.status_code == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        logout_user()
        flash("You've been logged out!")
        return redirect(url_for('show_items'))
    else:
        flash('Failed to revoke token for given user.')
        return redirect(url_for('show_items'))


# ****************** User Helper Functions **************
def create_user(login_session):
    """
    Creates a User and saves it to db
    :param login_session: stored user info
    :return: user id created
    """
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """
    Retrieve User from db based on his email.
    :param email: user's email
    :return: user's id
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def ownership(item_id):
    """Evaluates whether the current user is owner of the item or not."""
    if current_user.is_authenticated:
        owned_items = (session.query(Item)
                       .filter(Item.user_id == current_user.id).all())
        return item_id in [item.id for item in owned_items]
    else:
        return False


def generate_random_letter():
    """
    Generates a random letter.
    """
    return random.choice(string.ascii_uppercase + string.digits)


# JSON ENDPOINTS
@app.route('/items/<int:item_id>/JSON')
def catalog_item_json(item_id):
    """Returns item detail data for selected item"""
    i = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=i.serialize)


if __name__ == '__main__':
    app.secret_key = 'adjsfkls$%@#$REWGDFgfdg@$45432%@$%35asdfdsafas'
    # app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=5000)
