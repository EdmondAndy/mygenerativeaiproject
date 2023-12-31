import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

from dotenv import load_dotenv
load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


def ingest_docs() -> None:
    loader = ReadTheDocsLoader(path="ndis-docs/www.aat.gov.au/summaries-of-decisions")
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents) }documents")
    #text_splitter = RecursiveCharacterTextSplitter(
    #    chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    #)
    #documents = text_splitter.split_documents(documents=raw_documents)
    #print(f"Splitted into {len(documents)} chunks")

    for doc in raw_documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("ndis-docs", "https:/")
        new_url = new_url.removesuffix('.html')
        doc.metadata.update({"source": new_url})

    print(f"Going to insert {len(raw_documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(raw_documents, embeddings, index_name="langchain-doc-index")
    print("****** Added to Pinecone vectorstore vectors")


if __name__ == "__main__":
    ingest_docs()
