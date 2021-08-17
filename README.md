# Setup

Install postgress and do the initial configuration for your system.
Remember to also start the database.

Create a new user.
```shell
$ createuser --interactive
```

Create a new database.
```shell
$ createdb yourdatabase
```

In the main folder create a .env file and define the `SQLALCHEMY_DATABASE_URI` variable with the URI for your database
```shell
$ touch .env
$ cat >> .env
  SQLALCHEMY_DATABASE_URI=postgresql://youruser:userpassword@localhost/yourdatabase
```

Install falsk-sqlalchemy
```shell
$ pip install flask-sqlalchemy
```

Now launch the setup scritp that will initalize the database.
```shell
$ python setup.py
```

# Run

Use the flask run command
```
$ flask run
```

# TODO

- scrivere documento di progetto
- impementare i modelli ORM per il database in SQLAlchemy
  - tabella questionario
  - tabella domande
  - tabella risposte
- implementare meccanismo di login sicuro
- implementare meccanismo di creazione questionario
- implementare meccanismo di risposte al questionario
- implementare tool di analisi statistica