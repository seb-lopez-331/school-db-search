import csv
"""
I have taken the liberty to write documentation here for my own ease of reference.

Here is a layout of the records stored in school_data.csv:

Variable    Start       End         Field    Data 
Name        Position    Position    Length   Type    Description      
NCESSCH           01          12        12     AN    ID assigned by NCES to each school. 
LEAID             13          19         7     AN    Unique Agency ID (NCES assigned) 
LEANM05           20          79        60     AN    Name of Operating Agency 
SCHNAM05          80         129        50     AN    School Name 
LCITY05          130         159        30     AN    Location City Name 
LSTATE05         160         161         2     AN    Location USPS State Abbreviation 
LATCOD           162         170         9      N    Latitude 
LONCOD           171         181        11      N    Longitude 
MLOCALE          182         182         1     AN    Metro-centric locale code:
ULOCALE          183         184         2     AN    Urban-centric locale code:
STATUS05         185         185         1     AN    NCES code for the school status 


Here is a breakdown of MLOCALE:
1 = Large City: A principal city of a Metropolitan Core Based Statistical Area (CBSA), with the city having a 
    population greater than or equal to 250,000.  

2 = Mid-Size City: A principal city of a Metropolitan CBSA, with the city having a population less than 250,000.

3 = Urban Fringe of a Large City: Any incorporated place, Census-designated place, or non-place territory within a 
    Metropolitan CBSA  of a Large City and defined as urban by the Census Bureau. 

4 = Urban Fringe of a Mid-Size City: Any incorporated place, Census-designated place, or non-place territory within a
     CBSA of a Mid-Size City and defined as urban by the Census Bureau.  

5 = Large Town: An incorporated place or Census designated place with a population greater than or equal to 25,000 and 
    located outside a Metropolitan CBSA or inside a Micropolitan CBSA.  

6 = Small Town: An incorporated place or Census designated place with a population less than 25,000 and greater than 
    or equal to 2,500 and located outside a Metropolitan CBSA or inside a Micropolitan CBSA.  

7 = Rural, outside CBSA: Any incorporated place, Census-designated place, or non-place territory not within a 
    Metropolitan CBSA or within a Micropolitan CBSA and defined as rural by the Census Bureau.  

8 = Rural, inside CBSA: Any incorporated place, Census-designated place, or non-place territory within a 
    Metropolitan CBSA and defined as rural by the Census Bureau. 

    
Here is a breakdown of ULOCALE:
11 = City: Large: Territory inside an urbanized area and inside a principal city with population of 250,000 or more.

12 = City: Midsize: Territory inside an urbanized area and inside a principal city with population less than 250,000 
    and  greater than or equal to 100,000. 

13 = City: Small: Territory inside an urbanized area and inside a principal city with population less than 100,000. 

21 = Suburb: Large: Territory outside a principal city and inside an urbanized area with population of 250,000 or more. 

22 = Suburb: Midsize: Territory outside a principal city and inside an urbanized area with population less than 250,000 
    and greater than or equal to 100,000. 
    
23 = Suburb: Small: Territory outside a principal city and inside an urbanized area with population less than 100,000. 

31 = Town: Fringe: Territory inside an urban cluster that is less than or equal to 10 miles from an urbanized area. 

32 = Town: Distant: Territory inside an urban cluster that is more than 10 miles and less than or equal to 35 miles 
    from an urbanized area. 
    
33 = Town: Remote: Territory inside an urban cluster that is more than 35 miles of an urbanized area. 

41 = Rural: Fringe: Census-defined rural territory that is less than or equal to 5 miles from an urbanized area, as well 
    as rural territory that is less than or equal to 2.5 miles from an urban cluster.  
    
42 = Rural: Distant: Census-defined rural territory that is more than 5 miles but less than or equal to 25 miles from 
    an urbanized area, as well as rural territory that is more than 2.5 miles but less than or equal to 10 miles from 
    an urban cluster. 
    
43 = Rural: Remote: Census-defined rural territory that is more than 25 miles from an urbanized area and is also more 
    than 10 miles from an urban cluster.

    
Finally, here is a breakdown for STATUS05
1 = School was operational at the time of the last report and is currently operational. 

2 = School has closed since the time of the last report. 

3 = School has been opened since the time of the last report. 

4 = School was operational at the time of the last report but was not on the CCD list at that time. 

5 = School was listed in previous year's CCD school universe as being affiliated with a different education agency. 

6 = School is temporarily closed and may reopen within 3 years. 

7 = School is scheduled to be operational within 2 years. 

8 = School was closed on previous year's file but has reopened. 
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


def count_schools(
    data: list[dict[str, any]], column_names: list[str], school_name_column: str
) -> int:
    """This function counts the total schools in the provided loaded data.

    This function makes assertions on whether the data passed in follows the proper schema. And then it
    gathers all of the distinct schools, specified by the school_name_column agument, and counts them.
    
    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file.
    column_names: set[str]
        A set of strings that is supposed to represent each column in the data object. This is used to verify whether
        each line in the data is consistent.
    school_name_column: str
        The column that represents the name of the school.

    Returns
    -------
    int:
        The number of schools that the dataset has.
    """
    if school_name_column not in column_names:
        print(f'Error counting schools: column {school_name_column} not found in inputted columns {column_names}.')
        exit(1)

    distinct_schools = set()
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
        
        school = entry[school_name_column]
        distinct_schools.add(school)
    
    return len(distinct_schools)
        

def count_schools_for_each_state(
    data: list[dict[str, any]], column_names: set[str], school_name_column: str, state_column: str
) -> dict[str, int]:
    """This function counts the total amount of schools in each state.

    This function makes assertions on whether the data passed in follows the proper schema. And then it
    gathers all of the distinct schools for each state, specified by the school_name_column and state_column arguments,
    within an auxillary dict named distinct_schools_in_state. The function finally iterates through 
    distinct_schools_in_state, counting the number of distinct schools for each state and saving that information in
    the dict that will be returned.

    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file.
    column_names: set[str]
        A set of strings that is supposed to represent each column in the data object. This is used to verify whether
        each line in the data is consistent.
    school_name_column: str
        The column that represents the name of the school.
    state_column:
        The column that represents the state.
    
    Returns
    -------
    dict[str, int]:
        A dict that maps the state to the number of schools within it.
    """
    if school_name_column not in column_names:
        print(f'Error counting schools for each state: column {school_name_column} not found in inputted columns {column_names}.')
        exit(1)
    
    if state_column not in column_names:
        print(f'Error counting schools: column {state_column} not found in inputted columns {column_names}.')
        exit(1)
    
    distinct_schools_in_state = dict()
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
        
        school = entry[school_name_column]
        state = entry[state_column]
        
        if state not in distinct_schools_in_state:
            distinct_schools_in_state[state] = set()
        distinct_schools_in_state[state].add(school)

    count_schools_in_state = dict()
    for state, schools in distinct_schools_in_state.items():
        count_schools_in_state[state] = len(schools)
    
    return count_schools_in_state


def count_schools_for_each_metro_centric_locale(
    data: list[dict[str, any]], column_names: set[str], school_name_column: str, metro_centric_locale_column: str
) -> dict[str, int]:
    """This function counts the total amount of schools in each Metro-centric locale.

    This function makes assertions on whether the data passed in follows the proper schema. And then it
    gathers all of the distinct schools for each state, specified by the school_name_column and 
    metro_centric_locale_column arguments, within an auxillary dict named distinct_schools_in_metro_locale. The 
    function finally iterates through distinct_schools_in_metro_locale, counting the number of distinct schools for 
    each Metro-centric locale and saving that information in the dict that will be returned.

    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file.
    column_names: set[str]
        A set of strings that is supposed to represent each column in the data object. This is used to verify whether
        each line in the data is consistent.
    school_name_column: str
        The column that represents the name of the school.
    metro_centric_locale_column:
        The column that represents the Metro-centric locale.
    
    Returns
    -------
    dict[str, int]:
        A dict that maps the Metro-centric locale to the number of schools within it.
    """
    if school_name_column not in column_names:
        print(f'Error counting schools for each state: column {school_name_column} not found in inputted columns {column_names}.')
        exit(1)
    
    if metro_centric_locale_column not in column_names:
        print(f'Error counting schools: column {metro_centric_locale_column} not found in inputted columns {column_names}.')
        exit(1)
    
    distinct_schools_in_metro_locale = dict()
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
        
        school = entry[school_name_column]
        metro_centric_locale = entry[metro_centric_locale_column]
        
        if metro_centric_locale not in distinct_schools_in_metro_locale:
            distinct_schools_in_metro_locale[metro_centric_locale] = set()
        distinct_schools_in_metro_locale[metro_centric_locale].add(school)

    count_schools_in_metro_locale = dict()
    for metro_centric_locale, schools in distinct_schools_in_metro_locale.items():
        count_schools_in_metro_locale[metro_centric_locale] = len(schools)
    
    return count_schools_in_metro_locale


def find_city_with_max_schools(
    data: list[dict[str, any]], column_names: set[str], school_name_column: str, city_column: str
) -> tuple[str, int]:
    """This function finds the city with the maximum number of schools.

    This function makes assertions on whether the data passed in follows the proper schema. And then it
    gathers all of the distinct schools for each city, specified by the school_name_column and city_column arguments,
    within an auxillary dict named distinct_schools_in_city. The function finally returns a tuple containing the city 
    with the most distinct schools and the count.

    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file.
    column_names: set[str]
        A set of strings that is supposed to represent each column in the data object. This is used to verify whether
        each line in the data is consistent.
    school_name_column: str
        The column that represents the name of the school.
    city_column:
        The column that represents the city.
    
    Returns
    -------
    tuple[str, int]:
        A tuple with the first entry being a string that represents the city with the most schools and the second entry
        being the number of schools that city has.
    """
    if school_name_column not in column_names:
        print(f'Error counting schools for each state: column {school_name_column} not found in inputted columns {column_names}.')
        exit(1)
    
    if city_column not in column_names:
        print(f'Error counting schools: column {city_column} not found in inputted columns {column_names}.')
        exit(1)
    
    distinct_schools_in_city = dict()
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
        
        school = entry[school_name_column]
        city = entry[city_column]
        
        if city not in distinct_schools_in_city:
            distinct_schools_in_city[city] = set()
        distinct_schools_in_city[city].add(school)

    max_city = max(distinct_schools_in_city, key=lambda city: len(distinct_schools_in_city[city]))
    count_schools_in_max_city = len(distinct_schools_in_city[max_city])
    return (max_city, count_schools_in_max_city)


def count_cities_with_at_least_one_school(
    data: list[dict[str, any]], column_names: set[str], city_column: str
) -> int:
    """This function finds the number of distinct cities with at least one school.

    This function makes assertions on whether the data passed in follows the proper schema. And then it adds a city
    into an auxillary set cities_with_schools for each entry. The function finally returns the length of that set.

    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file.
    column_names: set[str]
        A set of strings that is supposed to represent each column in the data object. This is used to verify whether
        each line in the data is consistent.
    city_column:
        The column that represents the city.
    
    Returns
    -------
    int:
        The number of distinct cities that have at least one school.
    """    
    if city_column not in column_names:
        print(f'Error counting schools: column {city_column} not found in inputted columns {column_names}.')
        exit(1)
    
    cities_with_schools = set()
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
        
        city = entry[city_column]
        cities_with_schools.add(city)

    return len(cities_with_schools)
    

def print_counts() -> None:
    """A method that prints counts for a bunch of different queries in the school_data.csv file.

    This method prints outputs for the following queries:
    1. Total number of schools in the data set.
    2. Total number of schools in each state.
    3. Total number of schools in each Metro-centric locale.
    4. The city with the most schools in it, along with the number of schools in that city.
    5. The number of unique cities that have at least one school in it.
    """
    SCHOOL_NAME_COLUMN = 'SCHNAM05'
    STATE_COLUMN = 'LSTATE05'
    CITY_COLUMN = 'LCITY05'
    METRO_CENTRIC_LOCALE_COLUMN = 'MLOCALE'

    loaded_data, column_names = load_csv("school_data.csv")
    print()

    num_schools = count_schools(
        loaded_data, 
        column_names, 
        SCHOOL_NAME_COLUMN
    )
    num_schools_per_state = count_schools_for_each_state(
        loaded_data, 
        column_names, 
        school_name_column=SCHOOL_NAME_COLUMN, 
        state_column=STATE_COLUMN
    )
    num_schools_per_metro_centric_locale = count_schools_for_each_metro_centric_locale(
        loaded_data, 
        column_names, 
        school_name_column=SCHOOL_NAME_COLUMN, 
        metro_centric_locale_column=METRO_CENTRIC_LOCALE_COLUMN
    )
    max_city, num_schools_in_max_city = find_city_with_max_schools(
        loaded_data, 
        column_names, 
        school_name_column=SCHOOL_NAME_COLUMN, 
        city_column=CITY_COLUMN
    )
    num_cities_with_schools = count_cities_with_at_least_one_school(
        loaded_data, 
        column_names, 
        city_column=CITY_COLUMN
    )

    print(f'Total Schools: {num_schools}')
    print()

    print('Schools by State:')
    for state, count in num_schools_per_state.items():
        print(f'   {state}: {count}')
    print()

    print('Schools by Metro-centric locale:')
    for metro_centric_locale, count in num_schools_per_metro_centric_locale.items():
        print(f'   {metro_centric_locale}: {count}')
    print()

    print(f'City with most schools: {max_city} ({num_schools_in_max_city} schools)')
    print()

    print(f'Unique cities with at least one school: {num_cities_with_schools}')

print_counts()