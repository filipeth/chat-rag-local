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

## 🎨 Customization

The project is highly customizable to suit your specific needs:

1. Modify the environment variables in the respective `.env` files (`./knowledge_base/.env` and `./chat_rag/.env`) to configure the Knowledge Base and Chat RAG services.
1. Customize the services or add new ones by modifying the Docker Compose configuration file (docker-compose.yml) and the respective service directories.
