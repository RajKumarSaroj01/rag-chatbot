
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import secure_credentials

def set_vector_store(docs):
    global vectorstore_faiss
    if len(docs)==0:
        print("Please put some file in knowledge-base folder")
    vectorstore_faiss=FAISS.from_documents(docs,OpenAIEmbeddings(api_key=secure_credentials.OPENAI_API_KEY))
    vectorstore_faiss.save_local("knowledge-base-faiss-index")
