from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatItem, User
import random, string, httplib2, json,requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('c.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "item Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
@app.route('/')
@app.route('/catalog')
def browseCatalog():
    pass
# OAuth functionalty 
@app.route('/gconnect', methods=['POST'])
def gconnect():
    pass 

@app.route('/gdisconnect')
def gdisconnect():
    pass

@app.route('/catalog/<category_name>/items')
def browseCategory(category_name):
    pass

@app.route('/catalog/<category_name>/<item_name>')
def browseItem(category_name,item_name):
    pass

@app.route('/catalog/additem')
def addItem():
    pass

@app.route('/catalog/<item_name>/edit')
def editItem(item_name):
    pass

@app.route('/catalog/<item_name>/delete')
def deleteItem(item_name):
    pass

# JSON APIs to view Catalog Information
