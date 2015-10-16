def get_column_names(sheet):

        header = sheet.row(8)
        col_names = []
        for cell in header:
            col_names.append(str(cell.value))

        return col_names

def get_column_data(col_names, sheet):

        return_list = []
        for row in range(9, sheet.nrows):
            temp_dict = {}
            i = 0
            for cell in sheet.row(row):
                column_name = col_names[i]
                temp_dict[column_name] = str(cell.value)
                i += 1
            return_list.append(temp_dict)

        return return_list