# RAG Project

A FastAPI-based backend for a **Retrieval-Augmented Generation (RAG)** system. The project handles document upload, asset tracking, text extraction, intelligent chunking, and storage in MongoDB — forming the complete data ingestion pipeline for a RAG application.

## 📋 Features

- **Document Upload** — Upload `.txt` and `.pdf` files with validation for type and size
- **Asset Management** — Track uploaded files as assets in MongoDB with metadata (size, type, timestamps)
- **Text Extraction** — Extract text content from uploaded documents using LangChain loaders (PyPDFLoader, TextLoader)
- **Intelligent Chunking** — Split documents into overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`
- **Batch Processing** — Process all files in a project at once, or a single file by ID
- **MongoDB Storage** — Persist projects, assets, and document chunks via Motor (async MongoDB driver)
- **Automatic Index Management** — Collections and indexes are created automatically on first use
- **Project Organization** — Files, assets, and chunks are organized per project
- **Chunk Reset** — Option to delete existing chunks before re-processing a project
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

### `POST /data/upload/{filename}` — Upload a File

Upload a document to a project. Creates the project if it doesn't exist. The uploaded file is tracked as an **asset** in the `assets` collection with metadata such as file size, type, and timestamp.

**Parameters:**
| Parameter | Location | Description |
|-----------|----------|-------------|
| `filename` | Path | Project identifier (used both as the project name and to organize files) |
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
  "file_id": "67c1a2b3d4e5f6a7b8c9d0e1"
}
```

> **Note:** The `file_id` returned is the MongoDB ObjectId of the asset record, not the filename on disk.

**Errors:**
- `400` — File type not allowed or file size too large
- `500` — Internal upload error

---

### `POST /data/process/{project_id}` — Process & Chunk Files

Extract text from uploaded files, split into chunks, and store the chunks in MongoDB. Supports **single file** or **batch processing** of all files in a project.

**Parameters:**
| Parameter | Location | Description |
|-----------|----------|-------------|
| `project_id` | Path | Project identifier |

**Request Body (JSON):**

#### Single File Processing
```json
{
  "file_id": "aB3xYz789Klm_document.pdf",
  "chunk_size": 100,
  "overlap_size": 20,
  "do_reset": 0
}
```

#### Batch Processing (all project files)
```json
{
  "chunk_size": 100,
  "overlap_size": 20,
  "do_reset": 0
}
```

| Field | Type | Default | Required | Description |
|-------|------|---------|----------|-------------|
| `file_id` | string | `null` | No | The asset name of the file to process. **If omitted, all files in the project are processed.** |
| `chunk_size` | int | `100` | No | Number of characters per chunk |
| `overlap_size` | int | `20` | No | Overlap between consecutive chunks |
| `do_reset` | int | `0` | No | Set to `1` to delete all existing chunks for this project before inserting |

**Success (200):**
```json
{
  "message": "processing successfully",
  "no_record": 42,
  "no_file": 3
}
```

| Response Field | Description |
|----------------|-------------|
| `no_record` | Total number of chunks inserted |
| `no_file` | Number of files processed |

**Errors:**
- `400` — No file found, processing error, or unsupported format

---

### `GET /scalar` — API Documentation

Interactive API reference powered by Scalar.  
Access at: `http://localhost:8000/scalar`

## �️ Database Schema

The application uses **3 MongoDB collections**, each with automatic index management:

### `projects` Collection

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Auto-generated primary key |
| `project_id` | string | Unique project identifier |

**Indexes:** `project_id` (unique)

### `assets` Collection

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Auto-generated primary key |
| `asset_project_id` | ObjectId | Reference to the parent project |
| `asset_name` | string | Unique filename (random prefix + sanitized original name) |
| `asset_type` | string | Asset type (e.g., `"file"`) |
| `asset_size` | int | File size in bytes |
| `asset_config` | dict | Optional configuration metadata |
| `asset_pushed_at` | datetime | Upload timestamp |

**Indexes:** `asset_project_id` (non-unique), `asset_name` (unique)

### `chunks` Collection

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Auto-generated primary key |
| `chunk_text` | string | The text content of the chunk |
| `chunk_metadata` | dict | Source metadata (file path, page number, etc.) |
| `chunk_order` | int | Position of the chunk in the document |
| `chunk_project_id` | ObjectId | Reference to the parent project |
| `chunk_asset_id` | ObjectId | Reference to the source asset |

**Indexes:** `chunk_project_id` (non-unique)

## �📁 Project Structure

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
│   ├── assets/                     # Uploaded file storage
│   │   └── files/                  # Project directories with uploaded files
│   │
│   ├── routes/                     # API route handlers
│   │   ├── router.py               # Welcome endpoint
│   │   ├── data.py                 # Upload & Process endpoints
│   │   └── schemes/
│   │       └── data.py             # Request body schemas (process_request)
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
│   │   ├── AssetModel.py           # Asset CRUD operations (file tracking)
│   │   ├── ChunkModel.py           # Chunk CRUD operations (bulk insert)
│   │   ├── db_schemes/
│   │   │   ├── project.py          # Project Pydantic schema
│   │   │   ├── asset.py            # Asset Pydantic schema
│   │   │   └── chunk.py            # Data chunk Pydantic schema
│   │   └── enums/
│   │       ├── DataBaseenum.py     # Collection name constants
│   │       ├── ResponseEnum.py     # Response message constants
│   │       ├── ProcessEnum.py      # File extension constants
│   │       └── AssetTypeEnum.py    # Asset type constants
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