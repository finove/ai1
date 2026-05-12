from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any, Dict
import uuid
import platform
from config import Config

app = FastAPI(
    title=Config.API_NAME,
    version=Config.API_VERSION,
    description="External API Server built with FastAPI"
)

users_db: List[Dict[str, Any]] = []
resources_db: List[Dict[str, Any]] = []


def generate_id() -> str:
    return str(uuid.uuid4())


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, description="User name")
    email: Optional[str] = Field(default="", description="User email")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="User name")
    email: Optional[str] = Field(None, description="User email")


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: str


class ResourceCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Resource title")
    description: Optional[str] = Field(default="", description="Resource description")
    type: Optional[str] = Field(default="general", description="Resource type")


class ResourceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Resource title")
    description: Optional[str] = Field(None, description="Resource description")
    type: Optional[str] = Field(None, description="Resource type")


class ResourceResponse(BaseModel):
    id: str
    title: str
    description: str
    type: str
    created_at: str


@app.get("/api/", tags=["Info"])
async def welcome():
    return {
        "name": Config.API_NAME,
        "version": Config.API_VERSION,
        "message": "Welcome to the API Server"
    }


@app.get("/api/health", tags=["Info"])
async def health_check():
    return {
        "status": "ok",
        "message": "Server is healthy"
    }


@app.post("/api/echo", tags=["Utility"])
async def echo(request: Request):
    data = await request.json()
    return data


@app.get("/api/time", tags=["Info"])
async def get_time():
    return {
        "timestamp": datetime.now().isoformat(),
        "unix": int(datetime.now().timestamp())
    }


@app.get("/api/info", tags=["Info"])
async def get_info():
    return {
        "server": Config.API_NAME,
        "version": Config.API_VERSION,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/validate", tags=["Utility"])
async def validate(request: Request):
    data = await request.json()

    validation_result = {
        "valid": True,
        "data": data,
        "keys": list(data.keys()) if isinstance(data, dict) else None,
        "length": len(data) if hasattr(data, '__len__') else None
    }

    if not isinstance(data, dict):
        validation_result["valid"] = False
        validation_result["error"] = "Data must be a JSON object"

    return validation_result


@app.get("/api/users", response_model=List[UserResponse], tags=["Users"])
async def get_users():
    return users_db


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: str):
    user = next((u for u in users_db if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/users", response_model=UserResponse, status_code=201, tags=["Users"])
async def create_user(user: UserCreate):
    new_user = {
        "id": generate_id(),
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now().isoformat()
    }
    users_db.append(new_user)
    return new_user


@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(user_id: str, user_update: UserUpdate):
    user = next((u for u in users_db if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name is not None:
        user['name'] = user_update.name
    if user_update.email is not None:
        user['email'] = user_update.email

    return user


@app.delete("/api/users/{user_id}", tags=["Users"])
async def delete_user(user_id: str):
    global users_db
    user = next((u for u in users_db if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_db = [u for u in users_db if u['id'] != user_id]
    return {"message": "User deleted successfully"}


@app.get("/api/resources", response_model=List[ResourceResponse], tags=["Resources"])
async def get_resources():
    return resources_db


@app.get("/api/resources/{resource_id}", response_model=ResourceResponse, tags=["Resources"])
async def get_resource(resource_id: str):
    resource = next((r for r in resources_db if r['id'] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@app.post("/api/resources", response_model=ResourceResponse, status_code=201, tags=["Resources"])
async def create_resource(resource: ResourceCreate):
    new_resource = {
        "id": generate_id(),
        "title": resource.title,
        "description": resource.description,
        "type": resource.type,
        "created_at": datetime.now().isoformat()
    }
    resources_db.append(new_resource)
    return new_resource


@app.put("/api/resources/{resource_id}", response_model=ResourceResponse, tags=["Resources"])
async def update_resource(resource_id: str, resource_update: ResourceUpdate):
    resource = next((r for r in resources_db if r['id'] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource_update.title is not None:
        resource['title'] = resource_update.title
    if resource_update.description is not None:
        resource['description'] = resource_update.description
    if resource_update.type is not None:
        resource['type'] = resource_update.type

    return resource


@app.delete("/api/resources/{resource_id}", tags=["Resources"])
async def delete_resource(resource_id: str):
    global resources_db
    resource = next((r for r in resources_db if r['id'] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    resources_db = [r for r in resources_db if r['id'] != resource_id]
    return {"message": "Resource deleted successfully"}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "error": True,
            "message": "Endpoint not found",
            "code": "NOT_FOUND"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "code": "INTERNAL_ERROR"
        }
    )
