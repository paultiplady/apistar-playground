from apistar import App, Route
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.sql.schema import Column


def welcome():
    return {'message': 'Welcome to API Star!'}


routes = [
    Route('/', 'GET', welcome)
]

app = App(routes=routes)

Base = declarative_base()


class Beer(Base):
    __tablename__ = 'Beer'
    id = Column(UUID, primary_key=True)
    name = Column(String())


settings = {
    "DATABASE": {
        "URL": "postgresql://paul:paul@localhost/apistar",
        "METADATA": Base.metadata,
    }
}
