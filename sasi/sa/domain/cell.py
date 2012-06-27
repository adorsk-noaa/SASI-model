from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float, PickleType
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.domain.cell import Cell
from sasi.sa import metadata

cell_table = Table('cell', metadata,
		Column('id', Integer, primary_key=True),
		Column('type', String),
		Column('type_id', Integer),
		Column('area', Float),
		Column('habitat_composition', PickleType),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(cell_table)

mapper(
		Cell, 
		cell_table,
		properties = {
			'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator),
			}
	)



