# school-db-search
Here you will find more information on what this project entails and how to execute the code.

Both programs load data from a file named `school_data.csv`. I performed testing with the `Year 2005-2006 (v.lb), States A-I, ZIP (769 KB) CSV File` dataset, found on this [page](https://nces.ed.gov/ccd/CCDLocaleCode.asp).

## Prerequisites
Before you begin, please ensure you have Python 3 installed. Installation instructions can be found on this [page](https://www.python.org/downloads/).

## `count_schools.py`
This program loads the aforementioned dataset and performs the below series of queries:
- Total number of schools in the data set.
- Number of schools for each state.
- Number of schools for each Metro-centric locale.
- City with the most schools in it, along with the amount.
- Number of unique cities with at least one school.

### How to run this?
In order to run this program, ensure that you are within the `school-db-search` directory and run the following in the command prompt:
```
python3 count_schools.py
```

## `school_search.py`
This program loads the aforementioned dataset and allows users to look up schools on the data set. Based on a ranking algorithm that takes into account the school name, city, and state; it outputs the top three search results. 

### Tokenization
After loading the data set, the program uses the `batch_tokenize` function to tokenize each entry's school name, city, and state. For each of these entities (i.e. school name, city, and state), the tokenization function `tokenize` removes punctuation and stop words, as indicated by the constants `PUNCTUATION` and `STOP_WORDS` respectively, returning a list of tokens. These constants can be fine-tuned if we wish to improve the search accuracy.

Each entry becomes associated with a dict that stores three tokenized lists, one representing the school name, another representing the school's city, and the final one representing the school's state.

`tokenize` is called again to tokenize the query string, using the `STATE_ABBREVIATIONS` constant to perform the added operation of converting full state names (e.g. California) into state abbreviations (e.g. CA). This is to mimic what is being stored in the data set. It allows the user to query by the full name of the state if they choose to.

### Ranking
The ranking function `compute_rank` takes in the tokenized entries and query, and computes four values:
- `exact_match`: 1 if all of the tokens in the query are contained by the school name, city, and state; and 0 otherwise.
- `partial_match`: the ratio of all the tokens in the query that are contained by the school name, city, and state; over the total number of tokens in the query.
- `city_match`: the ratio of all the tokens in the query that are contained by the school's city; over the total number of tokens in the query.
- `state_match`: the ratio of all the tokens in the query that are contained by the school's state; over the total number of tokens in the query.

It then outputs a linear combination of those values, using weights defined by the following constants:
- `EXACT_MATCH_WEIGHT`
- `PARTIAL_MATCH_WEIGHT`
- `CITY_MATCH_WEIGHT`
- `STATE_MATCH_WEIGHT`

These variables can also be fine-tuned if enhanced accuracy for a particular data set is desired.

### Output
The `search_schools` function uses `compute_rank` to compute the ranks for each entry, outputting the three entries with the highest ranks in descending order.

### How to run this?
In order to run this program, again ensure that you are within the `school-db-search` directory and run the following in the command prompt:
```
python3 school_search.py
```

You will be asked whether you wish to supply your own queries or use queries built in this program. Please select by specifying `Y` or `N` and confirming with the `Enter` or `Return` key.
```
Please specify here if you wish to supply your own queries (Y) or use the built-in queries here (N).
> N
```

If you wish to supply your own queries, you will be prompted for one. After confirming your query by pressing `Enter` or `Return`, the program will output the top three search results.
```
Please specify here if you wish to supply your own queries (Y) or use the built-in queries here (N).
> Y
Please specify your query here
> elementary school highland park
Results for: "elementary school highland park" (search took: 0.058s)
1. HIGHLAND PARK ELEMENTARY SCHOOL
   PUEBLO, CO
2. HIGHLAND PARK ELEMENTARY SCHOOL
   MUSCLE SHOALS, AL
3. HIGHLAND PARK HIGH SCHOOL
   HIGHLAND PARK, IL
Would you like to continue (Y/N)?
>
```

As indicated above, you will be asked if you wish to continue supplying queries. Typing `Y` and `Enter` or `Return` afterwards will allow you to supply yet another query, while typing `N` instead will exit the program gracefully.