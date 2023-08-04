from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()


def query_vector_db(query: str):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )

    index_name = "doctest-index"

    docsearch = Pinecone.from_existing_index(index_name, embeddings)

    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")

    docs = docsearch.similarity_search(query)

    res = chain.run(input_documents=docs, question=query)
    return res
