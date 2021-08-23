# Setup

Install postgress and do the initial configuration for your system.
Remember to also start the database.

Login to postgres and create a new user.
```shell
$ sudo -iu postgres
postgres$ createuser --interactive
```

Create a new database.
```shell
postgres$ createdb yourdatabase
```

In the main folder create a .env file and define the `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY` variable with the URI for your database
```shell
$ touch .env
$ cat >> .env
  SQLALCHEMY_DATABASE_URI=postgresql://youruser:userpassword@localhost/yourdatabase
  SECRET_KEY=yoursecretkey
```

Install falsk-sqlalchemy
```shell
$ pip install flask-sqlalchemy
```

Now launch the setup scritp that will initalize the database.
```shell
$ python setup.py
```

## Troubleshooting postgres

Postgres requires the `/var/run/postgresql` folder to exist in order to startup the database, if said folder dosn't exist create it and assign it to postgres
```shell
$ sudo mkdir /var/run/postgresql
$ sudo chown -P postgres:postgres /var/run/postgresql
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
- implementare meccanismo di creazione questionario
- implementare meccanismo di risposte al questionario
- implementare tool di analisi statistica