from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
import logging
import json
from pathlib import Path
import numpy as np
import openai
from typing import List
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (ensure this is called early in the script)
load_dotenv()

# Configuration
# Read the API key from your specified environment variable
chatllm_api_key = os.getenv("CHATLLM_API_KEY")

# Set the standard OPENAI_API_KEY environment variable expected by the OpenAI library.
# This ensures the OpenAI client automatically picks it up without needing to pass it as a parameter.
if chatllm_api_key:
    os.environ["OPENAI_API_KEY"] = chatllm_api_key
    logger.info("OPENAI_API_KEY set from CHATLLM_API_KEY for client initialization.")
else:
    logger.error("CHATLLM_API_KEY not found in .env or environment variables. OpenAI API calls will likely fail.")

# Initialize the OpenAI client. It will now automatically pick up the API key
# from the OPENAI_API_KEY environment variable we just set.
client = openai.OpenAI()

# Check if the API key was loaded
if not chatllm_api_key:
    logger.error("OpenAI API key (CHATLLM_API_KEY) not configured.")
    # Depending on how critical this is at startup, you might exit or raise an error
    # For now, we'll just log and let subsequent API calls fail clearly.
    # A better approach might be to raise an exception immediately if key is required.
    # raise ValueError("OpenAI API key (CHATLLM_API_KEY) not found in environment variables.")

# API Configuration
API_CONFIG = {
    "base_url": os.getenv("CHATLLM_API_URL", "https://api.abacus.ai"),
    "model": os.getenv("CHATLLM_MODEL", "gpt-3.5-turbo"),
    "temperature": float(os.getenv("CHATLLM_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("CHATLLM_MAX_TOKENS", "1000"))
}

app = FastAPI(
    title="Search API",
    description="API for AI-powered search functionality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For debugging; change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory document and embedding store
DOCUMENTS: List[str] = []
EMBEDDINGS = None  # Will be a numpy array

class SearchQuery(BaseModel):
    query: str

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to the Search API",
            "status": "active",
            "endpoints": {
                "search": "/api/search",
                "upload": "/api/upload",
                "docs": "/docs"
            },
            "system_state": {
                "documents_indexed": len(DOCUMENTS),
                "embeddings_available": EMBEDDINGS is not None
            },
            "config": {
                "model": API_CONFIG["model"],
                "temperature": API_CONFIG["temperature"],
                "max_tokens": API_CONFIG["max_tokens"]
            }
        }
    )

@app.post("/api/search")
async def search(query: SearchQuery):
    try:
        logger.info(f"Received search query: {query.query}")
        logger.info(f"Current state - Number of documents: {len(DOCUMENTS)}, Embeddings shape: {EMBEDDINGS.shape if EMBEDDINGS is not None else None}")
        
        if not query.query.strip():
            logger.error("Empty query received")
            raise HTTPException(
                status_code=400,
                detail="Search query cannot be empty"
            )

        # --- RAG: Embed query and retrieve top docs ---
        if EMBEDDINGS is None or len(DOCUMENTS) == 0:
            error_msg = "No documents indexed for retrieval. Please upload documents first."
            logger.error(error_msg)
            raise HTTPException(
                status_code=400,
                detail=error_msg
            )
        
        # Get query embedding
        logger.info("Getting query embedding...")
        try:
            query_emb = await get_embedding(query.query)
            query_emb = query_emb.reshape(1, -1)
            logger.info(f"Query embedding shape: {query_emb.shape}")
        except Exception as e:
            logger.error(f"Failed to get query embedding: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get query embedding: {str(e)}"
            )
        
        # Calculate similarities
        logger.info("Calculating similarities...")
        try:
            similarities = cosine_similarity(query_emb, EMBEDDINGS)[0]
            logger.info(f"Similarities shape: {similarities.shape}")
        except Exception as e:
            logger.error(f"Failed to calculate similarities: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to calculate similarities: {str(e)}"
            )
        
        # Get top 3 most similar documents
        top_k = min(3, len(DOCUMENTS))
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        retrieved_docs = [DOCUMENTS[i] for i in top_indices]
        context = "\n---\n".join(retrieved_docs)
        logger.info(f"Retrieved {len(retrieved_docs)} documents")

        # --- Pass context + query to OpenAI ---
        system_prompt = (
            "You are a helpful assistant. Use the following context to answer the user's question. "
            "If the answer is not in the context, say you don't know.\n\nContext:\n" + context
        )
        
        try:
            response = client.chat.completions.create(
                model=API_CONFIG["model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query.query}
                ],
                temperature=API_CONFIG["temperature"],
                max_tokens=API_CONFIG["max_tokens"]
            )
            logger.info(f"Response received from OpenAI")
            
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
            else:
                logger.error("No valid response received from API")
                content = "No valid response received from API"
                
        except Exception as e:
            logger.error(f"Failed to process OpenAI response: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process OpenAI response: {str(e)}"
            )

        return {
            "choices": [
                {
                    "message": {
                        "content": content
                    }
                }
            ],
            "retrieved_docs": retrieved_docs
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to OpenAI API: {str(e)}"
        )

@app.options("/api/search")
async def options_search(request: Request):
    return JSONResponse(status_code=200)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_detail = exc.detail if exc.detail else "An unexpected error occurred"
    logger.error(f"HTTP Exception: {error_detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": error_detail}
    )

async def get_embedding(text: str) -> np.ndarray:
    """Get embedding for text using OpenAI's API."""
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        logger.error(f"OpenAI embedding error: {str(e)}")
        raise

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and create embeddings."""
    # Declare these global variables to be modified within this function
    global DOCUMENTS, EMBEDDINGS 
    try:
        # Read file content
        content = await file.read()
        content = content.decode()
        logger.info(f"Successfully read file: {file.filename}")
        
        # Get embedding
        try:
            embedding = await get_embedding(content)
            logger.info(f"Successfully created embedding for file: {file.filename}")
        except Exception as embed_err:
            logger.error(f"OpenAI embedding error: {str(embed_err)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create embedding: {str(embed_err)}"
            )
        
        # Store document and embedding
        DOCUMENTS.append(content)
        if EMBEDDINGS is None:
            EMBEDDINGS = embedding.reshape(1, -1)
        else:
            EMBEDDINGS = np.vstack([EMBEDDINGS, embedding])
        
        logger.info(f"Successfully stored document and embedding. Total documents: {len(DOCUMENTS)}")
        return {"message": "Document uploaded and embedded successfully"}
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        # Ensure traceback module is imported for logging full tracebacks
        import traceback 
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 