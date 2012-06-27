from sasi.conf import conf
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData

engine = create_engine(conf['DB_URI'])
session = scoped_session(sessionmaker(bind=engine))
metadata = MetaData()


