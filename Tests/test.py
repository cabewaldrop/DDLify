import unittest
from DDLify import PhyModel

class TestPhyModel(unittest.TestCase):

    def setUp(self):

        self.book = PhyModel.PhyModel('test_model.xls')

    def test_bad_file_name_throws_error(self):

        with self.assertRaises(ValueError):
            PhyModel.PhyModel('filename.xls')

    def test_primary_key_exists(self):

        self.assertEqual(self.book.primary_key, '')

    def test_index_list(self):

        self.assertEqual(self.book.indexes, [])

    def test_column_list(self):

        self.assertEqual(self.book.columns, [{'Order '1.0',
                                             'TEST_COLUMN_1',
                                              'INTEGER',
                                              'NULL',
                                              'TEST COLUMN: COMMENT ONE',
                                              '2.0'
                                              'TEST_COLUMN_2',
                                              'VARCHAR2(20)',
                                              'NULL',
                                              'TEST COLUMN: COMMENT TWO'])

if __name__ == '__main__':
    unittest.main()