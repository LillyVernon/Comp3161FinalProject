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
        
        return redirect(url_for('home'),user['FirstName'])
    else:
        msg = 'Incorrect email/password!'
   
    return render_template('login.html', msg='')


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
   session.pop('id', None)
   session.pop('email', None)
   return redirect(url_for('loginacc'))

@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        #account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


''' @app.route('/property', methods=['POST', 'GET'])
def property():
    form=MyForm()
    if request.method == 'POST' and form.validate_on_submit():
        photo=request.files['photo']
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File Saved', 'success')
        return redirect(url_for('home'))
    return render_template('property.html',form=form) '''


""" @app.route('/property', methods=['POST', 'GET'])
def property():
    form=MyForm()
    if request.method == 'POST' and form.validate_on_submit():
        #photo=request.files['photo']
        photo=form.photo.data
        filename=secure_filename(photo.filename)
        typevalue=dict(form.propertyType.choices).get(form.propertyType.data)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        property=Property(request.form['title'],request.form['description'], request.form['rooms'],
        request.form['bathroom'],request.form['price'],
        request.form['propertyType'], request.form['location'], filename)
        #photo1=request.file['photo'].read()
        db.session.add(property)
        db.session.commit()
        flash('Propery was sucessfully added', 'success')
        return redirect(url_for('properties'))
    flash_errors(form)
    return render_template('property.html',form=form) """


""" @app.route('/property/<propertyid>', methods=['get'])
def individualproperty(propertyid):
    query=db.session.query(Property).filter_by(id=propertyid)
    if request.method=='get':
        print(request.form['button'])
    return render_template('individualproperty.html',query=query) """

''' @app.route('/properties')
def property():
 property = db.session.query(Property).all()
 return render_template('show_users.html',property=property) '''



""" def get_uploaded_images():
    lst=[]
    rootdir=os.getcwd()
    for subdir, dirs, files in os.walk(rootdir + '/uploads/'):
        for file in files:
            lst.append(file)
    return lst

@app.route("/uploads/<filename>")
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

@app.route('/properties')
def properties():
    #items=get_uploaded_images()
    items=db.session.query(Property).all()
    return render_template("properties.html", items=items) """



""" 
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['ADMIN_USERNAME'] or request.form['password'] != app.config['ADMIN_PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('property'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home')) """


###
# The functions below should be applicable to all Flask apps.
###

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
