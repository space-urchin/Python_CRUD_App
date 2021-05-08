import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    contact = db.Column(db.String(100))

    def __init__(self,firstname,lastname,email,contact):
      self.firstname = firstname
      self.lastname = lastname
      self.email = email
      self.contact = contact
    
@app.before_first_request
def create_tables():
  db.create_all()

@app.route('/')
def Index():
  all_data = Data.query.all()
  return render_template("index.html", users = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
  if request.method == 'POST':
    firstname = request.form['firstName']
    lastname = request.form['lastName']
    email = request.form['email']
    contact = request.form['contact']

    my_data = Data(firstname, lastname, email, contact)
    db.session.add(my_data)
    db.session.commit()

    flash("New user created successfully")

    return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
  if request.method  == 'POST':
    my_data = Data.query.get(request.form.get('id'))

    print(my_data)

    my_data.firstname = request.form['firstName']
    my_data.lastname = request.form['lastName']
    my_data.email = request.form['email']
    my_data.contact = request.form['contact']

    db.session.commit()
    flash("User information has been updated successfully")

    return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
  my_data = Data.query.get(id)
  db.session.delete(my_data)
  db.session.commit()
  flash("User has been deleted successfully")

  return redirect(url_for('Index'))

if __name__ == "__main__":
  app.run(port = 2233, host = "0.0.0.0",debug=True)