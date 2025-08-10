# Search-Frontend: RAG-powered Document Search

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to upload documents and then search through them using natural language queries. The system leverages OpenAI's powerful language models to understand queries, retrieve relevant document snippets, and generate concise answers based on the retrieved context.

## Features

*   **Document Upload:** Asynchronously upload text documents to the backend.
*   **Vector Embeddings:** Documents are processed to generate vector embeddings using OpenAI's `text-embedding-ada-002` model.
*   **Semantic Search (RAG):**
    *   User queries are embedded.
    *   Cosine similarity is used to find the most relevant document snippets from the uploaded collection.
    *   The retrieved context and the user's query are sent to a Large Language Model (LLM) (e.g., GPT-3.5 Turbo) to generate an accurate and contextualized answer.
*   **FastAPI Backend:** A robust and efficient Python backend built with FastAPI.
*   **React Frontend:** A user-friendly React application for interacting with the backend.
*   **Detailed Logging & Error Handling:** Enhanced logging to aid in debugging and clearer error messages for better user experience.

## Tech Stack

**Backend:**
*   **Python 3.x**
*   **FastAPI:** Web framework for building APIs.
*   **Uvicorn:** ASGI server to run FastAPI.
*   **OpenAI Python Library:** For generating embeddings and LLM completions.
*   **NumPy:** For numerical operations on embeddings.
*   **python-dotenv:** For managing environment variables.
*   **httpx:** Underlying HTTP client for OpenAI.

**Frontend:**
*   **React.js:** JavaScript library for building user interfaces.
*   **Fetch API:** For making HTTP requests to the backend.

## Installation

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the `backend` directory with the following variables:
   ```env
   CHATLLM_API_KEY=your_openai_api_key
   CHATLLM_API_URL=https://api.openai.com/v1
   CHATLLM_MODEL=gpt-3.5-turbo
   CHATLLM_TEMPERATURE=0.7
   CHATLLM_MAX_TOKENS=1000
   ```

### Frontend

1. Install the required dependencies:
   ```bash
   npm install
   ```

## Usage

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```
   The backend will be available at `http://localhost:8000`.

2. In a new terminal, start the frontend development server:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

## API Endpoints

### Backend API

- `GET /` - Root endpoint with API information
- `POST /api/upload` - Upload a document for indexing
- `POST /api/search` - Perform a search query
- `GET /docs` - Interactive API documentation

### Example Usage

1. Upload a document:
   ```bash
   curl -X POST "http://localhost:8000/api/upload" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@path/to/your/document.txt"
   ```

2. Perform a search:
   ```bash
   curl -X POST "http://localhost:8000/api/search" \
        -H "Content-Type: application/json" \
        -d '{"query": "your search query"}'
   ```

## Project Structure

```
Search-AI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables (not in version control)
│   └── sample_document.txt  # Example document for testing
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx    # Component for document upload
│   │   ├── Header.jsx        # Application header
│   │   ├── SearchBar.jsx     # Search input component
│   │   ├── SearchComponent.js # Main search functionality
│   │   └── ToggleAbstracts.jsx # Toggle for abstract/full text
│   ├── pages/
│   │   ├── AdvancedSearchPage.jsx # Advanced search interface
│   │   ├── SearchPage.js     # Basic search page
│   │   └── SearchPage.jsx    # Enhanced search page
│   ├── App.js               # Main application component
│   ├── App.jsx              # Alternative main application component
│   ├── index.js             # React application entry point
│   └── theme.js             # Application theme configuration
├── public/
│   └── index.html           # Main HTML file
├── package.json             # Frontend dependencies and scripts
└── README.md               # This file
```

## How It Works

1. **Document Upload**: Users upload text documents through the frontend interface.
2. **Embedding Generation**: The backend processes uploaded documents to create vector embeddings using OpenAI's `text-embedding-ada-002` model.
3. **Storage**: Document contents and their embeddings are stored in memory (in production, this would be persisted to a database).
4. **Query Processing**: When a user submits a search query, it's converted to an embedding.
5. **Similarity Search**: The system finds the most relevant document snippets using cosine similarity.
6. **Response Generation**: The retrieved context and user query are sent to OpenAI's GPT model to generate a contextualized answer.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

*   OpenAI for providing the powerful language models and embeddings API
*   The FastAPI team for an excellent Python web framework
*   The React team for the frontend library
# Search-AI
