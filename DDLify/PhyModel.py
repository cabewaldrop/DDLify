# PhyModel Class
# To Do: Add header information

import xlrd
import filecmp
import getpass
import difflib

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

        # 1) Schema name is valid and matches an existing schema.

        if self.schema in schema_list():
            pass
        else:
            self.validation_message = 'Schema is not in the list\n'

        # 2) Table name is valid and the appropriate amount of characters (27 characters)
        if len(self.table_name) < 28:
            pass
        else:
            self.validation_message = self.validation_message+'Table name greater than 27 characters\n'

        # 3) Test that table type is valid and in the list of  [Dimension, Lookup, Link, Fact, Stage]
        if self.tabletype in table_type_list():
            pass
        else:
            self.validation_message = self.validation_message+'Table Type is not in the list\n'

        # 4) Test that table comment is populated
        if len(self.get_tablecomment) > 0:
            pass
        else:
            self.validation_message = self.validation_message+'Table Comment is empty\n'

        # 5) For each column there should be an associated comment.
        # Failing this test should issue a warning, but not fail the build
        first_sheet = self.book.sheet_by_index(0)
        first_num_rows = first_sheet.nrows
        for x in range(9, first_num_rows):
            if first_sheet.cell(x, 4).value == xlrd.empty_cell.value:
                print 'Warning: Comment empty for column %d'%(x-8)

        # 6) For each column nullity is specified
        for x in range(9, first_num_rows):
            if first_sheet.cell(x, 3).value == xlrd.empty_cell.value:
                self.validation_message = self.validation_message+'Nullity not specified for column %d\n'%(x-8)

        # 7) For each column datatype is specified
        for x in range(9,first_num_rows):
            if first_sheet.cell(x, 2).value == xlrd.empty_cell.value:
                self.validation_message = self.validation_message+'Datatype not specified for column %d\n'%(x-8)

        # 8) Each column name is 30 characters or less
        for x in range(9,first_num_rows):
            if len(first_sheet.cell(x, 1).value) > 30:
                self.validation_message = self.validation_message+'Length of clolumn name exceeds 30 for column %d\n'%(x-8)

        # 9) Tab name for the first tab matches table name
        if first_sheet.name != str(first_sheet.cell(1, 2).value):
            self.validation_message = self.validation_message+'Table name and Tab name are not same\n'

        # 10) Index naming convention is followed IX_TableName_XX or IX_TableName_PK for primary keys
        second_sheet = self.book.sheet_by_index(1)
        second_num_rows = second_sheet.nrows
        if second_sheet.cell(1, 0).value != 'IX_'+first_sheet.cell(1, 2).value+'_PK':
            self.validation_message = self.validation_message+'Index naming convention is not correct\n'

        for x in range(2, second_num_rows):
            if second_sheet.cell(x, 0).value != 'IX_'+first_sheet.cell(1, 2).value+'_0%d'%(x-1):
                self.validation_message = self.validation_message+'Index naming convention is not correct\n'

        # 11) Index tablespace is specified
        for x in range(1, second_num_rows):
            if second_sheet.cell(x, 1).value == xlrd.empty_cell.value:
                self.validation_message = self.validation_message+'Tablespace for Index not specified for'+second_sheet.cell(x, 0).value+'\n'

        # 12) Index column is specified
        for x in range(1, second_num_rows):
            if second_sheet.cell(x, 5).value == xlrd.empty_cell.value:
                self.validation_message = self.validation_message+'Column for Index not specified for ' + second_sheet.cell(x, 0).value+'\n'

        # 13) Primary key follows primary key naming standard. PK_TableName
        third_sheet = self.book.sheet_by_index(2)
        third_num_rows = third_sheet.nrows
        if third_sheet.cell(1, 0).value != 'PK_'+first_sheet.cell(1, 2).value:
            self.validation_message = self.validation_message+'Primary naming convention is not correct\n'

        # 14) Primary key index is specified
        for x in range(1, third_num_rows):
            if third_sheet.cell(x, 2).value == xlrd.empty_cell.value:
                self.validation_message = self.validation_message+'Primary Key Index not specified for'+third_sheet.cell(x, 0).value+'\n'

        # 15) Primary key column is specified
        for x in range(1, third_num_rows):
            if third_sheet.cell(x, 3).value == xlrd.empty_cell.value:
                 self.validation_message = self.validation_message+'Primary Key column not specified for'+third_sheet.cell(x, 0).value+'\n'

        if self.validation_message == '':
            pass
        else:
            print(self.validation_message)
            exit()

    def create_ddl_file(self):
        """
        This function uses values contained in the spreadsheet to populate a DDL .sql file with table creation SQL code.
        """
        first_sheet = self.book.sheet_by_index(0)
        first_num_rows = first_sheet.nrows
        second_sheet = self.book.sheet_by_index(1)
        second_num_rows = second_sheet.nrows
        third_sheet = self.book.sheet_by_index(2)
        third_num_rows = third_sheet.nrows
        schema = first_sheet.cell(0, 2).value
        table_name = first_sheet.cell(1, 2).value
        tablespace = first_sheet.cell(5, 2).value
        system = schema.split('_', 1)[0]
        table_comment = first_sheet.cell(6, 2).value

        f = open(table_name + '.sql', 'w+')
        f.write('-' * 80)
        f.write('\n-- ' + schema + '.' + table_name)
        f.write('\n\nBEGIN\n    EXECUTE IMMEDIATE \'DROP TABLE ' + schema + '.' + table_name + ' CASCADE CONSTRAINTS PURGE\';\n'
                'EXCEPTION WHEN OTHERS THEN\n    IF SQLCODE != -942 THEN\n        RAISE;\n    END IF;\nEND;\n/\n\n\n\n'
                '\nCREATE TABLE ' + schema + '.' + table_name + '\n( ')

        for i, x in enumerate(range(9, first_num_rows)):
            if i > 0:
                f.write('\n, ',)
            f.write('%-*s %-*s %s' % (35, (first_sheet.cell(x, 1).value), 20, (first_sheet.cell(x, 2).value), (first_sheet.cell(x, 3).value)))
        f.write('\n)\nCOMPRESS FOR OLTP\nTABLESPACE ' + tablespace + '\n')
        if first_sheet.cell(4, 2).value in ('Daily', 'Monthly', 'DAILY', 'MONTHLY', 'DLY', 'MTHLY', 'Dly', 'Mthly'):
            f.write('PARTITION BY LIST (DAY_ID)\n( PARTITION P20120131 VALUES (20120131)\n  LOGGING\n  COMPRESS FOR QUERY LOW\n  TABLESPACE ' + tablespace + '\n)\nENABLE ROW MOVEMENT\n;\n\n\n' )
        else:
            f.write(';\n\n\n')
        if '_OWNER' in schema:
            f.write('GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_JOBS;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_OWNER_RW;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ETL_ADMIN;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO ' + system + '_OWNER_READ;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO MSTR_ADMIN;\n'
                    'GRANT SELECT, INSERT, UPDATE, ALTER, DELETE ON ' + schema + '.' + table_name + ' TO DEVELOPER_RW;\n\n')
        elif '_STG' in schema:
            f.write('GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_JOBS;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_STG_RW;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO ' + system + '_STG_READ;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ETL_ADMIN;\n'
                    'GRANT SELECT, INSERT, UPDATE, ALTER, DELETE ON ' + schema + '.' + table_name + ' TO DEVELOPER_RW;\n\n')
        elif '_JOBS' in schema:
            f.write('GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ETL_ADMIN;\n'
                    'GRANT SELECT, INSERT, UPDATE, ALTER, DELETE ON ' + schema + '.' + table_name + ' TO DEVELOPER_RW;\n\n')
        elif '_CNTL' in schema:
            f.write('GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_JOBS;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ETL_ADMIN;\n'
                    'GRANT SELECT, INSERT, UPDATE, ALTER, DELETE ON ' + schema + '.' + table_name + ' TO DEVELOPER_RW;\n\n')
        elif '_APPL' in schema:
            f.write('GRANT SELECT ON ' + schema + '.' + table_name + ' TO ' + system + '_APPL_READ;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_APPL_RW;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ' + system + '_JOBS;\n'
                    'GRANT DELETE, INSERT, SELECT, UPDATE ON ' + schema + '.' + table_name + ' TO ETL_ADMIN;\n'
                    'GRANT SELECT, INSERT, UPDATE, ALTER, DELETE ON ' + schema + '.' + table_name + ' TO DEVELOPER_RW;\n\n')
        if 'DIM_TIME' or 'DIM_DAY' or 'DIM_MTH' or 'DIM_QTR' or 'DIM_WK' or 'DIM_YR' in table_name:
            f.write('GRANT SELECT ON ' + schema + '.' + table_name + ' TO COMM_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO COMM_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO COMM_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CA_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CA_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CA_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO OAO_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO OAO_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO OAO_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO MRDC_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO MRDC_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO MRDC_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CEN_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CEN_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CEN_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CARD_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CARD_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CARD_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CLO_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CLO_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CLO_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO DF_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO DF_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO DF_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CMPGN_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CMPGN_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO CMPGN_JOBS;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO PROS_OWNER;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO PROS_STG;\n'
                    'GRANT SELECT ON ' + schema + '.' + table_name + ' TO PROS_JOBS;\n')
        if 'DIM_ACCT_CPS' or 'DIM_CUST_CPS' or 'FACT_ACCT_PRFTBLY_12MRA' or 'FACT_ACCT_PRFTBLY_MTHLY' or 'FACT_ACCT_PRFTBLY_YTD' in table_name:
            f.write('GRANT ALTER ON ' + schema + '.' + table_name + ' TO SDSS_JOBS;\n')
        if 'CA_FACT_ACCT_PRFTBLY_MNTHLY' in table_name:
            f.write('GRANT ALTER ON ' + schema + '.' + table_name + ' TO CA_JOBS;\n')

        for i, x in enumerate(range(1, second_num_rows)):
            index_type = ('UNIQUE INDEX' if second_sheet.cell(x, 2).value == 'Y' else 'INDEX')
            f.write('CREATE %s %s.%s ON %s.%s (%s %s)\n' % (index_type, schema, second_sheet.cell(x, 0).value, schema, table_name, second_sheet.cell(x, 5).value, second_sheet.cell(x, 6).value))
            if second_sheet.cell(x, 4).value == 'N':
                f.write('NOLOGGING\n')
            else:
                f.write('LOGGING\n')
            if second_sheet.cell(x, 3).value == 'N':
                f.write('NOCOMPRESS\n')
            else:
                f.write('COMPRESS\n')
            f.write('TABLESPACE ' + tablespace + '\n;\n\n\n')
        else:
            f.write('\n')

        for i, x in enumerate(range(1, third_num_rows)):
            f.write('ALTER TABLE ' + schema + '.' + table_name + ' ADD CONSTRAINT ' + third_sheet.cell(x, 0).value + ' PRIMARY KEY (' + third_sheet.cell(x, 3).value + ') USING INDEX ' + schema + '.' + third_sheet.cell(x, 2).value + ';\n\n\n')
        else:
            f.write('\n')
        f.write('COMMENT ON TABLE %s.%-*s IS \'%s\';' % (schema, 48, table_name, table_comment))
        for x in range(9, first_num_rows):
            f.write('\nCOMMENT ON COLUMN %s.%s.%-*s IS \'%s\';' % (schema, table_name, 38, (first_sheet.cell(x, 1).value), (first_sheet.cell(x, 4).value)))
        f.close()

    print filecmp.cmp('C:\Users\\xsc1712\PycharmProjects\DDLify\DDL_OUT\owner.sql', 'C:\Users\\xsc1712\PycharmProjects\DDLify\Tests\correct_ddl.sql')

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


