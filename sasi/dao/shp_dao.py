"""
This class provides an interface to data stored in a shp file.
"""

import re
from memory_dao import Memory_DAO
#@TODO: make this platform agnostic later.
# E.g. use JTS if using jython.
import fiona
import shapely.geometry

class SHP_DAO(Memory_DAO):

    def __init__(self, shp_file, model=None):
        items = []
        with fiona.collection(shp_file, "r") as source:
            for record in source:
                obj = model()
                if hasattr(model, 'id'): 
                    obj.id = record['id']
                if hasattr(model, 'geom'): 
                    obj.geom = shapely.geometry.shape(record['geometry'])
                for prop in source.schema['properties'].keys():
                    if hasattr(model, prop): 
                        value = record['properties'][prop]
                        setattr(obj, prop, value)
                items.append(obj)

        Memory_DAO.__init__(self, items=items)

