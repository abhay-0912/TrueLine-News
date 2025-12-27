# Setup Guide - TrueLine News

Complete setup instructions for developing and deploying TrueLine News.

## Quick Start (Docker)

The fastest way to get TrueLine News running:

```bash
# Clone the repository
git clone https://github.com/yourusername/TrueLine-News.git
cd TrueLine-News

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost
# API: http://localhost/api/health
```

## Detailed Installation

### Prerequisites

#### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 2GB, recommended 4GB
- **Disk Space**: 2GB minimum
- **Internet**: Required for API calls and news scraping

#### Software Requirements

**Option 1: Docker (Recommended)**
- Docker Desktop 4.0+
- Docker Compose 1.29+

**Option 2: Manual Installation**
- Python 3.11+
- Node.js 16+ (optional)
- MongoDB 5.0+
- Git

### Installation Steps

#### Option 1: Docker Installation (Recommended)

1. **Install Docker & Docker Compose**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Includes both Docker and Docker Compose

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/TrueLine-News.git
   cd TrueLine-News
   ```

3. **Configure Environment**
   ```bash
   # Copy example configuration
   cp backend/.env.example backend/.env
   
   # Edit if needed (defaults work for development)
   # nano backend/.env
   ```

4. **Start Services**
   ```bash
   # Build and start all containers
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   ```

5. **Verify Installation**
   ```bash
   # Check health
   curl http://localhost/api/health
   
   # Should return:
   # {"status":"healthy","message":"TrueLine News API is running"}
   ```

6. **Access Application**
   - Frontend: http://localhost
   - API Documentation: http://localhost/api

#### Option 2: Manual Installation

**Step 1: Install Dependencies**

On Windows (PowerShell):
```powershell
# Install Python if not present
# Visit https://www.python.org/downloads/

# Install MongoDB
# Visit https://www.mongodb.com/try/download/community

# Or use Chocolatey
choco install python mongodb-community
```

On macOS:
```bash
# Using Homebrew
brew install python@3.11 mongodb-community

# Or using MacPorts
sudo port install python311 mongodb
```

On Linux (Ubuntu):
```bash
# Update package manager
sudo apt update

# Install Python and MongoDB
sudo apt install python3.11 python3.11-venv python3-pip
sudo apt install -y mongodb

# Or using MongoDB's official repository
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
```

**Step 2: Clone Repository**

```bash
git clone https://github.com/yourusername/TrueLine-News.git
cd TrueLine-News
```

**Step 3: Set Up Backend**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (CMD):
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4: Configure Environment**

```bash
# In backend directory
cp .env.example .env

# Edit configuration (optional, defaults work for development)
# nano .env
```

**Step 5: Start MongoDB**

On Windows:
```powershell
# If installed as service, it should start automatically
# If not, run:
mongod

# Or using Chocolatey installed MongoDB:
mongosh
```

On macOS:
```bash
# If installed via Homebrew
brew services start mongodb-community

# Or manually
mongod --config /usr/local/etc/mongod.conf
```

On Linux:
```bash
# If installed via package manager
sudo systemctl start mongod
sudo systemctl status mongod

# Or manually
mongod
```

**Step 6: Start Backend**

```bash
# In backend directory with venv activated
python -m flask run

# Server will run on http://localhost:5000
```

**Step 7: Set Up Frontend**

Open a new terminal (keep backend running):

```bash
cd frontend

# Option A: Python HTTP Server (Python 3)
python -m http.server 8000

# Option B: Node HTTP Server (if Node.js installed)
npx http-server

# Option C: Any other static server
# Access at http://localhost:8000
```

### Initial Configuration

#### MongoDB Setup

1. **Create Database**
   ```bash
   mongosh
   ```

   ```javascript
   // In mongosh shell
   use trueline_news
   db.createCollection("articles")
   db.createCollection("trusted_sources")
   db.createCollection("verification_logs")
   
   // Create indexes
   db.articles.createIndex({ "url": 1 }, { unique: true })
   db.articles.createIndex({ "source": 1 })
   db.trusted_sources.createIndex({ "domain": 1 }, { unique: true })
   ```

2. **Add Trusted Sources**
   ```javascript
   db.trusted_sources.insertMany([
     {
       name: "BBC",
       url: "https://www.bbc.com",
       domain: "bbc.com",
       trustworthiness_score: 0.98,
       category: "news",
       country: "UK",
       language: "en",
       is_active: true,
       added_date: new Date()
     },
     {
       name: "Reuters",
       url: "https://www.reuters.com",
       domain: "reuters.com",
       trustworthiness_score: 0.97,
       category: "news",
       country: "UK",
       language: "en",
       is_active: true,
       added_date: new Date()
     },
     {
       name: "AP News",
       url: "https://apnews.com",
       domain: "apnews.com",
       trustworthiness_score: 0.96,
       category: "news",
       country: "USA",
       language: "en",
       is_active: true,
       added_date: new Date()
     }
   ])
   ```

#### Environment Variables

Create `.env` file in `backend/` directory:

```env
# Flask Configuration
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# MongoDB Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=trueline_news
MONGODB_USER=
MONGODB_PASSWORD=

# API Configuration
API_TIMEOUT=30
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Verification

Test your installation:

```bash
# Test API health
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","message":"TrueLine News API is running"}

# Test getting articles
curl http://localhost:5000/api/articles

# Test frontend
# Open http://localhost:8000 in browser
```

## Development Setup

### IDE Configuration

#### Visual Studio Code

1. **Install Extensions**
   - Python
   - Pylance
   - MongoDB for VS Code
   - Thunder Client (for API testing)

2. **Create Launch Configuration** (`.vscode/launch.json`)
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Flask",
         "type": "python",
         "request": "launch",
         "module": "flask",
         "env": {
           "FLASK_APP": "app",
           "FLASK_ENV": "development"
         },
         "args": ["run"],
         "jinja": true,
         "cwd": "${workspaceFolder}/backend"
       }
     ]
   }
   ```

3. **Python Path** (`.vscode/settings.json`)
   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python"
   }
   ```

### Database Tools

**MongoDB Compass** (GUI Client)
1. Download from https://www.mongodb.com/products/tools/compass
2. Connect to `mongodb://localhost:27017`
3. Explore databases and collections

**mongosh** (CLI Client)
```bash
# Connect
mongosh

# Common commands
show dbs
use trueline_news
show collections
db.articles.find().limit(5)
```

### Running Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_articles.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Install linting tools
pip install pylint flake8 black isort

# Check code style
flake8 app/
pylint app/

# Auto-format code
black app/
isort app/
```

## Troubleshooting

### Port Already in Use

**Problem:** Port 5000 or 8000 already in use

**Solution:**

```bash
# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess
Stop-Process -Id <PID>

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### MongoDB Connection Failed

**Problem:** Cannot connect to MongoDB

**Solutions:**

```bash
# Check if MongoDB is running
# Windows
net start | findstr MongoDB

# macOS
brew services list | grep mongodb

# Linux
sudo systemctl status mongod

# Verify connection
mongosh --eval "db.adminCommand('ping')"

# Check firewall
# Ensure port 27017 is not blocked
```

### Dependencies Installation Failed

**Problem:** pip install fails

**Solutions:**

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Clear cache
pip install --no-cache-dir -r requirements.txt

# Use specific Python version
python3.11 -m pip install -r requirements.txt
```

### CORS Errors in Frontend

**Problem:** Frontend cannot call backend API

**Solution:** Ensure Flask-CORS is installed and configured

```bash
pip install Flask-CORS

# Check app/__init__.py has:
# CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## Performance Optimization

### Frontend Optimization
- Minimize CSS/JS files
- Enable gzip compression
- Use CDN for Chart.js library
- Implement lazy loading for images

### Backend Optimization
- Enable caching with Redis (optional)
- Use connection pooling for database
- Implement pagination for large result sets
- Add response compression

```python
# Install compression support
pip install flask-compress

# Enable in app/__init__.py
from flask_compress import Compress
Compress(app)
```

### Database Optimization
- Create indexes on frequently queried fields
- Archive old verification logs
- Monitor query performance

```javascript
// Create compound indexes
db.articles.createIndex({ "source": 1, "verified_date": -1 })
db.articles.createIndex({ "status": 1, "credibility_score": -1 })
```

## Next Steps

1. **Read API Documentation** - See `docs/API.md`
2. **Explore Architecture** - See `docs/ARCHITECTURE.md`
3. **Create Test Articles** - Use API endpoints to add sample data
4. **Set Up Monitoring** - Configure logging and error tracking
5. **Deploy** - Follow production deployment guide

## Getting Help

- Check logs: `docker-compose logs -f` or `flask run --debug`
- Review API docs: `docs/API.md`
- Search issues: GitHub Issues
- Create new issue with error details

---

**Last Updated:** December 27, 2025
