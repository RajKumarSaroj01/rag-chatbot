
import os
from langchain_community.document_loaders import PyPDFLoader 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader

def data_ingestion():
    documents=[]
    for file in os.listdir("knowledge-base"):
        if file.endswith(".pdf"):
            loader=PyPDFLoader("./knowledge-base/"+file)
            documents.extend(loader.load())
            print("Loaded ",file,sep=" -------------- ")
        elif file.endswith(".docx") or file.endswith(".doc"): 
            loader=Docx2txtLoader("./knowledge-base/"+file)
            documents.extend(loader.load())
            print("Loaded ",file,sep=" -------------- ")
        elif file.endswith(".txt"):
            loader=TextLoader("./knowledge-base/"+file)
            documents.extend(loader.load())
            print("Loaded ",file,sep=" -------------- ")       

    print("Total number of loaded pages ",len(documents),sep=" ----- ")        
    return documents