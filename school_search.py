import csv

"""
We can use a predefined list of states, cities, and schools
"""
# Constants
SCHOOL_NAME_COLUMN = 'SCHNAM05'
CITY_COLUMN = 'LCITY05'
STATE_COLUMN = 'LSTATE05'

# We use these as stop words because we are looking for schools anyways
STOP_WORDS = set([
    'school', 
    'academy', 
    'institute'
])

def load_csv(filename: str, encoding: str = 'Windows-1252') -> tuple[list[dict[str, any]], list[str]]:
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


def tokenize(text: str) -> list[str]:
    # We want to replace all punctuation characters with space
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    text = text.lower()
    text = ''.join(' ' if char in punctuation else char for char in text)
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    tokens = text.split()
    filtered = filter(lambda word: word not in STOP_WORDS, tokens)
    return list(filtered)


def compute_exact_match(entry: dict[str, any], keywords: list[str]) -> float:
    school_name_tokens = tokenize(entry[SCHOOL_NAME_COLUMN])
    city_tokens = tokenize(entry[CITY_COLUMN])
    state_token = entry[STATE_COLUMN].lower()

    keywords_set = set(keywords)
    
    return 1.0 if (keywords_set.issubset(school_name_tokens) or
                 keywords_set.issubset(city_tokens) or
                 keywords_set.issubset([state_token])) else 0.0



def compute_partial_match(entry: dict[str, any], keywords: list[str]) -> float:
    school_name_tokens = tokenize(entry[SCHOOL_NAME_COLUMN])
    city_tokens = tokenize(entry[CITY_COLUMN])
    state_token = entry[STATE_COLUMN].lower()

    all_tokens = set(school_name_tokens + city_tokens + [state_token])

    total_matches = 0
    for word in keywords:
        if word in all_tokens:
            total_matches += 1
    
    return float(total_matches) / len(keywords)


def compute_city_match(entry: dict[str, any], keywords: list[str]) -> float:
    city_tokens = set(tokenize(entry[CITY_COLUMN]))

    total_matches = 0
    for word in keywords:
        if word in city_tokens:
            total_matches += 1
    
    return float(total_matches) / len(keywords)


def compute_rank(entry: dict[str, any], keywords: list[str]) -> float:
    exact_match = compute_exact_match(entry, keywords)
    partial_match = compute_partial_match(entry, keywords)
    location_score = compute_city_match(entry, keywords)
    final_score = 0.5*exact_match + 0.3*partial_match + 0.05*location_score
    return final_score
    

loaded_data, column_names = load_csv("school_data.csv")
print()


def search_schools(query: str, n: int = 3) -> list[dict[str, any]]:
    keywords = tokenize(query)
    top_results = []

    for entry in loaded_data:
        score = compute_rank(entry, keywords)
        
        if len(top_results) < n:
            top_results.append({'entry': entry, 'score': score})
            continue

        # This may be optimized for a heap if we choose n entries, but with 3 entries it is faster as is.
        min_index = 0

        for i in range(1, n): # This is O(1) for small n, like n = 3.
            if top_results[i]['score'] <= top_results[min_index]['score']:
                min_index = i

        if score >= top_results[min_index]['score']:
            top_results.pop(min_index)
            top_results.append({'entry': entry, 'score': score})
    
    top_results.sort(key=lambda result: result['score'])

    print('Search results for query: ', query)
    for result in top_results[::-1]:
        entry = result['entry']
        school = entry[SCHOOL_NAME_COLUMN]
        city = entry[CITY_COLUMN]
        state = entry[STATE_COLUMN]
        print(f'{school}, {city}, {state}, {result["score"]}')
