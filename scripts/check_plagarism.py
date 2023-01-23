#importing all the libraries!

from thefuzz import fuzz
from scripts.scrape_google import scrape_google
from application_logger.logging import App_Logger

file_object = open("logs/check_plagarism.txt","a+")
logger = App_Logger(file_object)

def check_similarity(query:str)->list:
    """
    This is a custom function to check the similarity of two given
    text based on the fuzzy search algorithm.

    Parameters: query->string object

    Returns: link with match percentage->list object

    Author: Biswajit Mohapatra
    """
    try:
        # Getting the google search scrape results.
        logger.log(f"Checking for similarity started!")
        sc_obj = scrape_google(query)
        matches = {}
        logger.log(f"Fetching the search result.")
        result = sc_obj.search_result()
        logger.log(f"Search result fetched successfully! Finding the matches.")

        # finding the match ratio based on the fuzzy search!
        for key in result.keys():
            q2 = result[key].replace("\xa0...","")
            set_ratio = fuzz.token_set_ratio(query,q2)
            matches[set_ratio] = key
        
        # sorting the collection in descending order of the match percentage.
        logger.log(f"{len(list(matches.keys()))}Matches found, sorting them.")
        idx = list(matches.keys())
        idx.sort(reverse=True)
        logger.log(f"Matches sorted.")
        output = {}
        for i in idx:
            output[matches[i]] = i
        # [(matches[i],i) for i in idx]
        return output
    except TypeError:
        logger.log(f"Something went wrong in checking similarity.\nError Message: {TypeError}")
        raise TypeError
    except Exception:
        logger.log(f"Something went wrong in checking similarity.\nError Message: {Exception}")
        raise Exception  