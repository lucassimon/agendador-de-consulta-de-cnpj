import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()



# create command function
@click.command(name='createdb')
@with_appcontext
def createdb():
    db.create_all()
