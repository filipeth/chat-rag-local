# Local Knowledge Base and Chat Interface

Welcome to this project that combines the power of a local vector database, local embeddings, and an open-source local language model to create a knowledge base and chat interface. This project emphasizes the importance of running everything locally, ensuring data privacy and control.

## 🚀 Key Features

1. 📂 **Local Vector Database**: Utilizes Qdrant, a high-performance vector database, to store and retrieve knowledge base data efficiently.
1. 🧠 **Local Language Model**: Leverages Ollama, an open-source language model, for natural language processing tasks such as text generation and question answering.
1. 🌐 **Local Embeddings**: Generates embeddings locally using fastembed, ensuring that your data remains secure and private.
1. 💬 **Chat Interface**: Provides a user-friendly chat interface powered by the Ollama language model and the knowledge base service.
1. 🐳 **Docker Compose**: Simplifies the deployment and management of the project's services using Docker Compose.

## 📁 Folder Structure

The project is organized into the following main folders:

1. `chat_rag`: Contains the Chat RAG (Retrieval-Augmented Generation) service, which provides the chat interface.
1. `knowledge_base`: Houses the Knowledge Base service, responsible for managing the knowledge base data and interacting with the Qdrant vector database.
1. `ollama`: Includes the Ollama language model and its associated data.

## 🛠️ Usage

To get started with this project, follow these simple steps:

Ensure that you have Docker and Docker Compose installed on your system.
Navigate to the project directory.
Run `docker-compose up -d` to start all the services in detached mode.
Access the services through the exposed ports on `localhost`.

### APIs

1. **Knowledge base**
    1. ENV VARIABLES
        - `LLM_API_URL` = "http://ollama:11434/api/chat" ollama url
        - `LLM_MODEL` = "phi3:mini" llm model to generate text
        - `QDRANT_URL` = "http://qdrant:6333" qdrant url
        - `QDRANT_EMBED_MODEL` = "sentence-transformers/all-MiniLM-L6-v2" model used for embedding
        - `QDRANT_SEARCH_LIMIT` = "10" number of itens to fetch from vectordb
        - `SEMANTIC_CHUNKER_TYPE` = "percentile" params for semantic chunking
        - `SEMANTIC_CHUNKER_AMOUNT` = "85" params for semantic chunking

    2. ENDPOINTS
        - `vectorize` http://localhost:8777/v1/vectorize

        ```shell
        curl -X 'POST' \
        'http://localhost:8777/v1/vectorize?collection_name=teste' \
        -H 'accept: application/json' \
        -H 'Content-Type: multipart/form-data' \
        -F 'file=@pagina_web.htm;type=text/html'
        ```

        - `search` http://localhost:8777/v1/search

        ```shell
        curl -X 'GET' \
        'http://localhost:8777/v1/search?query=Qual%20%C3%A9%20o%20principal%20produto%20da%20sua%20empresa%3F&collection_name=teste' \
        -H 'accept: application/json'
        ```

2. **Chat RAG**
    1. ENV VARIABLES
        - `LLM_API_URL` = "http://ollama:11434/api/chat" ollama endpoint
        - `LLM_MODEL` = "phi3:mini" llm model to generate text
        - `SEARCH_LIMIT` = "10" number of itens to fetch from vectordb
        - `SEARCH_API_URL` = "http://knowledge-base:8000/v1/search"
        - `PROMPT` = "DOCUMENTS:\n{DOCUMENTS}\n\nQUESTION:\n{QUESTION}"
        - `SYSTEM_PROMPT` = prompt

    2. ENDPOINTS
        - `chat` http://localhost:8778/v1/chat
        ```shell
        curl -X 'POST' \
        'http://localhost:8778/v1/chat' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "collection_name": "teste",
        "text": "Qual é o principal produto da sua empresa?",
        "stream": false
        }'
        ```

## 🎨 Customization

The project is highly customizable to suit your specific needs:

1. Modify the environment variables in the respective `.env` files (`./knowledge_base/.env` and `./chat_rag/.env`) to configure the Knowledge Base and Chat RAG services.
1. Customize the services or add new ones by modifying the Docker Compose configuration file (docker-compose.yml) and the respective service directories.

## Limitations

1. Only `html` and `.txt` type files are allowed for now. In the future will be added support to other types of documents such as `.pdf` and `.doc`, and also websites.
2. Not support for evaluations, metrics and tracing for now. Those are super important features that must be implemented in the near future.
