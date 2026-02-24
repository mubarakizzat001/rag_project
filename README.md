# RAG Project

FastAPI backend for a Retrieval-Augmented Generation (RAG) pipeline.

The project currently supports:
- Uploading files (`.txt`, `.pdf`)
- Processing files into chunks and storing chunks in MongoDB
- Indexing chunks into Qdrant using embedding models (Cohere/OpenAI providers)

## Features

- FastAPI app with lifespan startup/shutdown
- MongoDB integration via `motor`
- File upload and project-based asset tracking
- Chunk generation with overlap support
- Vector indexing flow (`/nlp/nlp/{project_id}`)
- Scalar API docs at `/scalar`

## Tech Stack

- FastAPI
- MongoDB + Motor
- Qdrant (`qdrant-client`)
- Cohere / OpenAI providers
- LangChain loaders/splitters

## Project Structure

```text
rag_project/
├── docker/
│   └── docker-compose.yml
├── src/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── router.py
│   │   ├── data.py
│   │   └── nlp.py
│   ├── controllers/
│   ├── models/
│   └── stores/
└── README.md
```

## Prerequisites

- Python 3.10+
- MongoDB running
- Cohere API key (if embedding backend is Cohere)
- Qdrant connection target:
  - Local embedded path (default style in this project), or
  - Remote URL (example: `http://localhost:6333`)

## Installation

```bash
git clone <your-repo-url>
cd rag_project
cd src
python -m venv .rag_project
source .rag_project/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create `src/.env` from `src/.env.example` and fill values.

```env
APP_NAME="rag_app"
APP_VERSION="0.1"

FILE_ALLOWED_TYPE=["text/plain","application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000

MONGODB_URL="mongodb://localhost:27017"
MONGODB_DATABASE="RAG_PROJECT"

GENERATION_BACKEND="OPENAI"
EMBEDDING_BACKEND="COHERE"

OPENAI_API_KEY=""
OPENAI_API_URL=""
COHERE_API_KEY=""

GENERATION_MODEL_ID="gpt-4o-mini"
EMBEDDING_MODEL_ID="embed-multilingual-light-v3.0"
EMBEDDING_MODEL_SIZE=384

INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=200
GENERATION_DAFAULT_TEMPERATURE=0.1

VECTOR_DB_BACKEND="QDRANT"
VECTOR_DB_PATH="qdrant_db"
VECTOR_DB_DISTANCE_METHOD="cosine"
```

Notes:
- `VECTOR_DB_PATH` behavior:
  - If it starts with `http://` or `https://`, the app treats it as remote Qdrant URL.
  - Otherwise, it is treated as a local embedded Qdrant path under `src/assets/database/`.
- Keep `EMBEDDING_MODEL_SIZE` aligned with your embedding model output dimension.

## Run

From `src/`:

```bash
fastapi dev
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Scalar: `http://127.0.0.1:8000/scalar`

## API Endpoints

### Welcome

- `GET /welcome/`

Response:

```json
{
  "app_name": "rag_app",
  "app_version": "0.1"
}
```

### Upload File

- `POST /data/upload/{filename}`
- Form-data: `file`

Example:

```bash
curl -X POST "http://127.0.0.1:8000/data/upload/my_project" \
  -F "file=@/path/to/file.pdf"
```

### Process Files into Chunks

- `POST /data/process/{project_id}`

Body:

```json
{
  "file_id": "optional_file_id",
  "chunk_size": 100,
  "overlap_size": 20,
  "do_reset": 0
}
```

- If `file_id` is omitted, all project files are processed.
- If `do_reset=1`, existing project chunks are deleted before insert.

### Index Chunks into Vector DB

- `POST /nlp/nlp/{project_id}`

Body:

```json
{
  "do_reset": 0
}
```

This endpoint:
- Reads project chunks from MongoDB
- Generates embeddings
- Creates/updates Qdrant collection
- Inserts records into vector DB

## Common Issues

### Qdrant connection error

Error like:
- `No address associated with hostname`

Cause:
- `VECTOR_DB_PATH` configured as non-URL but treated as hostname previously.

Current behavior in this project:
- Non-URL path -> local embedded Qdrant
- URL -> remote Qdrant server

### Cohere embedding input_type error

Error like:
- `valid input_type must be provided with the provided model`

Ensure:
- Cohere API key is valid
- Embedding backend/model are configured correctly in `.env`

## License

This project is licensed under the MIT License.
