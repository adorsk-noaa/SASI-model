"""
This class provides an interface to data stored in a CSV file.
"""

import csv
import re

class CSV_DAO(object):

	def __init__(self, csv_file):
		self.rows = []
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
				'index': i,
				'type': column_type
			})

		for row in reader:
			parsed_row = []
			for c in self.columns:
				value = eval("%s('%s')" % (c['type'], row[c['index']]))
				parsed_row.append(value)
			self.rows.append(parsed_row)

	def all(self):
		return self.rows





