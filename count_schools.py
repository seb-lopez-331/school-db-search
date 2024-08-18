import csv, time, itertools
"""
Here is a layout of the records stored in school_data.csv

Variable    Start       End         Field    Data 
Name        Position    Position    Length   Type    Description      
NCESSCH      01         12          12       AN      ID assigned by NCES to each school. 
LEAID        13         19           7       AN      Unique Agency ID (NCES assigned) 
LEANM05      20         79          60       AN      Name of Operating Agency 
SCHNAM05     80         129         50       AN      School Name 
LCITY05     130         159         30       AN      Location City Name 
LSTATE05    160         161          2       AN      Location USPS State Abbreviation 
LATCOD      162         170          9        N      Latitude 
LONCOD      171         181         11        N      Longitude 
MLOCALE     182         182          1       AN      Metro-centric locale code:
ULOCALE     183         184          2       AN      Urban-centric locale code:
STATUS05    185         185          1       AN      NCES code for the school status 


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

def load_csv(filename: str, encoding: str = 'Windows-1252') -> tuple[list[dict[str[any]]], set[str]]:
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
    (list[dict[str, any]], set[str])
        A tuple that contains a list of dicts that represent each row, and a set with strings that represent the names
        of each column.
    """
    loaded_data = []

    try:
        with open(filename, mode='r', encoding=encoding) as file:
            csv_reader = csv.reader(file)
            print(f'File {filename} opened successfully')

            # Gather a list with the column names
            schema = next(csv_reader)
            
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
                    for j, name in enumerate(schema):
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
    
    return loaded_data, set(schema)


def count_schools(data: list[dict[str, any]], schema: set[str]) -> int:
    """This function will count the total schools in the provided loaded data.

    Firstly, this function makes assertions on whether the data passed in follows the proper schema. And then it
    computes the number of distinct entries for the SCHNAM05 column.
    
    Parameters
    ----------
    data: list[dict]
        A list of dicts that is supposed to represent each row in the school_data.csv file

    Returns
    -------
    int:
        The number of schools that the dataset has.
    """
    

    


loaded_data = load_csv("school_data.csv")