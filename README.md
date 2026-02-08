# RAG Project

A FastAPI-based RESTful API for managing document uploads in a RAG (Retrieval-Augmented Generation) system. This project provides secure file handling with validation, unique filename generation, and project-based organization.

## 📋 Features

- **File Upload Management**: Upload documents with validation for file type and size
- **Smart File Naming**: Automatic generation of unique filenames with sanitization
- **Project Organization**: Files organized by project ID in dedicated folders
- **File Validation**: 
  - Supported formats: Text files (`.txt`) and PDFs (`.pdf`)
  - Configurable maximum file size (default: 10 MB)
- **Error Handling & Logging**: Comprehensive error catching with detailed logging
- **API Documentation**: Interactive API documentation via Scalar UI
- **Async File Handling**: Efficient chunked file uploads using `aiofiles`

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.118.0
- **API Documentation**: Scalar FastAPI 1.6.1
- **Configuration**: Pydantic Settings 2.12.0
- **File Handling**: aiofiles 25.1.0
- **Environment Management**: python-dotenv 1.2.1

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag_project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the `src/` directory:
   ```bash
   cp src/.env.example src/.env
   ```
   
   Edit `src/.env` to configure your settings:
   ```env
   APP_NAME="rag_app"
   APP_VERSION="0.1"
   
   FILE_ALLOWED_TYPE=["text/plain","application/pdf"]
   FILE_MAX_SIZE=10
   FILE_DEFAULT_CHUNK_SIZE=512000 #512K
   ```

## 🚀 Running the Application

### Development Mode

```bash
cd src
fastapi dev
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
cd src
fastapi run
```

## 📚 API Endpoints

### 1. Welcome Endpoint

Get application information.

**Endpoint**: `GET /welcome/`

**Response**:
```json
{
  "app_name": "rag_app",
  "app_version": "0.1"
}
```

### 2. File Upload

Upload a file to a specific project.

**Endpoint**: `POST /data/upload/{filename}`

**Parameters**:
- `filename` (path parameter): Project ID where the file will be stored
- `file` (form-data): The file to upload

**Request Example**:
```bash
curl -X POST "http://localhost:8000/data/upload/project123" \
  -F "file=@document.pdf"
```

**Success Response** (200 OK):
```json
{
  "message": "File uploaded successfully"
}
```

**Error Responses**:

- **400 Bad Request** - Invalid file type:
  ```json
  {
    "message": "File type not allowed"
  }
  ```

- **400 Bad Request** - File too large:
  ```json
  {
    "message": "File size too large"
  }
  ```

- **500 Internal Server Error** - File upload error:
  ```json
  {
    "message": "[Error details]"
  }
  ```
  Note: All errors are logged to the application logs for debugging.

### 3. API Documentation

Interactive API documentation powered by Scalar.

**Endpoint**: `GET /scalar`

Access at: `http://localhost:8000/scalar`

## 📁 Project Structure

```
rag_project/
├── src/
│   ├── .env                    # Environment variables (not in git)
│   ├── .env.example           # Environment template
│   ├── main.py                # Application entry point
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── routes/                # API route handlers
│   │   ├── router.py          # Welcome route
│   │   └── data.py            # File upload route
│   │
│   ├── controllers/           # Business logic
│   │   ├── BaseController.py      # Base controller with utilities
│   │   ├── DataController.py      # File validation & processing
│   │   └── ProjectController.py   # Project path management
│   │
│   ├── models/                # Data models
│   │   └── enums/
│   │       └── ResponseEnum.py    # Response message enums
│   │
│   ├── helpers/               # Helper utilities
│   │   └── config.py          # Configuration management
│   │
│   └── .rag_project/          # Project data storage
│       └── {project_id}/      # Project-specific folders
│
├── LICENSE
└── README.md
```

## ⚙️ Configuration

All configuration is managed through environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `"rag_app"` |
| `APP_VERSION` | Application version | `"0.1"` |
| `FILE_ALLOWED_TYPE` | List of allowed MIME types | `["text/plain", "application/pdf"]` |
| `FILE_MAX_SIZE` | Maximum file size in MB | `10` |
| `FILE_DEFAULT_CHUNK_SIZE` | Chunk size for file uploads in bytes | `512000` (512KB) |

## 🔐 File Handling Details

### File Validation

The system validates uploaded files based on:
- **Content Type**: Only allows MIME types specified in `FILE_ALLOWED_TYPE`
- **File Size**: Enforces maximum size limit from `FILE_MAX_SIZE`

### Unique Filename Generation

To prevent filename conflicts and sanitize unsafe characters:

1. **Sanitization**: Removes special characters, keeping only alphanumeric, underscores, and dots
2. **Random Prefix**: Adds a 12-character random string prefix
3. **Collision Prevention**: Checks for existing files and regenerates if needed

Example:
- Original: `My Document (final).pdf`
- Saved as: `aB3xYz789Klm_MyDocumentfinal.pdf`

### File Storage

Files are organized by project:
```
src/.rag_project/
├── project123/
│   ├── aB3xYz789Klm_document1.pdf
│   └── cD4wVu890Mno_document2.txt
└── project456/
    └── eF5tQr901Pqr_report.pdf
```

## 🧪 Testing the API

### Using cURL

```bash
# Upload a text file
curl -X POST "http://localhost:8000/data/upload/myproject" \
  -F "file=@sample.txt"

# Upload a PDF
curl -X POST "http://localhost:8000/data/upload/myproject" \
  -F "file=@document.pdf"
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/data/upload/myproject"
files = {"file": open("document.pdf", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This is a development version. For production deployment, ensure proper security measures, rate limiting, and error handling are implemented.