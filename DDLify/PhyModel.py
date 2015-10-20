# PhyModel Class
# To Do: Add header information

import xlrd
from utility_funcs import get_column_names, get_column_data, get_index_data, get_primary_key_data

class PhyModel(object):

    def __init__(self, filename):

        try:
            self.book = xlrd.open_workbook(filename)
        except:
            raise ValueError("Unable to open filename: {0}".format(filename))

        self.indexes = self.get_indexes()
        self.columns = self.get_columns()
        self.primary_key = self.get_primary_key()
        self.schema = self.get_schema()
        self.tablespace = self.get_tablespace()
        self.tabletype = self.get_tabletype()
        self.table_name = self.get_table_name()
        self.is_valid = False
        self.validation_message = ''

    def validate_model(self):
        """TO-DO: Create validation code here. This code should include checks for the following:
           1) Schema name is valid and matches an existing schema.
           2) Table name is valid and the appropriate amount of characters (24 characters)
           3) Test that table type is valid and in the list of  [Dimension, Lookup, Link, Fact, Stage]
           4) Test that table comment is populated
           5) For each column there should be an associated comment.  Failing this test should issue a warning, but not fail the build
           6) For each column nullity is specified
           7) For each column datatype is specified
           8) Each column name is 30 characters or less
           9) Tab name for the first tab matches table name
          10) Index naming convention is followed IX_TableName_XX or IX_TableName_PK for primary keys
          11) Index tablespace is specified
          12) Index column is specified
          13) Primary key follows primary key naming standard. PK_TableName
          14) Primary key index is specified
          15) Primary key column is specified
        """

    def create_ddl_file(self):
        """
        TO-DO: Create routine to output DDL using the attributes gathered during initialization.  This DDL should have
        structure matching our current ddl files and should be output into the working directory under owner, stage, or
        amalgamation.
        """
    def get_columns(self):

        sheet = self.book.sheet_by_index(0)
        col_names = get_column_names(sheet, 8)
        column_data = get_column_data(col_names, sheet)

        return column_data

    def get_indexes(self):

        sheet = self.book.sheet_by_index(1)
        ix_props = get_index_data(sheet)

        return ix_props


    def get_primary_key(self):

        sheet = self.book.sheet_by_index(2)
        primary_key = get_primary_key_data(sheet)

        return primary_key

    def get_schema(self):

        sheet = self.book.sheet_by_index(0)
        cell = sheet.row(0)[2]
        return str(cell.value)

    def get_tablespace(self):

        sheet = self.book.sheet_by_index(0)
        cell = sheet.row(5)[2]

        return str(cell.value)

    def get_table_name(self):

        sheet = self.book.sheet_by_index(0)
        cell = sheet.row(1)[2]

        return str(cell.value)

    def get_tabletype(self):

        sheet = self.book.sheet_by_index(0)
        cell = sheet.row(2)[2]

        return str(cell.value)
