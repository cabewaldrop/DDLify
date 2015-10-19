import unittest
from DDLify import PhyModel

class TestPhyModel(unittest.TestCase):

    def setUp(self):

        self.book = PhyModel.PhyModel('test_model.xls')
        self.bad_book = PhyModel.PhyModel('bad_model.xls')

    def test_bad_file_name_throws_error(self):

        with self.assertRaises(ValueError):
            PhyModel.PhyModel('filename.xls')

    def test_primary_key_data(self):

        self.assertEqual(self.book.primary_key, [{'Key': 'PK_DIM_TEST',
                                                  'Type': 'Primary Key',
                                                  'Index': 'IX_DIM_TEST_PK',
                                                  'Columns': 'TEST_COLUMN_1'}])

    def test_index_list(self):

        self.assertEqual(self.book.indexes, [{'Index': 'IX_DIM_TEST_PK',
                                              'Tablespace': 'TEST_DATA',
                                              'Is Unique?': 'Y',
                                              'Is Compression Enabled?': 'N',
                                              'Is Logging Enabled?': 'N',
                                              'Columns': 'TEST_COLUMN_1',
                                              'Order': 'ASC'}])

    def test_column_list(self):

        self.assertEqual(self.book.columns, [{'Order': '1.0',
                                              'Column': 'TEST_COLUMN_1',
                                              'Datatype': 'INTEGER',
                                              'Nullity': 'NULL',
                                              'Comment': 'TEST COLUMN: COMMENT ONE'},
                                             {'Order': '2.0',
                                              'Column': 'TEST_COLUMN_2',
                                              'Datatype': 'VARCHAR2(20)',
                                              'Nullity': 'NULL',
                                              'Comment': 'TEST COLUMN: COMMENT TWO'}])

    def test_tablespace(self):

        self.assertEqual(self.book.tablespace, 'TEST_DATA')

    def test_schema(self):

        self.assertEqual(self.book.schema, 'TEST_OWNER')

    def test_tabletype(self):

        self.assertEqual(self.book.tabletype, 'Dimension')

    def test_table_name(self):

        self.assertEqual(self.book.table_name, 'DIM_TEST')

    def test_validation_on_correct_model(self):

        self.assertTrue(self.book.is_valid)

    def test_validation_on_incorrect_model(self):

        self.assertFalse(self.bad_book.is_valid)

    def test_validation_message_on_incorrect_model(self):
        """
        TO-DO: Update this test so that it validates the actual message sent by the validation routine
        """
        self.assertEqual(self.bad_book.validation_message, 'Test')


if __name__ == '__main__':
    unittest.main()