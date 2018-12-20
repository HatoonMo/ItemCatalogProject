# Item Catalog




## Project Description 
this application provides a list of items within a variety of categories,and ( add, edit, delete ) item functionality, as well as provide a user registration and authentication system.
A user does not need to be logged in in order to view categories or items. However, owners of items meaning who created the item can edit and delete it.

This program uses OAuth 2 with Google.
 Flask, Jinja2, and SQLalchemy. are some of the technologies used to create this project.

 
## set up
* install Vagrant and  virtual machine VirtualBox 
* Download a FSND virtual machine: https://github.com/udacity/fullstack-nanodegree-vm
* clone this repository into catalog dirctory
* cd into /vagrant folder 
* run vagrant up then vagrant ssh 
* run the project from python3 application.py
* access application from http://localhost:5000/catalog
## CRUD Functionalities 
### Main page (view Catalog)
/catalog --- Returns catalog page with all categories and Latest Added Items.
![main page](https://user-images.githubusercontent.com/19895545/50293813-7e70e480-0485-11e9-97d3-dfb6be7aa52c.PNG)
### Main Page (Logged in)
if logged in allows the user to add item 
![main page logged in](https://user-images.githubusercontent.com/19895545/50293956-d6a7e680-0485-11e9-9332-bdcd2134bd69.PNG)

### Browse Category 
/catalog/category name/items -- Returns all items of this category
![brows category](https://user-images.githubusercontent.com/19895545/50294219-75344780-0486-11e9-8a1c-9c6b2dc19d46.PNG)

### Browse Item 
/catalog/category name/item name -- Returns name and description of item

![brows item](https://user-images.githubusercontent.com/19895545/50294218-749bb100-0486-11e9-979d-7bc39a1de038.PNG)
### Edit Item

/catalog/item name/edit -- Returns edit page for item if the user is owner of item otherwise prompt a message "You are not authorized to edit items you have not added."
![edit item](https://user-images.githubusercontent.com/19895545/50294220-75344780-0486-11e9-9401-46fb3b95e800.PNG)
### Delete Item

/catalog/item name/delete -- Returns delete page for item if the user is owner of item otherwise prompt a message "You are not authorized to delete items you have not added."

![delete item](https://user-images.githubusercontent.com/19895545/50294937-0952de80-0488-11e9-8017-f07bda9336d6.PNG)

## API Endpoint 

/catalog/catalog.json -- Returns list of all categories with their items 
![catalog](https://user-images.githubusercontent.com/19895545/50295017-33a49c00-0488-11e9-973f-7b28e3984024.png)

/catalog/category name/item/item_id/JSON -- Returns specific item information

![item json](https://user-images.githubusercontent.com/19895545/50295015-33a49c00-0488-11e9-89c6-814237bbd217.PNG)
