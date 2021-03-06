
# Item Management

An application provides RESTful APIs to manage records of categories and their corresponding items.

## Getting Started

### Prerequisites
- Database: [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- Programming Language: [ Python 2.7 ](https://www.python.org/download/releases/2.7/) 
- Connector: [ MySQL Connector/Python ](https://dev.mysql.com/downloads/connector/python/) 
- Virtual environment: [ Virtualenv ](https://virtualenv.pypa.io/en/latest/) 
- Package installer: [ Pip ](https://pip.pypa.io/en/urdy/installing/) 
- Version control: [ Git ](https://git-scm.com/downloads)





### Installing

Clone the project from [github](https://github.com):

```sh
git clone https://github.com/JustNam/ItemManagement
```


Create Virtualenv folder:

```sh
cd ItemManagement
python2.7 -m virtualenv venv 
```

Install necessary packages:
```sh
pip install -r requirements.txt
```
 
Create new database in MySQL:
```sh
mysql> CREATE DATABASE {database_name};
```

Rename following configuration files in `configs` directory: 
- File contains common configurations: `config.example.py` -> `config.py`
- File contains configurations of `development` environment: `development.example.py` -> `development.py`
- File contains configurations of `production` environment: `production.example.py` -> `production.py`

Edit database information in `production.py` and `development.py`:
```sh
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE','mysql://{username}:{password}@localhost/{database_name}') 
```

Edit secret key of the application in `config.py`: 
```sh
SECRET_KEY = {your secret key}
```

Some optional parameters can be changed in configuration files:
```
SQLALCHEMY_TRACK_MODIFICATIONS= {True/False}
JWT_ACCESS_TOKEN_EXPIRES= {The number of seconds from when the token is created until the token expired}
ITEMS_PER_PAGE= {The number of records in one page}
```
 
Start the server with the environment you want to run the application on:
```sh
ENV={'production'/'development'} python run.py
```



## Running the tests
Import test database:
```sh
mysql -u {username} -p {database_name} < item_management_test.sql
```
Execute all the tests:
```sh
pytest tests
```

Execute all the tests of "user" endpoints:
```sh
cd tests
python user.py
```
Add `-v` option to show the detail of testing process:
```sh
python user.py -v
```

Execute all the tests of "item" endpoints from `tests` folder:
```sh
python item.py
```

Execute all the tests of "category" endpoints from `tests` folder:
```sh
python category.py
```
