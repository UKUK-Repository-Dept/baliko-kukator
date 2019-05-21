from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

__all__ = ['reflect']

def reflect(engine):
    Base = declarative_base()
    metadata = MetaData(bind=engine)

    metadata.reflect(views=True)

    return metadata