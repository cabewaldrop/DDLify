# PhyModel Class
# To Do: Add header information

import xlrd
from utility_funcs import get_column_names, get_column_data

class PhyModel(object):

    def __init__(self, filename):

        try:
            self.book = xlrd.open_workbook(filename)
        except:
            raise ValueError("Unable to open filename: {0}".format(filename))

        self.indexes = []
        self.columns = self.get_columns()
        self.primary_key = ''

    def get_columns(self):

        sheet = self.book.sheet_by_index(0)

        col_names = get_column_names(sheet)

        column_data = get_column_data(col_names, sheet)

        return column_data


