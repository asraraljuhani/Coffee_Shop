import json
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(
#     os.path.join(project_dir, database_filename))
# database_name = "coffeeShop"
# database_path = "postgresql://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQL_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db_drop_and_create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
    to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    drink = Drink(
        title='water',
        created_by='Manager',
        recipe='[{"name": "water", "color": "blue", "parts": 1}]'
    )

    drink.insert()
    barista_role = Role(
        name='Barista',
        permissions_number=2
    )
    barista_role.insert()
    manager_role = Role(
        name='Manager',
        permissions_number=5
    )
    manager_role.insert()
# ROUTES


'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # String Created_by
    created_by = Column(String(80))
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is
    # [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'title': self.title
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Role(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Name
    name = Column(String(80), unique=True)
    # Integer Permissions Number
    permissions_number = Column(Integer())

    '''
    info()
        info return role name and permissions number
    '''

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'permissions_number': self.permissions_number
        }

    '''
    insert()
        inserts a new role into a database
        the role must have a unique name
        the role must have a unique id or null id
        EXAMPLE
            role = Role(name=req_name)
            role.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new role into a database
        the role must exist in the database
        EXAMPLE
            role = Role(name=req_name)
            role.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new role into a database
        the role must exist in the database
        EXAMPLE
            role = Role.query.filter(Role.id == id).one_or_none()
            role.name = 'Role 1'
            role.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.info())
