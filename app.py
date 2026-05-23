import streamlit as st
from langchain_groq import ChatGroq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.chains import RetrievalQA
import os
import tempfile

# 1. Setup Your Groq API Key



# 2. Configure the Embeddings Model
# This model translates text into numbers (vectors)
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3. Process the PDF
def process_pdf(uploaded_file):
    # Save the uploaded file temporarily so PyPDF can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    # Load the PDF
    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    # Split the document into chunks (1000 characters each, 200 character overlap)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # Delete the temporary file
    os.remove(temp_path)
    
    return chunks

# 4. Create the FAISS Vector Database
def create_vector_db(chunks):
    embeddings = get_embeddings()
    # Create the database in memory
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# 5. Setup the LLM (Using Meta's Llama 3.1 via Groq for lightning speed)
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

# 6. Build the Streamlit Web UI
st.set_page_config(page_title="Enterprise RAG Engine", page_icon="📚", layout="centered")
st.title("📚 Enterprise Document Q&A Engine")
st.write("Upload any PDF and ask questions about its content. Powered by LangChain, FAISS Vector DB, and Mistral-7B.")

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    st.info("The document is chunked, embedded, and stored locally in a FAISS vector database.")

# 7. Core Application Logic
if uploaded_file is not None:
    with st.spinner("Processing document and building vector database..."):
        # We use session_state so it doesn't rebuild the database every time you type a letter
        if "vector_store" not in st.session_state:
            chunks = process_pdf(uploaded_file)
            st.session_state.vector_store = create_vector_db(chunks)
            st.success("Database built successfully!")
    
    # QA Input Box
    st.divider()
    question = st.text_input("Ask a question based on the uploaded document:")
    
    if question:
        with st.spinner("Searching database and generating answer..."):
            # Setup the retriever to find the top 3 most relevant chunks
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
            llm = get_llm()
            
            # Create the LangChain RetrievalQA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever
            )
            
            # Generate the final response
            response = qa_chain.invoke(question)
            
            # Display Results
            st.subheader("Answer:")
            st.info(response["result"])
else:
    st.warning("👈 Please upload a PDF document in the sidebar to get started.")