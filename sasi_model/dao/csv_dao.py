"""
This class provides an interface to data stored in a CSV file.
"""

import csv
import re

class CSV_DAO(object):

	def __init__(self, csv_file, model=None):
		self.rows = []
		self.model = model
		if isinstance(csv_file, str):
			csv_file = open(csv_file, 'rb')
		reader = csv.reader(csv_file)
		self.columns = []
		headers = reader.next()
		for i in range(len(headers)):
			header = headers[i]
			m = re.match('(.*)__(int|str|float)', header)
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

		for row in reader:
			obj = self.model()
			for c in self.columns:
				value = eval("%s('%s')" % (c['type'], row[c['index']]))
				setattr(obj, c['name'], value)
			self.rows.append(obj)

	def all(self):
		return self.rows





