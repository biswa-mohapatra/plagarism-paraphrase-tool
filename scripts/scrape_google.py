"""
Scrape Google package is a package that scrapes google search
results like links, title and snippet content.

Author : Biswajit Mohapatra, Munj Bhavesh Patel

Copyright : iamneo.ai
"""


from apiclient.discovery import build
from jsonpath_ng import jsonpath, parse
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from scripts.utils.common import read_yaml
from application_logger.logging import App_Logger


class scrape_google(object):
    """
    This class is responsible for performing all the necessary
    operations that are necessary to scrape google links
    descriptions and titles for a given searching query.

    Params: questions : array of questions
            transformed data : pd.DataFrame
    Returns: details of the duplicate questions : pd.DataFrame
    Exceptions:
    Author: Biswajit Mohapatra, Munj Bhavesh Patel
    """

    def __init__(self,query:str):
        self.meta_data = read_yaml("meta-data/config.yaml")
        self.file_object = open("logs/scrape_google.txt","a+")
        self.logging = App_Logger(self.file_object)
        self.query = query

    def get_source(self)->list:
        """Return the source code for the provided URL. 

        Params: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        
        Author: Biswajit Mohapatra
        """

        try:
            # invoking the custom search engine
            self.logging.log(f"Getting the source content for the search querry started.")
            resource = build(self.meta_data["META-DATA"]["search_type"],
                            self.meta_data["META-DATA"]["version"],
                            developerKey=self.meta_data["META-DATA"]["api_key"]).cse()
            self.logging.log(f"Resource built successfuly!")
            if not self.query == None:
                self.logging.log(f"Starting the searching operation.")
                # returning list of search results.
                return [resource.list(q=self.query,cx=self.meta_data["META-DATA"]["search_id"],start=i).execute() for i in range(1,20,10)]
            else:
                self.logging.log(f"Search query is empty!")
                raise TypeError("Empty query can't be searched!")
        except TypeError:
            self.logging.log(f"Something went wrong in searching reasults.\nError Message: {TypeError}")
            raise TypeError
        except Exception as e:
            self.logging.log(f"Something went wrong in searching reasults.\nError Message: {e}")
            raise Exception
        
    def search_result(self)->dict:
        """
        This method is responsible for preparing the searched data into
        a dictonary format where link being key and snippent being value.

        Params: None

        Returns: result->dict

        Author: Biswajit Mohapatra, Munj Bhavesh Patel
        """
        try:
            # getting the search results using get source method
            self.logging.log(f"Started creating the search results.")
            result = {}
            items = self.get_source()

            #accessing the link and snippent in a dict format
            if not items == None:
                self.logging.log(f"Preparing the result!")
                for i in range(len(items)):
                    for j in range(len(items[i])):
                        result[items[i]["items"][j]["link"]] = items[i]["items"][j]["snippet"]
                
                self.logging.log(f"Prepared the result!")
                return result

            else:
                self.logging.log(f"Get source method returned None value.")
                raise TypeError("Empty items can't be processes!")
        except TypeError:
            self.logging.log(f"Something went wrong in preparing reasults.\nError Message: {TypeError}")
            raise TypeError
        except Exception as e:
            self.logging.log(f"Something went wrong in preparing reasults.\nError Message: {e}")
            raise Exception