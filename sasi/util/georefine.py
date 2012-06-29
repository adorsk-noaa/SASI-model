"""
Utility functions for packaging data for georefine.
"""

import tempfile
import csv
import tarfile
import os

def objects_to_csv_file(objects=[], fields=[], prefix=''):
    csv_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".csv", delete=False)
    writer = csv.writer(csv_file)
    for i in range(len(fields)):
        if type(fields[i]) == str:
            fields[i] = {'name': fields[i]}
    writer.writerow([f['name'] for f in fields])
    for obj in objects:
        row = []
        for f in fields:
            if not f.has_key('formatter'):
                f['formatter'] = lambda o: getattr(o, f['name'])
            row.append(f['formatter'](obj))
        writer.writerow(row)
    csv_file.close()
    return csv_file.name

def create_gr_project_file(filename=None, schema_file=None, app_config_file=None, data_files=[]):
    if filename == None:
        filename = os.path.join(tempfile.gettempdir(), "sasi_georefine.%s.tar.gz" % (os.getpid()))
    topdir = "georefine"
    tar = tarfile.open(filename, "w:gz")
    tar.add(schema_file, arcname=os.path.join(topdir, "schema.py"))
    tar.add(app_config_file, arcname=os.path.join(topdir, "app_config.py"))
    for data_file in data_files:
        tar.add(data_file['path'], arcname=os.path.join(topdir, "data", data_file['name']))
    tar.close
    return filename

    
