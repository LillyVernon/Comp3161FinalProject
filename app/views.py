"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os 
from app import app
from flask import render_template, request, redirect, url_for, session, abort, send_from_directory
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import mysql
from app import database
import base64
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random

#.\venv\Scripts\activate

###
# Routing for your application.
###
@app.route('/login', methods=['GET', 'POST'])
def loginacc():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    
        email= request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email= %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        print (user)
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['uid'] = user['UID']
            session['email'] = user['email']
        
        return redirect(url_for('home'))
    else:
        msg = 'Incorrect email/password!'
   
    return render_template('login.html', msg='')

@app.route('/login/recipe', methods=['GET', 'POST'])
def recipe():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT IName FROM ingredient')
        ingredients = cursor.fetchall()
        cursor.execute('SELECT Quantity,measurements from measurement')
        measurements=cursor.fetchall()

        return render_template('recipe.html', email=session['email'], ingredients=ingredients, measurements=measurements)
    return redirect(url_for('loginacc'))

@app.route('/login/home/breakfast', methods=['GET', 'POST'])
def breakfast():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT RecipeID from recipe')
        recipeid=cursor.fetchall()
        print(recipeid)
        ran=random.choice(recipeid)
        cursor.execute('SELECT Manual.steps, Manual.instructions from manual where recipeID =%s', str(ran['RecipeID']),)
        instruction=cursor.fetchall()
        #print(instruction)
        #create['recipeIngredients']="CREATE TABLE RecipeIngredient (RecipeID int not null, IngredientID int not null, MID int not null, amount float, 
        # foreign key(RecipeID) references Recipe(RecipeID), foreign key(IngredientID) references ingredient(IngredientID), foreign key(MID) references Measurement(MID))"
        cursor.execute('select * from recipeingredient where recipeID=%s', str(ran['RecipeID']),)
        recipeingredients=cursor.fetchall()
        print(recipeingredients)
        #cursor.execute('insert into meal()', str(ran['RecipeID']),)
        return render_template('breakfast.html', email=session['email'])
    return redirect(url_for('loginacc'))

@app.route('/login/home/supermarket', methods=['GET', 'POST'])
def supermarket():
    if 'loggedin' in session:
        return render_template('supermarket.html', email=session['email'])
    return redirect(url_for('loginacc'))

@app.route('/login/home/ingredients', methods=['GET', 'POST'])
def ingredients():
    if 'loggedin' in session:
        return render_template('ingredients.html', email=session['email'])
    return redirect(url_for('loginacc'))

@app.route('/login/register', methods=['GET', 'POST'])
def register():
    msg=''
    print(request.form)
    #if request.method == 'POST' and 'FirstName' in request.form and 'LastName' in request.form and 'password' in request.form and 'email' in request.form:
    if request.method == 'POST' and 'FirstName' in request.form and 'LastName' in request.form and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access 
        firstname = request.form['FirstName']
        lastname = request.form['LastName']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        users = cursor.fetchone()
        if users:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not email or not password or not email or not firstname or not lastname:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,%s, %s, %s, %s)', (firstname,lastname, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('home.html', email=session['email'])
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/login/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('loginacc'))

@app.route('/login/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('uid', None)
   session.pop('email', None)
   return redirect(url_for('loginacc'))

@app.route('/')
def base():
    return render_template('login.html')
    
@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE uid = %s', (session['uid'],))
        user = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))






# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
