# importing all the libraries:
from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
from application_logger import logging
import torch
import os
import sys
from src.utils import common
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from src.plagarism_paraphrase.paraphrase import rephrase
from src.plagarism_paraphrase import check_plagarism
import json

app = Flask(__name__)

# Reading program details
# with open("details.txt","r") as f:
#         prompt = f.read()

# file object for the logs.
file_obj = open("MAIN.txt","a+")
log = logging.App_Logger(file_obj)

@app.route("/")
@cross_origin()
def home(message=None):
    """
    This function is responsible for rendering the home page.
    """
#     sys.stdout.write(prompt)
    if message == None:
        return f"<h2>Welcome to plagarism checker.</h2>"
    else:
        return message

@app.route("/query", methods = ["GET"])
@cross_origin()
def get_params():
        try:
                if request.method == "GET":
                        global query 
                        args = request.args
                        query = args.get("text")
                        return home(message=f"<h3>Recieved!</h3>")
                else:
                        return home(message=f"<h3>Error while receiving query.\
                                Check logs for more details!</h3>")
        except ConnectionAbortedError as ca:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {ca}")
                return f"{ca}"

        except ConnectionError as ce:
                log.log(f"Something went wrong: {ce}")
                return f"{ce}"
        
        except Exception as e:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {e}")
                return f"{e}"
        

@app.route("/checkPlagarism", methods = ["POST","GET"])
@cross_origin()
def main():
    """
    This is the main function to implement the pipeline for all the 
    methods/steps we follow for the plagarism checker.
    """
    try:
        if request.method == "POST" or request.method == "GET":

                log.log(f"Recieved Query!")

                # check plagarism
                final_data = check_plagarism.check_similarity(query)
                log.log(f"Final data for the query is recieved!")

                # saving the json output.
                # with open("result.json", "w") as final:
                #         json.dump(final_data, final, indent=4)
                # log.log(f"Final data for the query is saved as json.")
                #return render_template("home.html",matches=final_data)
                #return f"{final_data}"
                return json.dumps(dict(final_data))
                
        else:
                log.log(f"Request Method is not POST.")
                return home()  
    except ConnectionAbortedError as ca:
                log.log(f"Something went wrong while chceking plagarism!\nError Message: {ca}")
                return f"{ca.errno}"
    except ConnectionError as ce:
        log.log(f"Something went wrong while chceking plagarism!\nError Message: {ce}")
        return f"{ce.errno}"
    except OSError as os:
        log.log(f"Something went wrong while chceking plagarism!\nError Message: {os}")
        return f"{os.errno}"
    except Exception as e:
        log.log(f"Something went wrong while chceking plagarism!\nError Message: {e}")
        return f"{e.args}"

@app.route("/paraphrase", methods = ["POST","GET"])
@cross_origin()
def paraphrase():
        """
        This is a custom defination for performing rephrasing.
        """
        try:
                if request.method == "POST" or request.method == "GET":
                        log.log(f"Starting paraphrasing!")

                        # reading all the meta-data related to the model:
                        model_configs = common.read_yaml("meta-data/config.yaml")
                        log.log(f"Collected the model configurations!")
                        tokens = model_configs["PARAPHRASE"]["tokens"]
                        model_path = model_configs["PARAPHRASE"]["model_path"]
                        num_outputs = model_configs["PARAPHRASE"]["num_outputs"]
                        
                        # downloading the tokens:
                        log.log(f"Loading the saved model.")
                        tokenizer = AutoTokenizer.from_pretrained(tokens)

                        #loading the model
                        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
                        log.log(f"Starting the paraphrasing process...")

                        # rephrasing the given query
                        paraphrased = rephrase(query,
                                                tokenizer,model,
                                                num_outputs=num_outputs)
                        log.log(f"Paraphrasing process completed...")
                        #return render_template("home.html",paraphrased=paraphrased)
                        #return f"{paraphrased}"
                        return json.dumps(dict(paraphrased))
                else:
                        log.log(f"Paraphrasing process did not complete due to inadequate response method hence\nreturning home page...")
                        return home()
        except ConnectionAbortedError as ca:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {ca}")
                return f"{ca}"
        except ConnectionError as ce:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {ce}")
                return f"{ce}"
        except OSError as os:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {os}")
                return f"{os}"
        except Exception as e:
                log.log(f"Something went wrong while paraphrasing!\nError Message: {e}")
                return f"{e}"
        

@app.route("/clearLogs", methods = ["GET", "POST"])
@cross_origin()
def clear_logs():
        try:
                log.log(f"Deleting all the logs.")
                delete_main = request.args.get("delete_main")
                log_files = os.listdir("logs/")
                for file in log_files:
                        if os.path.getsize(f"logs/{file}")/1e+6 >= 2.0:
                                with open(f"logs/{file}","w") as f:
                                        pass
                                log.log(f"Cleared old log of size {os.path.getsize(f'logs/{file}')/1e+6}MB from logs.")
                
                if delete_main == "True":
                        if os.path.getsize(f"MAIN.txt")/1e+6 >= 2.0:
                                with open("MAIN.txt","w") as f:
                                        pass
                                log.log(f"Deleted the main log of size {os.path.getsize(f'MAIN.txt')/1e+6} file.")
                return "<h3>All the logs are cleared.</h3>"
        except UnboundLocalError:
                raise UnboundLocalError("UnboundLocalError: Assignemnt before declaration.")
        except OSError:
                raise OSError("OS Error while deleting logs.")
        except Exception as e:
                raise Exception("Exception while deleting log files.")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000) 