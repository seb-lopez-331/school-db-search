import csv, time

"""
We can use a predefined list of states, cities, and schools
"""
# Constants
SCHOOL_NAME_COLUMN = 'SCHNAM05'
CITY_COLUMN = 'LCITY05'
STATE_COLUMN = 'LSTATE05'

# We use these as stop words because we are looking for schools anyways
STOP_WORDS = {'school', 'academy', 'institute'}

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


def tokenize(text: str) -> set[str]:
    # We want to replace all punctuation characters with space
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    text = text.lower()
    text = ''.join(' ' if char in punctuation else char for char in text)
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    tokens = text.split()
    filtered = filter(lambda word: word not in STOP_WORDS, tokens)
    return set(filtered)


def batch_tokenize(data: list[dict[str, any]]) -> list[dict[str, set[str]]]:
    tokenized_data = []
    for entry in data:
        tokens = {
            SCHOOL_NAME_COLUMN: tokenize(entry[SCHOOL_NAME_COLUMN]),
            CITY_COLUMN: tokenize(entry[CITY_COLUMN]),
            STATE_COLUMN: tokenize(entry[STATE_COLUMN])
        }
        tokenized_data.append(tokens)
    return tokenized_data

    
def compute_exact_match(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    school_name_tokens = tokens[SCHOOL_NAME_COLUMN]
    city_tokens = tokens[CITY_COLUMN]
    state_tokens = tokens[STATE_COLUMN]
    
    return 1.0 if (keywords.issubset(school_name_tokens) or
                 keywords.issubset(city_tokens) or
                 keywords.issubset(state_tokens)) else 0.0


def compute_partial_match(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    school_name_tokens = tokens[SCHOOL_NAME_COLUMN]
    city_tokens = tokens[CITY_COLUMN]
    state_tokens = tokens[STATE_COLUMN]

    all_tokens = school_name_tokens | city_tokens | state_tokens
    total_matches = sum(1 for word in keywords if word in all_tokens)
    
    return total_matches / len(keywords)


def compute_city_match(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    city_tokens = tokens[CITY_COLUMN]
    total_matches = sum(1 for word in keywords if word in city_tokens)
    return total_matches / len(keywords)


def compute_rank(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    exact_match = compute_exact_match(tokens, keywords)
    partial_match = compute_partial_match(tokens, keywords)
    location_score = compute_city_match(tokens, keywords)
    final_score = 0.5*exact_match + 0.3*partial_match + 0.05*location_score
    return final_score
    

loaded_data, column_names = load_csv("school_data.csv")
tokenized_data = batch_tokenize(loaded_data)
print()


def search_schools(query: str, n: int = 3) -> list[dict[str, any]]:
    keywords = tokenize(query)
    top_results = []
    start_time = time.time()

    for entry, tokens in zip(loaded_data, tokenized_data):
        score = compute_rank(tokens, keywords)
        
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
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    top_results.sort(key=lambda result: result['score'])

    print(f'Results for: "{query}" (search took: {elapsed_time:.3f}s)')
    for i, result in enumerate(top_results[::-1]):
        if result['score'] == 0:
            break
        entry = result['entry']
        school = entry[SCHOOL_NAME_COLUMN]
        city = entry[CITY_COLUMN]
        state = entry[STATE_COLUMN]
        print(f'{i + 1}. {school}')
        print(f'   {city}, {state}')

search_schools("elementary school highland park")
search_schools("jefferson belleville")
search_schools("riverside school 44")
search_schools("granada charter school")
search_schools("foley high alabama")
search_schools("KUSKOKWIM")