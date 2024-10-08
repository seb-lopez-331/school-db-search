import csv, time

# Constants
SCHOOL_NAME_COLUMN = 'SCHNAM05'
CITY_COLUMN = 'LCITY05'
STATE_COLUMN = 'LSTATE05'
PUNCTUATION = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

# We use these as stop words because we are looking for schools anyways
STOP_WORDS = {'school', 'academy', 'institute'}

# These weights are configurable
EXACT_MATCH_WEIGHT = 0.5
PARTIAL_MATCH_WEIGHT = 0.3
CITY_MATCH_WEIGHT = 0.05
STATE_MATCH_WEIGHT = 0.01

# Allows the school_search script to search by state
STATE_ABBREVIATION = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}


def load_csv(filename: str, encoding: str = 'Windows-1252') -> list[dict[str, any]]:
    loaded_data = []

    with open(filename, mode='r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        print(f'File {filename} opened successfully.')

        column_names = next(csv_reader)
        for row in csv_reader:
            entry = {}
            for index, name in enumerate(column_names):
                entry[name] = row[index]
            loaded_data.append(entry)

    print(f'Loaded data in {filename} successfully.')
    return loaded_data


def abbreviate_states(text: str) -> str:
    for full_state in STATE_ABBREVIATION:
        if full_state.lower() in text:
            text = text.replace(full_state, STATE_ABBREVIATION[full_state])
    return text


def tokenize(text: str, is_query_text: bool = False) -> set[str]:
    # We want to replace all punctuation characters with space
    text = text.lower()
    if is_query_text:
        text = abbreviate_states(text)
    text = ''.join(' ' if char in PUNCTUATION else char for char in text)
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


def compute_state_match(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    state_tokens = tokens[STATE_COLUMN]
    total_matches = sum(1 for word in keywords if word in state_tokens)
    return total_matches / len(keywords)


def compute_rank(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    exact_match = compute_exact_match(tokens, keywords)
    partial_match = compute_partial_match(tokens, keywords)
    city_match = compute_city_match(tokens, keywords)
    state_match = compute_state_match(tokens, keywords)
    return EXACT_MATCH_WEIGHT * exact_match + \
        PARTIAL_MATCH_WEIGHT * partial_match + \
        CITY_MATCH_WEIGHT * city_match + \
        STATE_MATCH_WEIGHT * state_match
    

loaded_data = load_csv("school_data.csv")
tokenized_data = batch_tokenize(loaded_data)
print()


def search_schools(query: str, n: int = 3) -> None:
    top_results = []
    keywords = tokenize(query, is_query_text=True)
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

option = input('Please specify here if you wish to supply your own queries (Y) or use the built-in queries here (N).\n> ')
while option not in ['N', 'Y']:
    option = input(f'{option} is not a valid option. Would you like to supply your own queries? Specify Y if yes, or N if no.\n> ')

if option == 'N':
    search_schools("elementary school highland park")
    search_schools("jefferson belleville")
    search_schools("riverside school 44")
    search_schools("granada charter school")
    search_schools("foley high alabama")
    search_schools("KUSKOKWIM")
else:
    keep_going = 'Y'
    while keep_going == 'Y':
        query = input('Please specify your query here\n> ')
        search_schools(query)
        keep_going = input('Would you like to continue (Y/N)?\n> ')
        while keep_going not in ['N', 'Y']:
            keep_going = input(f'{keep_going} is not a valid option. Would you like to continue? Specify Y if yes, or N if no.\n> ')

