import csv

"""
We can use a predefined list of states, cities, and schools
"""

def load_csv(
    filename: str, encoding: str = 'Windows-1252'
) -> tuple[list[dict[str, any]], list[str]]:
    """This function loads data from an inputted CSV file with the specified encoding, defaulted to Windows-1252.

    If the file does not exist or if there are any errors associated with loading the data, we exit from the script 
    with an error message. The function returns a list of dicts that each represent a row in the data. It also 
    returns a reference for the columns. 
    
    Below is an example of how the first row of data will be dynamically stored:

    {
        "NCESSCH": "010000200277",
        "LEAID": "0100002",
        "LEANM05": "ALABAMA YOUTH SERVICES",
        "SCHNAM05": "SEQUOYAH SCHOOL - CHALKVILLE CAMPUS",
        "LCITY05": "PINSON",
        "LSTATE05": "AL",
        "LATCOD": "33.674697",
        "LONCOD": "-86.627775",
        "MLOCALE": "3",
        "ULOCALE": "41",
        "status05": "1"
    }

    Parameters
    ----------
    filename: str
        The name of the CSV file
    encoding: str
        The encoding to use for loading the CSV file
    
    Returns
    -------
    tuple[list[dict[str, any]], list[str]]
        A tuple that contains a list of dicts that represent each row, and a list with strings that represent the names
        of each column.
    """
    loaded_data = []

    try:
        with open(filename, mode='r', encoding=encoding) as file:
            csv_reader = csv.reader(file)
            print(f'File {filename} opened successfully.')

            # Gather a list with the column names
            column_names = next(csv_reader)
            
            # Construct entry objects that map column_name -> value
            # Below is an example:
            # {
            #     "NCESSCH": "010000200277",
            #     "LEAID": "0100002",
            #     "LEANM05": "ALABAMA YOUTH SERVICES",
            #     "SCHNAM05": "SEQUOYAH SCHOOL - CHALKVILLE CAMPUS",
            #     "LCITY05": "PINSON",
            #     "LSTATE05": "AL",
            #     "LATCOD": "33.674697",
            #     "LONCOD": "-86.627775",
            #     "MLOCALE": "3",
            #     "ULOCALE": "41",
            #     "status05": "1"
            # }
            try:
                for line, row in enumerate(csv_reader):
                    entry = {}
                    for j, name in enumerate(column_names):
                        entry[name] = row[j]
                    loaded_data.append(entry)

            except UnicodeDecodeError as e:
                print(f'Error parsing data file on line {line + 1}. The encoding {encoding} is incorrect here: {e}')
                exit(1)

            except IndexError as e:
                print(f'Error parsing data file on line {line}. This is likely due to mismatched numbers of columns on a row with the schema: {e}')
                exit(1)

    except FileNotFoundError | PermissionError | OSError as e:
        print(f'Error loading file: {e}')
        exit(1)
    
    print(f'Loaded data in {filename} successfully.')
    return loaded_data, column_names


def find_distinct(data: dict[str, any], column_names: list[str], column: str) -> list[str]:
    if column not in column_names:
        print(f'Error counting schools: column {column} not found in inputted columns {column_names}.')
        exit(1)
    
    distinct = set()
    column_set = set(column_names)

    for line, entry in enumerate(data):
        # Check here if all the required keys in the schema are present
        if column_set != entry.keys():
            key_list = list(entry.keys())
            diff = list(entry.keys() ^ column_set)
            print(
                f'Error counting schools: Entry #{line} has keys {key_list} when the expected keys are '
                f'{column_names}.\n'
                f'Here is a diff for ease of reference: {diff}.'
            )
            exit(1)
        
        distinct.add(entry[column])

    return distinct

loaded_data, column_names = load_csv("school_data.csv")
SCHOOL_NAME_COLUMN = 'SCHNAM05'
CITY_COLUMN = 'LCITY05'
STATE_COLUMN = 'LSTATE05'


distinct_schools = find_distinct(loaded_data, column_names, column=)
distinct_cities = find_distinct(loaded_data, column_names, column=)

