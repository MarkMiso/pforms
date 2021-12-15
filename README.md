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

In the main folder create a .env file and define the `SQLALCHEMY_DATABASE_URI` (database uri), `SECRET_KEY` (server secret key) and `CSV_FOLDER_PATH` (path to store exported csv files) variables
```shell
$ touch .env
$ cat >> .env
  SQLALCHEMY_DATABASE_URI=postgresql://youruser:userpassword@localhost/yourdatabase
  SECRET_KEY=YourServerSecretkey
  CSV_FOLDER_PATH=/YourAbsolutePathToStoreCSVFiles
```

Install the dependencies
```shell
$ pip install -r requirements.txt
```

Now launch the setup scritp that will initalize the database.
```shell
$ python setup.py
```

> NOTE: The scipt initializes the database creating all tables and adding 2 form categories (sport and food) and a user called deleted
> 
> The user deleted is necessary for the correct functioning of the database, you should not modify it.
> You are free to add and remove any category from the setup script.

## Troubleshooting postgres

Postgres requires the `/var/run/postgresql` folder to exist in order to startup the database, if said folder dosn't exist create it and assign it to postgres
```shell
$ sudo mkdir /var/run/postgresql
$ sudo chown -P postgres:postgres /var/run/postgresql
```

# Run

Use the flask run command to start the flask server
```
$ flask run
```