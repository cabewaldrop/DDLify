def get_column_names(sheet, row):

        header = sheet.row(row)
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

def get_index_props(sheet):

    col_names = get_column_names(sheet, 0)

    return_list = []
    for row in range(1, sheet.nrows):
        temp_dict = {}
        i = 0
        for cell in sheet.row(row):
            column_name = col_names[i]
            temp_dict[column_name] = str(cell.value)
            i += 1
        return_list.append(temp_dict)

    return return_list