from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.domain.habitat import Habitat
from sasi.sa import metadata


table = Table('habitat', metadata,
		Column('id', Integer, primary_key=True),
		Column('substrate', String),
		Column('energy', String),
		Column('z', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(table)

mapper(
		Habitat,
		table,
		properties = {
		'geom': GeometryColumn(table.c.geom, comparator=PGComparator),
		})

