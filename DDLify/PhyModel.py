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
