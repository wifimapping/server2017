# Record of Work sensitive details have been abstracted, but can be viewed on [this private google doc](https://docs.google.com/a/nyu.edu/document/d/1U-lNzP9veLojQvmOC0riIdTdyrbDZKYQMqo8AeE3nqM/)

## Synopsis:

### Part 1: Setting up Directories
 - Set up Directory in capstone.cloudapp.net in /var/www/2016/
 - Cloned 'Server' Repository into this Directory

### Part 2: PostGreSQL DataBase installation on Django using [this resource](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04):
 - Installed PostGreSQL on Azure server
 - Created PostGres DataBase, User and Password
 - Stored Authentication infromation locally in password.py file in Cloned Directory

 ### Part 3: Django modifications
 - Created New Branch 'Django_PostGres'
 - Editted Code to make new Django server and new PostGres DB and point Django to it 
 
 (modified last year's code to do this)
 - Merged Branch back into original after review
 - Ran Migrate commands on Azure Server to create new Django Server which points to PostGresDB

 ### Part 4: Database Dump
 - Dumped all data from old DB into new DB

 ### Part 5: Test to see if everything fits in well
 -Still undone

 ### Part 6: Point Apache server to new Django Server
 -Still undone





 ## Documentation of Commands used and Why:

### Part 1: Setting up Directories

ssh \<username>@capstone.cloudapp.net

- *Set up Directory in capstone.cloudapp.net /var/www/2016/*

 sudo mkdir /var/www/2016

- *Clone 'Server' Repository into this Directory*

cd /var/www/2016
sudo git clone https://github.com/wifimapping/server.git






### Part 2: PostGreSQL DataBase installation on Django



#### A: Postgres installation

*Install the Components from the Ubuntu Repositories*

sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib

*PostGres was installed, during which, an operating system user named 'postgres' was created to correspond to the postgres PostgreSQL administrative user.*

*We now change to this user to perform administrative tasks:*

sudo su - postgres

*We are now in shell for user 'postgres'. Log into a Postgres session*

psql



#### B: PostGreSQL Commands:

*Create DataBase*

CREATE DATABASE \<databasename>; 

*Create Username and Password*

CREATE USER \<username> WITH PASSWORD \<password>;

*Tweak user’s properties*

ALTER ROLE \<username> SET client_encoding TO 'utf8';

ALTER ROLE \<username> SET default_transaction_isolation TO 'read committed';

ALTER ROLE \<username> SET timezone TO 'America/New_York';

*Give all privileges to user*

GRANT ALL PRIVILEGES ON DATABASE \<databasename> TO \<username>;

*Exit sql prompt*

\q



#### C: Store authentication details in password file

*Exit postgres session*

exit

*Enter server Repo and create password authentication file*

cd /var/www/2016/server/cusp_sonyc_wifi

cat "DB_NAME = '\<databasename>' ">password.py

cat "DB_USER = '\<username>' ">>password.py

cat "DB_PASS = '\<password>' ">>password.py


# From Here onwards, I'm still working on it... will update the progress on this readme as I complete work. The google doc is likely to be updated more frequently, simply because its easier to do so, (and fonts render immediately and spell checks are available)


### Part 3: Django modifications using [this resource](http://tutorial.djangogirls.org/en/django/)

 - *Created New Branch 'Django_PostGres'*

 git branch Django_PostGres
 git checkout Django_PostGres



 - *Editted Code to make new Django server and new PostGres DB and point Django to it* 

editted settings.py file and 



 - *Merged Branch back into original after review*

git 



 - *Ran Migrate commands on Azure Server to create new Django Server which points to PostGresDB*

cd 

python manage.py makemigrations 
python manage.py migrate 

### Part 4: Database Dump


 - Dumped all data from old DB into new DB
 (Still to do)