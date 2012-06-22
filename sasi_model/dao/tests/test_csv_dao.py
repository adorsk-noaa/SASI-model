import unittest
import tempfile
import csv
import os

from sasi_model.dao.csv_dao import CSV_DAO

class Test_CSV_DAO(unittest.TestCase):

	def setUp(self):
		trash, self.csv_filename = tempfile.mkstemp()
		csv_file = open(self.csv_filename, 'wb')
		writer = csv.writer(csv_file)

		columns = [
				{'name': 'col1', 'type': 'int'},
				{'name': 'col2', 'type': 'str'},
				{'name': 'col3', 'type': 'float'},
				{'name': 'col4'},
				]
		headers = []
		for c in columns:
			header = c['name']
			if c.get('type'):
				header += "__%s" % c['type']
			headers.append(header)
		writer.writerow(headers)

		for i in range(10):
			row = []
			for c in columns:
				col_type = c.get('type', 'str')
				if col_type == 'str':
					value = "str_%s" % i
				else:
					value = i
				row.append(eval("%s('%s')" % (col_type, value)))
			writer.writerow(row)

		csv_file.close()

	def tearDown(self):
		os.unlink(self.csv_filename)

	def test_CSV_DAO(self):
		csv_dao = CSV_DAO(self.csv_filename)

		print csv_dao.all()
	

if __name__ == '__main__':
	unittest.main()
