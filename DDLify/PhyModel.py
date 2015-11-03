# PhyModel Class
# To Do: Add header information

import xlrd
from utility_funcs import get_column_names, get_column_data, get_index_data, get_primary_key_data
from validate_funcs import schema_list, table_type_list

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
        self.get_tablecomment = self.get_tablecomment()
        self.is_valid = False
        self.validation_message = ''

    def validate_model(self):

        #1) Schema name is valid and matches an existing schema.

        if self.schema in schema_list():
            pass
        else:
            self.validation_message = 'Schema is not in the list'

        #2) Table name is valid and the appropriate amount of characters (27 characters)
        if len(self.table_name) < 28:
            pass
        else:
            self.validation_message = 'Table name greater than 27 characters'

        #3) Test that table type is valid and in the list of  [Dimension, Lookup, Link, Fact, Stage]
        if self.tabletype in table_type_list():
            pass
        else:
            self.validation_message = 'Table Type is not in the list'

        #4) Test that table comment is populated
        if len(self.get_tablecomment) > 0:
            pass
        else:
            self.validation_message = 'Table Name is empty'

        #5) For each column there should be an associated comment.  Failing this test should issue a warning, but not fail the build
        first_sheet = self.book.sheet_by_index(0)
        first_num_rows = first_sheet.nrows
        for x in range(9,first_num_rows):
            if first_sheet.cell(x, 4).value == xlrd.empty_cell.value:
                self.validation_message = "Warning: Comment empty for column %d" % (x-8)
            else:
                pass

        #6) For each column nullity is specified
        for x in range(9,first_num_rows):
            if first_sheet.cell(x, 3).value == xlrd.empty_cell.value:
                self.validation_message = "Nullity not specified for column %d" % (x-8)
            else:
                pass

        #7) For each column datatype is specified
        for x in range(9,first_num_rows):
            if first_sheet.cell(x, 2).value == xlrd.empty_cell.value:
                self.validation_message = "Datatype not specified for column %d" % (x-8)
            else:
                pass

        #8) Each column name is 30 characters or less
        for x in range(9,first_num_rows):
            if len(first_sheet.cell(x, 1).value) > 30:
                self.validation_message = "Length of clolumn name exceeds 30 for column %d" % (x-8)
            else:
                pass

        #9) Tab name for the first tab matches table name
        if first_sheet.name <> str(first_sheet.cell(1, 2).value):
            self.validation_message = "Table name and Tab name are not same"
        else:
            pass

        #10) Index naming convention is followed IX_TableName_XX or IX_TableName_PK for primary keys
        second_sheet = self.book.sheet_by_index(1)
        second_num_rows = second_sheet.nrows
        if second_sheet.cell(1, 0).value <> 'IX_'+ first_sheet.cell(1, 2).value + '_PK':
            self.validation_message = "Index naming convention is not correct"
        else:
            pass

        for x in range(2,second_num_rows):
            if second_sheet.cell(x, 0).value <> 'IX_'+ first_sheet.cell(1, 2).value + '_0%d' %(x-1) :
                self.validation_message = "Index naming convention is not correct"
            else:
                pass

        #11) Index tablespace is specified
        for x in range(1,second_num_rows):
            if second_sheet.cell(x, 1).value == xlrd.empty_cell.value:
                self.validation_message = "Tablespace for Index not specified for " + second_sheet.cell(x, 0).value
            else:
                pass

        #12) Index column is specified
        for x in range(1,second_num_rows):
            if second_sheet.cell(x, 5).value == xlrd.empty_cell.value:
                self.validation_message = "Column for Index not specified for " + second_sheet.cell(x, 0).value
            else:
                pass

        #13) Primary key follows primary key naming standard. PK_TableName
        third_sheet = self.book.sheet_by_index(2)
        third_num_rows = third_sheet.nrows
        if third_sheet.cell(1, 0).value <> 'PK_'+ first_sheet.cell(1, 2).value:
            self.validation_message = "Primary naming convention is not correct"
        else:
            pass

        #14) Primary key index is specified
        for x in range(1,third_num_rows):
            if third_sheet.cell(x, 2).value == xlrd.empty_cell.value:
                self.validation_message = "Primary Key Index not specified for " + third_sheet.cell(x, 0).value
            else:
                pass

        #15) Primary key column is specified
        for x in range(1,third_num_rows):
            if third_sheet.cell(x, 3).value == xlrd.empty_cell.value:
                self.validation_message = "Primary Key column not specified for " + third_sheet.cell(x, 0).value
            else:
                pass

        if self.validation_message == '':
            pass
        else:
            print(self.validation_message)
            exit()


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

    def get_tablecomment(self):

        sheet = self.book.sheet_by_index(0)
        cell = sheet.row(6)[2]

        return str(cell.value)


