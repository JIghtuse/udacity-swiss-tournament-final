# Swiss-system tournament

This project implements [Swiss-system tournament] using PostgreSQL and Python.

# System requirements

Project was tested on a Linux machine, and this README describes usage on a
typical Linux distribution.

You will need to install `postgresql` and `python3-psycopg2` packages
to execute code.  On Fedora you can install them with following command:

        # dnf install postgresql postgresql-server python3-psycopg2

On Debian/Ubuntu you can run:

        # apt install postgresql postgresql-client postgresql-client-common python3-psycopg2 


# Installation

You will need a PostgreSQL server running and Python installed on your machine.


1. Clone this project to your machine with git:

        $ git clone https://github.com/JIghtuse/udacity-swiss-tournament-final.git tournament
        $ cd tournament

2. If you just installed PostgreSQL, you may need to initialize database
cluster, start server, and create a user with the same name as your account
name (`username` in following examples):

        # postgresql-setup --initdb
        # systemctl start postgresql
        # su postgres
        bash-4.3$ psql
        postgres=# create user username;

3. As PostgreSQL account create a database `tournament`, owned by your user
account:

        # su postgres
        $ psql
        postgres=# create database tournament owner username ;

4. As your user account connect to database and execute commands from
file "tournament.sql" to create database tables:

        $ psql tournament
        tournament=> \i tournament.sql

# Running

After finishing [Installation](#installation), you are ready ready to execute
tournament code. See `tournament.py` for list of available functions. You can
also run unit tests to check if the code executes properly:

        $ python3 tournament_test.py

[Swiss-system tournament]: https://en.wikipedia.org/wiki/Swiss-system_tournament
