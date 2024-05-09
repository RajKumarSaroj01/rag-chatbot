# import all required packages 
import os
import boto3
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain

from langchain_community.embeddings import BedrockEmbeddings
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.document_loaders import PyPDFLoader 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import FAISS


# embeddings 
bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddins=BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", region_name='us-east-1')

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

    print("Total number of loaded files ",len(documents),sep=" ----- ")        
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    docs=text_splitter.split_documents(documents)
    return docs

def get_vector_store(docs):
    global vectorstore_faiss
    if len(docs)==0:
        print("Please put some file in knowledge-base folder")
    vectorstore_faiss=FAISS.from_documents(docs,bedrock_embeddins)
    vectorstore_faiss.save_local("knowledge-base-faiss-index")

def call_ingestion():
    docs=data_ingestion()
    get_vector_store(docs)

call_ingestion()    
# function to invoke model 
llm_data=Bedrock(
        credentials_profile_name='default',
        model_id='meta.llama2-70b-chat-v1',
        model_kwargs={ 
        "temperature": 0.9,
        "top_p": 0.5,
        "max_gen_len": 512}, region_name='us-east-1')

def demo_memory():
    memory=ConversationBufferMemory(llm=llm_data,memory_key="chat_history",output_key="answer")
    return memory

# create fun for conversation chain which is input + memory
def demo_conversation(input_txt,memory):
    chain = ConversationalRetrievalChain.from_llm(llm_data, 
                                                  retriever=
                                                  vectorstore_faiss.as_retriever(search_kwargs={"k": 3}),
                                                  get_chat_history=lambda h : h,
                                                  return_source_documents=False,memory=memory)
    result =chain({"question":input_txt})
    return result["answer"]

    


