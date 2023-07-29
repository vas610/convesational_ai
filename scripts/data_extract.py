import os
import glob
from langchain.document_loaders import BSHTMLLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings


# Step1: Define a sentence transformer model that will be used 
#        to convert the documents into vector embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2")

# Step2: Create a list of html contents from the documents
html_docs = []
for _docs in ["lambda", "sagemaker"]:
    path_to_dir = f"./aws_docs/{_docs}/"
    html_files = glob.glob(os.path.join(path_to_dir, "*.html"))
    for _file in html_files:
        with open(_file) as f:
            loader = BSHTMLLoader(_file)
            data = loader.load()
            html_docs.extend(data)
    # Step3: Create & save a vector database with the vector embeddings
    #        of the documents
    db = FAISS.from_documents(html_docs, embeddings)
    db.save_local(f"faiss_index_{_docs}")
