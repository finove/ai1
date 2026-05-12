#!/usr/bin/env python3
"""
External API Server - Startup Script (FastAPI)
"""

import uvicorn
from config import Config

if __name__ == '__main__':
    print(f"Starting {Config.API_NAME} v{Config.API_VERSION}")
    print(f"Server running on http://{Config.HOST}:{Config.PORT}")
    print("Press CTRL+C to stop the server")
    uvicorn.run(
        "app:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )
