import pandas


# appends a new column with binaryzed data to dataframe
def mark_up_area_of_testing(dataframe, column_name, area_of_testing, prefix, value_patterns):
        dataframe[area_of_testing+prefix] = dataframe[column_name].apply(apply_mark_up_area_of_testing, args=(value_patterns,))
        return dataframe


def apply_mark_up_area_of_testing(x, value_patterns):
        for val in value_patterns.split("|"):
                if val.strip() in str(x).split(","):
                        return 1
        return 0
        

# appends additional column which represents data that isn't related to marked up fields
def mark_up_other_data(dataframe, marked_up_columns):
    dataframe['Other_lab'] = '0'
    # replaces field value to 1 when summ of the fields from marked_up_columns is 0
    dataframe['Other_lab'] = dataframe['Other_lab'].replace(['0'], '1').where(dataframe[marked_up_columns].sum(axis=1) == 0, 0).apply(int)
    return dataframe

