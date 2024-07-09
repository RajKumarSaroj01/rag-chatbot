
import read_file
import db_store
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents=read_file.data_ingestion()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
docs=text_splitter.split_documents(documents)
 
db_store.set_vector_store(docs)

result=db_store.vectorstore_faiss.search("add query text here",search_type ="similarity")
print(result)