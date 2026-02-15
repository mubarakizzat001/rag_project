# RAG Project

A FastAPI-based backend for a **Retrieval-Augmented Generation (RAG)** system. The project handles document upload, text extraction, chunking, and storage in MongoDB — forming the data ingestion pipeline for a RAG application.

## 📋 Features

- **Document Upload** — Upload `.txt` and `.pdf` files with validation for type and size
- **Text Extraction** — Extract text content from uploaded documents using LangChain loaders (PyPDFLoader, TextLoader)
- **Intelligent Chunking** — Split documents into overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`
- **MongoDB Storage** — Persist projects and document chunks via Motor (async MongoDB driver)
- **Project Organization** — Files and chunks are organized per project
- **Chunk Reset** — Option to delete existing chunks before re-processing a document
- **Smart File Naming** — Automatic sanitization and unique filename generation to prevent collisions
- **API Documentation** — Interactive docs via Scalar UI at `/scalar`
- **Docker Support** — Docker Compose file for running MongoDB

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI 0.118.0 |
| **Database** | MongoDB 8.x (via Motor 3.7.1) |
| **Document Processing** | LangChain 1.2.10, LangChain Community 0.4.1 |
| **Text Splitting** | LangChain Text Splitters 1.1.0 |
| **PDF Parsing** | PyMuPDF 1.27.1 |
| **Data Validation** | Pydantic Settings 2.12.0 |
| **API Docs** | Scalar FastAPI 1.6.1 |
| **Async File I/O** | aiofiles 25.1.0 |

## 📦 Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for MongoDB)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag_project
   ```

2. **Start MongoDB**
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```

3. **Create a virtual environment**
   ```bash
   cd src
   python -m venv .rag_project
   source .rag_project/bin/activate  # On Windows: .rag_project\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your settings:
   ```env
   APP_NAME="rag_app"
   APP_VERSION="0.1"

   FILE_ALLOWED_TYPE=["text/plain","application/pdf"]
   FILE_MAX_SIZE=10
   FILE_DEFAULT_CHUNK_SIZE=512000

   MONGODB_URL="mongodb://localhost:27017"
   MONGODB_DATABASE="RAG_PROJECT"
   ```

## 🚀 Running the Application

### Development

```bash
cd src
fastapi dev
```

The API will be available at `http://localhost:8000`

### Production

```bash
cd src
fastapi run
```

## 📚 API Endpoints

### `GET /welcome/` — Application Info

Returns the application name and version.

**Response:**
```json
{
  "app_name": "rag_app",
  "app_version": "0.1"
}
```

---

### `POST /data/upload/{project_id}` — Upload a File

Upload a document to a project. Creates the project if it doesn't exist.

**Parameters:**
| Parameter | Location | Description |
|-----------|----------|-------------|
| `project_id` | Path | Project identifier |
| `file` | Form-data | The file to upload (`.txt` or `.pdf`) |

**Example:**
```bash
curl -X POST "http://localhost:8000/data/upload/my_project" \
  -F "file=@document.pdf"
```

**Success (200):**
```json
{
  "message": "File uploaded successfully",
  "file_id": "aB3xYz789Klm_document.pdf"
}
```

**Errors:**
- `400` — File type not allowed or file size too large
- `500` — Internal upload error

---

### `POST /data/process/{project_id}` — Process & Chunk a File

Extract text from an uploaded file, split it into chunks, and store the chunks in MongoDB.

**Parameters:**
| Parameter | Location | Description |
|-----------|----------|-------------|
| `project_id` | Path | Project identifier |

**Request Body (JSON):**
```json
{
  "file_id": "aB3xYz789Klm_document.pdf",
  "chunk_size": 100,
  "overlap_size": 20,
  "do_reset": 0
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `file_id` | string | *required* | The file ID returned from the upload endpoint |
| `chunk_size` | int | `100` | Number of characters per chunk |
| `overlap_size` | int | `20` | Overlap between consecutive chunks |
| `do_reset` | int | `0` | Set to `1` to delete existing chunks for this project before inserting |

**Success (200):**
```json
{
  "message": "processing successfully",
  "no_record": 42
}
```

**Errors:**
- `400` — Processing error (empty content or unsupported format)

---

### `GET /scalar` — API Documentation

Interactive API reference powered by Scalar.  
Access at: `http://localhost:8000/scalar`

## 📁 Project Structure

```
rag_project/
├── docker/
│   └── docker-compose.yml          # MongoDB container
├── src/
│   ├── .env                        # Environment variables (not in git)
│   ├── .env.example                # Environment template
│   ├── main.py                     # App entry point & lifespan (MongoDB connection)
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── routes/                     # API route handlers
│   │   ├── router.py               # Welcome endpoint
│   │   ├── data.py                 # Upload & Process endpoints
│   │   └── schemes/
│   │       └── data.py             # Request body schemas
│   │
│   ├── controllers/                # Business logic
│   │   ├── BaseController.py       # Base controller (settings, random string)
│   │   ├── DataController.py       # File validation & unique naming
│   │   ├── ProjectController.py    # Project directory management
│   │   └── ProcessController.py    # Text extraction & chunking (LangChain)
│   │
│   ├── models/                     # Data models & database layer
│   │   ├── BaseDataModel.py        # Base model with DB client
│   │   ├── ProjectModel.py         # Project CRUD operations
│   │   ├── ChunkModel.py           # Chunk CRUD operations
│   │   ├── db_schemes/
│   │   │   ├── project.py          # Project Pydantic schema
│   │   │   └── chunk.py            # Data chunk Pydantic schema
│   │   └── enums/
│   │       ├── DataBaseenum.py     # Collection name constants
│   │       ├── ResponseEnum.py     # Response message constants
│   │       └── ProcessEnum.py      # File extension constants
│   │
│   └── helpers/
│       └── config.py               # Pydantic Settings configuration
│
├── LICENSE
└── README.md
```

## ⚙️ Configuration

All settings are managed via environment variables in `src/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `rag_app` |
| `APP_VERSION` | Application version | `0.1` |
| `FILE_ALLOWED_TYPE` | Allowed MIME types (JSON list) | `["text/plain","application/pdf"]` |
| `FILE_MAX_SIZE` | Max file size in MB | `10` |
| `FILE_DEFAULT_CHUNK_SIZE` | Upload stream chunk size (bytes) | `512000` |
| `MONGODB_URL` | MongoDB connection string | — |
| `MONGODB_DATABASE` | Database name | `RAG_PROJECT` |

## 🐳 Docker

A Docker Compose file is provided for MongoDB:

```bash
# Start MongoDB
docker compose -f docker/docker-compose.yml up -d

# Stop MongoDB
docker compose -f docker/docker-compose.yml down
```

MongoDB will be accessible on `localhost:27017`. Data is persisted via a named Docker volume (`mongodb`).

## 📄 License

Licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.