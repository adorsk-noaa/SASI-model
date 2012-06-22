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

		class TestClass(object):
			attr1 = None
			attr2 = None
			attr3 = None
			attr4 = None

		self.model = TestClass

		columns = [
				{'name': 'attr1', 'type': 'int'},
				{'name': 'attr2', 'type': 'str'},
				{'name': 'attr3', 'type': 'float'},
				{'name': 'attr4'},
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
		csv_dao = CSV_DAO(self.csv_filename, model=self.model)

		all_results = csv_dao.all()

		queried_results =csv_dao.query(filters=[
			{'entity': {'expression': '{attr1}'}, 'op': 'in', 'value': [2,3]}
			])
	

if __name__ == '__main__':
	unittest.main()
