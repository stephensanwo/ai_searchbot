# AI SearchBot Demo

A Fullstack Demo Application that ingests data from csv, pdf files and implements a chat user interface for users to query/search data with AI.

Built with:
- FastAPI
- Python
- HTML
- JavaScript
- CSS
- Langchain
- Pinecone
- OpenAI

### How to Run

- Create a free pinecone index named `doctest-index` [here](https://www.pinecone.io)
- Configure environment variables in .env file in app root:

    ```bash
    export ENVIRONMENT = <local>
    export VERSION = <version>
    export OPENAI_API_KEY = <openapi-key>
    export PINECONE_API_KEY = <pinecone-api-key>
    export PINECONE_API_ENV = <pinecone-api-env>
    ```
- Load Model
    `python model.py` or make `load_model`

- Load Web App
    `uvicorn main:app --reload`