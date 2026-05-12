# External API Server Specification

## 1. Project Overview

- **Project Name**: External API Server
- **Project Type**: RESTful API Service
- **Core Functionality**: A Flask-based external API server providing CRUD operations, health checking, and common utility endpoints
- **Target Users**: Developers and applications requiring external API services

## 2. Technology Stack

- **Framework**: Flask (Python)
- **Server**: Flask development server (for production: use Gunicorn/nginx)
- **Data Format**: JSON
- **Port**: 5000

## 3. API Endpoints

### 3.1 Health Check
- **Endpoint**: `GET /api/health`
- **Description**: Check if the server is running
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "Server is healthy"
  }
  ```

### 3.2 Welcome Message
- **Endpoint**: `GET /api/`
- **Description**: Welcome endpoint with API information
- **Response**:
  ```json
  {
    "name": "External API Server",
    "version": "1.0.0",
    "message": "Welcome to the API Server"
  }
  ```

### 3.3 Echo Endpoint
- **Endpoint**: `POST /api/echo`
- **Description**: Echoes back the received data
- **Request Body**: Any JSON object
- **Response**: Same JSON object received

### 3.4 User Management (Mock)
- **GET /api/users**: List all users
- **GET /api/users/<id>**: Get user by ID
- **POST /api/users**: Create a new user
- **PUT /api/users/<id>**: Update user by ID
- **DELETE /api/users/<id>**: Delete user by ID

### 3.5 Resource Endpoints
- **GET /api/resources**: List all resources
- **GET /api/resources/<id>**: Get resource by ID
- **POST /api/resources**: Create a new resource
- **PUT /api/resources/<id>**: Update resource by ID
- **DELETE /api/resources/<id>**: Delete resource by ID

### 3.6 Utility Endpoints
- **GET /api/time**: Get current server time
- **GET /api/info**: Get server information
- **POST /api/validate**: Validate JSON data structure

## 4. Error Handling

### Error Response Format
```json
{
  "error": true,
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `405`: Method Not Allowed
- `500`: Internal Server Error

## 5. Project Structure

```
/workspace/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── config.py          # Configuration settings
└── run.py             # Server startup script
```

## 6. Configuration

- **Host**: 0.0.0.0 (exposed to external)
- **Port**: 5000
- **Debug Mode**: False (production default)
- **JSON Indent**: 2 spaces

## 7. Acceptance Criteria

1. ✅ Server starts successfully on port 5000
2. ✅ Health check endpoint returns proper status
3. ✅ All CRUD endpoints for users and resources work correctly
4. ✅ Proper error responses for invalid requests
5. ✅ JSON responses are properly formatted
6. ✅ Server accepts connections from external sources (0.0.0.0)
7. ✅ Echo endpoint correctly mirrors input data
8. ✅ Utility endpoints return accurate information
