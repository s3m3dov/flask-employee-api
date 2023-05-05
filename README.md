# Flask API for Employee Data
This Flask API serves data from a SQLite database containing information about employees of a fictional company. The API allows for basic CRUD (Create, Read, Update, Delete) operations on the employee data, and also provides additional endpoints for data analysis purposes.

## Endpoints
The Flask API has the following endpoints:
- `GET /employees`: Returns a list of all employees in the database.
- `GET /employees/<int:id>`: Returns the employee with the specified ID.
- `POST /employees`: Creates a new employee with the specified data (name, department, salary, hire_date). The API returns the ID of the newly created employee.
- `PUT /employees/<int:id>`: Updates the employee with the specified ID with the specified data (name, department, salary, hire_date).
- `DELETE /employees/<int:id>`: Deletes the employee with the specified ID.
- `GET /departments`: Returns a list of all unique departments in the database.
- `GET /departments/<string:name>`: Returns a list of all employees in the specified department.
- `GET /average_salary/<string:department>`: Returns the average salary of employees in the specified department.
- `GET /top_earners`: Returns a list of the top 10 earners in the company based on their salary.
- `GET /most_recent_hires`: Returns a list of the 10 most recently hired employees.
- `POST /predict_salary`: Takes in data for a new employee (department, hire date, and job title) and returns the predicted salary.

## Commands
- `flask generate-employees`: run this command to generate employees using `faker`
- `flask train-salary-model --count 1000`: run this command to train salary prediction model

## Models
The database is generated using the SQLAlchemy library and contains a table called "employees" with the following columns:
- `id`: an auto-incrementing integer and primary key
- `name`: a string with a maximum length of 50 characters
- `department`: a string with a maximum length of 50 characters
- `salary`: a float with a minimum value of 0 and maximum value of 1000000
- `hire_date`: a datetime object in the format of 'YYYY-MM-DD HH:MM:SS', with a range from 01-01-2020 00:00:00 to today. 

## Set-Up
1. Clone the repository:
```
git clone https://github.com/s3m3dov/flask-employee-api.git
```

2. Set-up poetry
```
poetry env use python3.10
```
```
poetry install
```

3. Run the development server
```
poetry run flask run
```

4. Generate fake data for employees
```
flask train-salary-model --count 1000
```

## Documentation
The API documentation is available at:
- Swagger UI: `http://localhost:5000/api/swagger`
- Redoc UI: `http://localhost:5000/api/redoc`
- Rapidoc UI: `http://localhost:5000/api/rapidoc`

## Dependencies
- Python 3.10
- `Flask`: a micro web framework for Python used to build the API endpoints
- `Flask-Smorest`: an extension for Flask that simplifies the creation of RESTful APIs
- `Marshmallow`: a Python library for serializing and deserializing data, which is used for validating input and output data in the API
- `Flask-SQLAlchemy`: an extension for Flask that adds support for SQLAlchemy, a SQL toolkit and ORM, which is used for communicating with the SQLite database
- `SQLAlchemy-Utils`: a library that provides various utility functions for working with SQLAlchemy
- `pandas`: a library for data manipulation and analysis, used for loading and preprocessing data for the salary prediction model.
- `scikit-learn`: a popular machine learning library for Python, used for building and training the salary prediction model
- `colorlog`: a library that provides colored logs
- `Faker`: a library for generating fake data, used for populating the SQLite database with random employee data
- `Flask-Migrate`: an extension for Flask that handles SQLAlchemy database migrations
- `Flask-Testing`: an extension for Flask that provides utilities for testing the API
