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
LOCATION_MATCH_WEIGHT = 0.05

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


def tokenize(text: str) -> set[str]:
    # We want to replace all punctuation characters with space
    text = text.lower()
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


def compute_rank(tokens: dict[str, set[str]], keywords: set[str]) -> float:
    exact_match = compute_exact_match(tokens, keywords)
    partial_match = compute_partial_match(tokens, keywords)
    location_match = compute_city_match(tokens, keywords)
    return EXACT_MATCH_WEIGHT*exact_match + PARTIAL_MATCH_WEIGHT*partial_match + LOCATION_MATCH_WEIGHT*location_match
    

loaded_data = load_csv("school_data.csv")
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