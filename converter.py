from pathlib import Path
import pymupdf
import streamlit as st
import requests
from bs4 import BeautifulSoup

def text_converter(type:str , file , url):
    if type == "pdf":
        save_folder = "./converted_text"
        save_path = Path(save_folder, file.name)
        with open(save_path,"wb") as w:
            w.write(file.getvalue())
        
        # if save_path.exists():
        #     st.success(f'File {file.name} is successfully saved!')

        extracted_text = ""
        doc = pymupdf.open(f"./converted_text/{file.name}") # open a document
        for page in doc: # iterate the document pages
            extracted_text += page.get_text() # get plain text encoded as UTF-8

    elif type=='url':
        reqs = requests.get(f"{url}")
    # # req = requests.Session()
    # # req.get(f"{url}")
    # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')

    # Extract all the text from the webpage
        extracted_text = soup.get_text(separator='\n')

        print(extracted_text)
    return extracted_text
