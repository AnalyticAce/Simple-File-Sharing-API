# Simple-File-Sharing-API

This project is a simple file sharing API built using FastAPI. It provides endpoints to upload, download, and retrieve metadata about files. The uploaded files are stored securely using `pickle` for serialization, and metadata is managed in a JSON file.

## Features

- **File Upload**: Upload files to the server with metadata tracking.
- **File Download**: Securely download files by their unique ID.
- **Metadata Retrieval**: Access metadata for all files or a specific file.
- **Secure Storage**: Files are serialized using `pickle` for added security.
- **Download Count Tracking**: Monitor how many times each file has been downloaded.

## Technologies Used

- **Python**
- **FastAPI**: Web framework for building APIs.
- **Pickle**: For secure file serialization.
- **JSON**: For metadata storage.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   fastapi run app/main.py --host 0.0.0.0 --port 8080 --reload
   ```

The server will be accessible at `http://0.0.0.0:8080`.

## API Endpoints

### Upload File

**Endpoint**: `POST /file/upload/`

Uploads a file to the server.

**Request**:
- `file`: The file to upload (as `multipart/form-data`).

**Response**:
```json
{
  "file_id": "<unique_file_id>",
  "original_name": "<original_filename>",
  "content_type": "<file_mime_type>",
  "file_size": <file_size_in_bytes>,
  "download_link": "<download_url>"
}
```

### Download File

**Endpoint**: `GET /file/download/{file_id}`

Downloads a file by its unique ID.

**Response**:
- Returns the file as an attachment.

### Get Metadata for All Files

**Endpoint**: `GET /file/metadata/`

Retrieves metadata for all uploaded files.

**Response**:
```json
{
  "<file_id>": {
    "original_name": "<original_filename>",
    "content_type": "<file_mime_type>",
    "file_size": <file_size_in_bytes>,
    "download_count": <download_count>,
    "download_link": "<download_url>"
  },
  ...
}
```

### Get Metadata for a Specific File

**Endpoint**: `GET /file/metadata/{file_id}`

Retrieves metadata for a specific file by its unique ID.

**Response**:
```json
{
  "original_name": "<original_filename>",
  "content_type": "<file_mime_type>",
  "file_size": <file_size_in_bytes>,
  "download_count": <download_count>,
  "download_link": "<download_url>"
}
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- FastAPI documentation: https://fastapi.tiangolo.com/
- Python `pickle` module documentation: https://docs.python.org/3/library/pickle.html

