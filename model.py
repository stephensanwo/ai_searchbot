from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

loader = CSVLoader(file_path='__mock__/captured_texts.csv')

data = loader.load()

# Chunk your data up into smaller documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)
print(f'Now you have {len(texts)} documents')


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)

print("Pinecone Initialized")
index_name = "doctest-index"

docsearch = Pinecone.from_texts(
    [t.page_content for t in texts], embeddings, index_name=index_name)

docsearch = Pinecone.from_existing_index(index_name, embeddings)
# Query those docs to get your answer back

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

#  Test Query
query = "What are the top 2 one-bedroom properties below $200?"
docs = docsearch.similarity_search(query)

res = chain.run(input_documents=docs, question=query)
print(res)
