"""
This class provides an interface to data stored in a shp file.
"""

import re
from memory_dao import Memory_DAO
#@TODO: make this platform agnostic later.
# E.g. use JTS if using jython.
import ogr
import shapely.wkb, shapely.geometry

class SHP_DAO(Memory_DAO):

    def __init__(self, shp_file, model=None):
        items = []

        # Open shapefile and get source SRS.
        sf = ogr.Open(shp_file)
        layer = sf.GetLayer(0)
        layer_srs = layer.GetSpatialRef()

        # Set target srs to 4326 (lat/lon).
        target_srs = ogr.osr.SpatialReference()
        target_srs.ImportFromEPSG(4326)

        # Get fields.
        layer_def = layer.GetLayerDefn()
        field_count = layer_def.GetFieldCount()
        fields = [layer_def.GetFieldDefn(i).GetName() for i in range(field_count)]

        for feature in layer:
            obj = model()

            # Get fields.
            feature_fields = {}
            for i in range(field_count): 
                field = fields[i]
                value = feature.GetField(i)
                if hasattr(model, field):
                    setattr(obj, field, value)

            # Get geometry and reproject.
            if hasattr(model, 'geom'): 
                ogr_g = feature.GetGeometryRef()
                ogr_g = feature.GetGeometryRef()
                ogr_g.TransformTo(target_srs)

                # We convert each feature into a multipolygon, since
                # we may have a mix of normal polygons and multipolygons.
                geom = shapely.wkb.loads(ogr_g.ExportToWkb())
                if geom.geom_type =='Polygon':
                    geom = shapely.geometry.MultiPolygon([(geom.exterior.coords, geom.interiors )])
                model.geom = geom

        Memory_DAO.__init__(self, items=items)

