# Imorting all the libraries:

from application_logger.logging import App_Logger
import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

file_object = open("logs/paraphrase.txt","a+")
logger = App_Logger(file_object)

def rephrase(sentence:str,tokenizer,model,num_outputs:int)->list:
    """
    """
    try:

        # mentioning query structure for tokenizing.
        logger.log(f"Starting rephrase module...")
        text =  "paraphrase: " + sentence + " </s>"

        # Selecting the system device.
        logger.log(f"Device : {torch.device}\nCuda Available : {torch.cuda.is_available()}")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # Encoding the query:
        logger.log(f"Starting encoding on the available device.")
        encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")

        # setting the query to device processor.
        input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

        # setting the model to the device.
        model.to(device)
        logger.log(f"Fitting model to the available device : {torch.device}")
        logger.log(f"Generating {num_outputs} outputs.")

        # generating outputs
        outputs = model.generate(
                                    input_ids=input_ids, attention_mask=attention_masks,
                                    max_length=256,
                                    do_sample=True,
                                    top_k=120,
                                    top_p=0.95,
                                    early_stopping=True,
                                    num_return_sequences=num_outputs,
                                )

        collections = []

        # collecting all the generated outputs:
        for output in outputs:
            line = tokenizer.decode(output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
            collections.append(line)
        logger.log(f"Rephrasing completed with {num_outputs} outputs.")
        return list(set(collections))

    except TypeError as te:
        logger.log(f"Something went wrong in rephrasing the text.\nError Message:{te}") 
        raise TypeError
    except Exception as e:
        logger.log(f"Something went wrong in rephrasing the text.\nError Message:{e}") 
        raise e