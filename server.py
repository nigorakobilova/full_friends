from flask import Flask, render_template, request, session, flash, request, redirect

from mysqlconnection import MySQLConnector

app = Flask(__name__)

mysql = MySQLConnector(app, 'full_friends')



@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template("index.html", all_friends=friends)

@app.route('/friends', methods=['POST'])
def addUser():
    query = "INSERT INTO friends(first_name, last_name, email) VALUES(:first_name, :last_name, :email)"
    
    data ={
        'first_name': request.form['first'],
        'last_name':request.form['last'],
        'email':request.form['email']}
    mysql.query_db(query, data)
    return redirect("/")

@app.route('/friends/<id>/edit')
def update(id):
    query = "SELECT * from friends where id = {}".format(id)
    friends = mysql.query_db(query)
    return render_template("update.html", friend=friends[0])


@app.route('/friends/<id>', methods=['POST'])
def updateUser(id):
    
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email=:email WHERE id = :id"
    data = {
             'first_name': request.form['first'], 
             'last_name':  request.form['last'],
             'email': request.form['email'],
             'id': id
           }
    friends=mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/deletePage')
def delete(id):
    query = "SELECT * from friends where id = {}".format(id)
    
    friends=mysql.query_db(query)
    return render_template("delete.html", friend=friends[0])

@app.route('/friends/<id>/delete', methods=['POST'])
def deleteUser(id):
    query = "DELETE FROM friends where id = {}".format(id)
    
    friends=mysql.query_db(query)
    return redirect('/')
    
 
app.run(debug=True)