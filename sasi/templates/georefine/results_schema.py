from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.postgis import PGComparator

classes = {}
tables = []
metadata = MetaData()
primary_class = None

# Define classes.

# Cell
class Cell(object):
    id = None		
    z = None
    area = None
    geom = None
classes['Cell'] = Cell

# Substrate
class Substrate(object):
    id = None
    name = None
classes['Substrate'] = Substrate

# Feature
class Feature(object):
    id = None
    name = None
    category = None
classes['Feature'] = Feature

# Gear
class Gear(object):
    id = None
    name = None
    category = None
classes['Gear'] = Gear

# Result
class Result(object):
    id = None
    t = None
    cell = None
    gear = None
    substrate = None
    energy = None
    feature = None
    a = None
    x = None
    y = None
    z = None
    znet = None
classes['Result'] = Result

# Set primary class.
primary_class = Result

#
## Define tables and mappings (in dependency order). ##
#

# Cell
cell_table = Table('cell', metadata,
        Column('id', Integer, primary_key=True),
        Column('z', Float),
        Column('area', Float),
        GeometryExtensionColumn('geom', Polygon(2)),
        )
GeometryDDL(cell_table)
tables.append({'id': 'cell', 'table': cell_table})
mapper(Cell, cell_table, properties = {
    'geom': GeometryColumn(test1_table.c.geom, comparator=PGComparator),
    })

# Substrate
substrate_table = Table('substrate', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        )
tables.append({'id': 'substrate', 'table': substrate_table})
mapper(Substrate, substrate_table)

# Feature
feature_table = Table('feature', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('category', String),
        )
tables.append({'id': 'feature', 'table': feature_table})
mapper(Feature, feature_table)

# Gear
gear_table = Table('gear', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('category', String),
        )
tables.append({'id': 'gear', 'table': gear_table})
mapper(Gear, gear_table)

# Result 
result_table = Table('result', metadata,
        Column('id', Integer, primary_key=True),
        Column('t', Integer),
        Column('cell_id', Integer, ForeignKey('cell.id')),
        Column('gear_id', Integer, ForeignKey('gear.id')),
        Column('substrate_id', Integer, ForeignKey('substrate.id')),
        Column('feature_id', Integer, ForeignKey('feature.id')),
        Column('a', Float),
        Column('x', Float),
        Column('y', Float),
        Column('z', Float),
        Column('znet', Float),
        )
tables.append({'id': 'result', 'table': result_table})
mapper(Result, result_table, properties={
    'cell': relationship(Cell),
    'gear': relationship(Gear),
    'substrate': relationship(Substrate),
    'feature': relationship(Feature),
    })

