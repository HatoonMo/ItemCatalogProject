from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatItem, User
import random
import string
import httplib2
import json
import requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('c.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "item Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogDB.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def browseCatalog():
    catalog = session.query(Category).order_by(asc(Category.name))
    latestitems = session.query(CatItem).order_by(CatItem.id.desc()).limit(7)
    if 'username' not in login_session:
        return render_template('publiccatalog.html', catalog=catalog,
                               latestitems=latestitems)
    else:
        return render_template('catalog.html', catalog=catalog,
                               latestitems=latestitems)


# OAuth functionalty
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    print("Obtain authorization code")
    try:
        print("after try")
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('c.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        login_session['credentials'] = credentials.to_json()
        print("59")
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print(response)
        return response
    print("Upgrade the authorization code into a credentials object")
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # Added decode to fix an error
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
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
        response = make_response(json.dumps('Current user is already'
                                            ' connected.'), 200)
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

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    gdisconnect()
    # del login_session['gplus_id']
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    flash("You have successfully been logged out.")
    return redirect(url_for('browseCatalog'))


@app.route('/catalog/<category_name>/items')
def browseCategory(category_name):
    catalog = session.query(Category).order_by(asc(Category.name))
    items = session.query(CatItem).filter_by(category_name=category_name)
    return render_template('category.html', catalog=catalog, items=items,
                           category_name=category_name)


@app.route('/catalog/<category_name>/<item_name>')
def browseItem(category_name, item_name):
    item = session.query(CatItem).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return render_template('publicitem.html', item=item)
    else:
        return render_template('item.html', item=item)


@app.route('/catalog/additem', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CatItem(
            name=request.form['title'], user_id=login_session['user_id'],
            description=request.form['description'],
            category_name=request.form['catname'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('browseCatalog'))
    else:
        catalog = session.query(Category).order_by(asc(Category.name))
        return render_template('addItem.html', catalog=catalog)


@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CatItem).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(
        name=editedItem.category_name).one()
    if login_session['user_id'] != editedItem.user_id:
        script = "<script>function myFunction() {alert('You are not "
        script += "authorized to edit items you have not added.');}"
        script += "</script><body onload='myFunction()'>"
        return script
    if request.method == 'POST':
        if request.form['title']:
            editedItem.name = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['catname']:
            editedItem.category_name = request.form['catname']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('browseCategory', category_name=category.name))
    else:
        catalog = session.query(Category).order_by(asc(Category.name))
        return render_template('editItem.html',
                               item=editedItem, catalog=catalog)


@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(CatItem).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(
        name=deletedItem.category_name).one()
    if login_session['user_id'] != deletedItem.user_id:
        script = "<script>function myFunction() {alert('You are not "
        script += "authorized to delete items you have not added.');}"
        script += "</script><body onload='myFunction()'>"
        return script
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('browseCategory', category_name=category.name))
    else:
        catalog = session.query(Category).order_by(asc(Category.name))
        return render_template('deleteitem.html',
                               item=item_name, catalog=catalog)


# JSON APIs to view Catalog Information
@app.route('/catalog/catalog.json')
def catalogJSON():
    # returns all categories with their items
    items = session.query(CatItem).order_by(CatItem.id.desc())
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/catalog/<category_name>/item/<int:item_id>/JSON')
def itemJSON(category_name, item_id):
    # returns specific item
    item = session.query(CatItem).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
