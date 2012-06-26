"""
This class provides an interface to data stored in a CSV file.
"""

import csv
import re

class CSV_DAO(object):

	def __init__(self, csv_file, model=None):
		self.items = []
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
			self.items.append(obj)


	def all(self):
		return self.items

	def query(self, filters=[]):
		results = []

		for item in self.items:
			passes = True

			# Assumes filters are like: {'entity': {'expression': '{prop}'}, 'op': '==', 'value': 'foo'}.
			for f in filters:
				entity = f['entity']
				expression = entity['expression']
				entity_code = re.sub('{(.*?)}', r'getattr(item, "\1")', entity['expression'])
				filter_code = "%s %s %s" % (entity_code, f['op'], f['value'])
				if not eval(filter_code):
					passes = False
					break
					
			if passes:
				results.append(item)

		return results

