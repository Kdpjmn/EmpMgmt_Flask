from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# employee Class/Model
class Employee(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  email = db.Column(db.String(200))
  department = db.Column(db.String(100))

  def __init__(self, name, email, department):
    self.name = name
    self.email = email
    self.department = department


# employee Schema
class EmployeeSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'email', 'department')

# Init schema
employee_schema = EmployeeSchema(strict=True)
employees_schema = EmployeeSchema(many=True, strict=True)

# Create a employee
@app.route('/employee', methods=['POST'])
def add_employee():
  name = request.json['name']
  email = request.json['email']
  department = request.json['department']
  

  new_employee = Employee(name, email, department)

  db.session.add(new_employee)
  db.session.commit()

  return employee_schema.jsonify(new_employee)

# Get All employees
@app.route('/employee', methods=['GET'])
def get_employees():
  all_employees = Employee.query.all()
  result = employees_schema.dump(all_employees)
  return jsonify(result.data)

# Get Single employees
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
  employee = Employee.query.get(id)
  return employee_schema.jsonify(employee)

# Update a employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
  employee = Employee.query.get(id)

  name = request.json['name']
  email = request.json['email']
  department = request.json['department']

  employee.name = name
  employee.email = email
  employee.department = department
  
  db.session.commit()

  return employee_schema.jsonify(employee)

# Delete employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
  employee = Employee.query.get(id)
  db.session.delete(employee)
  db.session.commit()

  return employee_schema.jsonify(employee)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
