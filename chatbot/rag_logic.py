import os
from django.conf import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# --- Global Variables & Caching ---
# Simple in-memory cache for the vector store to avoid rebuilding it on every request in a dev environment.
# For production, a more robust caching mechanism like Redis would be better.
_vector_store_cache = None

def get_text_content():
    """
    Loads the biography text from the file.
    """
    try:
        file_path = os.path.join(settings.BASE_DIR, 'chatbot', 'data', 'biography.txt')
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: biography.txt not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def build_vector_store(text_content, api_key):
    """
    Builds or retrieves the FAISS vector store from raw text content.
    """
    global _vector_store_cache
    if _vector_store_cache:
        return _vector_store_cache

    if not text_content:
        return None

    try:
        # 1. Create a Document object
        docs = [Document(page_content=text_content, metadata={"source": "biography"})]

        # 2. Split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # 3. Create Embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )

        # 4. Build and cache Index
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        _vector_store_cache = vectorstore
        return vectorstore

    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def get_rag_chain(vectorstore, api_key):
    """
    Creates the RAG chain for question answering.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            google_api_key=api_key,
            convert_system_message_to_human=True
        )

        system_prompt = (
            "You are an AI assistant representing the person described in the context. "
            "Answer questions as if you are that person, using the first person ('I', 'my', 'me'). "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not in the context, say you don't have information on that based on the biography. "
            "Keep your answers concise and conversational. "
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        retriever = vectorstore.as_retriever()
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        return rag_chain
    except Exception as e:
        print(f"Error creating RAG chain: {e}")
        return None
