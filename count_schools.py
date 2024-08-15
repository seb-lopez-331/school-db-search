import csv, time, itertools

def load_csv(filename, encoding='Windows-1252'):
    """This function loads data from an inputted CSV file with the specified encoding,
    defaulted to Windows-1252.

    If the file does not exist or if there are any errors associated with loading
    the data, we exit from the script with an error message. The function returns 
    a list of dicts that each represent a row in the data. Below is an example
    of how the first row of data will be dynamically stored:

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
    list
        a list of dicts that represent each row
    """
    loaded_data = []

    try:
        with open(filename, mode='r', encoding=encoding) as file:
            csv_reader = csv.reader(file)
            print(f'File {filename} opened successfully')

            # Gather a list with the column names
            column_names = next(csv_reader)
            print(f'Column names: {column_names}')
            
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
                    print(f'Parsing row {line}')
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

    except Exception as e:
        print(f'Error loading file: {e}')
        exit(1)
    
    return loaded_data


loaded_data = load_csv("school_data.csv")