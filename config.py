import os

basedir = os.path.abspath((os.path.dirname(__file__)))

SQLALCHEMY_ECHO = False

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/ticket_sell?unix_socket=/srv/run/mysqld/mysqld.sock"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/ticket_sell"

