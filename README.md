# Flask Redis Project

## Overview
This project is a **Flask** web application that integrates **Redis** for task queue management and temporary data storage. It efficiently handles background tasks, improves application performance, and provides fast data access.

## Features
- **Task Queue with Redis**: Uses Redis as a task queue for asynchronous background job execution.
- **Fast Data Storage**: Stores session data and temporary values in Redis for quick retrieval.
- **Health Check Endpoint**: Provides an API endpoint to check the server's status.

## Technologies Used
- **Flask** - Lightweight Python web framework.
- **Redis** - In-memory data structure store, used as a cache and message broker.
- **Python** - Main programming language of the project.

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/omergev/flask_redis_project.git
cd flask_redis_project
```

### 2. Set up a virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install and start Redis
#### macOS (using Homebrew)
```bash
brew install redis
brew services start redis
```
#### Ubuntu
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```
#### Windows
- Download and install Redis from the official Redis website.
- Start the Redis server manually.

### 4. Run the application
```bash
python app.py
```

### 5. Verify it's working
Visit the health check endpoint in your browser:
```
http://127.0.0.1:3000/health
```

## Project Structure
```
flask_redis_project/
│   app.py               # Main Flask application entry point
│   requirements.txt     # Project dependencies
│   redis-server.exe     # Redis server (for Windows users)
│   readme.md            # Project documentation
│
├── config/
│   ├── appsettings.json    # Configuration file
│
├── core/
│   ├── redis_client.py  # Redis client setup
│   ├── scheduler.py     # Task scheduler
│
├── routes/
│   ├── routes.py        # API routes and endpoints
│   ├── __init__.py      # Package initialization
│
└── venv/                # Virtual environment (not included in repo)
```

## Future Improvements
- Implementing authentication for API endpoints.
- Expanding Redis capabilities for additional caching mechanisms.
- Adding Celery for more advanced background task processing.

## Contribution
Feel free to fork the repository and submit pull requests to improve the project.

---
Developed by [Omer Geva](https://github.com/omergev)

