
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
virtualenv venv
```

Install necessary packages:
```sh
pip install -r requirements.txt
```
 
Create new database in MySQL:
```sh
mysql> CREATE DATABASE {database name};
```


Edit database information in `config.py`:
 ```sh
...
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE','mysql://{username}:{password}@localhost/{database name}') 
...
```
 

Start the server: 
```sh
 python run.py
 ```
 



## Running the tests

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
