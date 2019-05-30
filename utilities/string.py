import re


def convert_column_to_string(column):
    return re.sub(r'.*\.', '', str(column))
