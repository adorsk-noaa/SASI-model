"""
This class provides an interface to data stored in a CSV file.
"""

import csv
import re
from memory_dao import Memory_DAO
#@TODO: make this platform agnostic later.
# E.g. use JTS if using jython.
import shapely.wkt, shapely.wkb

class CSV_DAO(Memory_DAO):

    def __init__(self, csv_file, model=None):
        self.model = model
        if isinstance(csv_file, str):
            csv_file = open(csv_file, 'rb')
        reader = csv.reader(csv_file)
        self.columns = []
        headers = reader.next()
        for i in range(len(headers)):
            header = headers[i]
            m = re.match('(.*)__(.*)', header)
            if m:
                column_name = m.group(1)
                column_type = m.group(2)
            else:
                column_name = header
                column_type = 'str'

            self.columns.append({
                'name': column_name,
                'index': i,
                'type': column_type
            })

        items = []
        for row in reader:
            obj = self.model()
            try:
                for c in self.columns:
                    if c['type'] == 'geom_wkt':
                        value = shapely.wkt.loads(row[c['index']])
                    elif c['type'] == 'geom_wkb':
                        value = shapely.wkb.loads(row[c['index']])
                    else:
                        value = eval("%s('%s')" % (c['type'], row[c['index']]))
                    setattr(obj, c['name'], value)
                items.append(obj)
            except: continue

        Memory_DAO.__init__(self, items=items)

