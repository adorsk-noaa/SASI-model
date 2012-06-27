from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sasi.habitat.substrate import Substrate

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('substrate', metadata,
		Column('id', String, primary_key=True),
		Column('name', String)
		)
		
mapper(Substrate, table)
