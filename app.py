import logging
import json
from uuid import uuid4

from apistar import App, Route, schema, http, environment
from apistar.backends import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.schema import Column

_log = logging.getLogger(__name__)


def welcome():
    return {'message': 'Welcome to API Star!'}


class BeerSchema(schema.Object):
    name = schema.String


Base = declarative_base()


class Beer(Base):
    __tablename__ = 'Beer'
    id = Column(UUID, primary_key=True)
    name = Column(String())


def create_beer(db: SQLAlchemy, body: http.Body):
    session = db.session_class()
    data = json.loads(body.decode('utf-8'))
    print('Got body: %s', data)

    beer = Beer(
        id=str(uuid4()),
        name=data['name'],
    )
    session.add(beer)
    session.commit()
    return {'name': data['name']}


def list_beer(db: SQLAlchemy):  # -> schema.List[BeerSchema]:
    session = db.session_class()
    beers = session.query(Beer).all()
    return {'beers': [{'name': b.name} for b in beers]}
    # return [BeerSchema(name=b.name) for b in beers]


routes = [
    Route('/', 'GET', welcome),
    Route('/beers/', 'GET', list_beer),
    Route('/beers/', 'POST', create_beer),
]


class Env(environment.Environment):
    properties = {
        'DATABASE_URL': schema.String(default='postgresql://paul:paul@localhost/apistar')
    }

env = Env()
print('Using DB URL: ', env['DATABASE_URL'])

app = App(
    routes=routes,
    settings={
        "DATABASE": {
            "URL": env['DATABASE_URL'],
            "METADATA": Base.metadata,
        }
    }
)
