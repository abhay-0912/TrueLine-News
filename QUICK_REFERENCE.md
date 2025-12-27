# TrueLine News - Quick Reference Guide

## 🚀 Quick Start (5 minutes)

### With Docker (Easiest)
```bash
cd TrueLine-News
docker-compose up -d
# Frontend: http://localhost
# API: http://localhost/api/health
```

### Without Docker
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m flask run

# Terminal 2 - Frontend
cd frontend
python -m http.server 8000

# Terminal 3 - MongoDB (if not running)
mongod
```

## 📁 Important Files & Directories

| Path | Purpose |
|------|---------|
| `frontend/` | Web interface (HTML/CSS/JS) |
| `backend/app/` | Flask application code |
| `backend/requirements.txt` | Python dependencies |
| `database/schema.mongodb` | Database structure |
| `docker-compose.yml` | Container configuration |
| `docs/API.md` | API documentation |
| `docs/SETUP.md` | Installation guide |
| `.env.example` | Configuration template |

## 🔌 API Endpoints Quick Reference

### Health Check
```
GET /api/health
```

### Articles
```
GET    /api/articles                    # List articles
GET    /api/articles/{id}               # Get article
POST   /api/articles                    # Create article
PUT    /api/articles/{id}               # Update article
GET    /api/articles/sources            # Trusted sources
```

### Verification
```
POST   /api/verify                      # Verify news
POST   /api/verify/analyze-credibility  # Deep analysis
POST   /api/verify/compare-sources      # Compare sources
GET    /api/verify/history              # History log
```

## 📝 Common Commands

### Backend Development
```bash
# Start server
python -m flask run

# Run tests
pytest

# Check code style
flake8 app/
black app/

# Install new package
pip install package-name
pip freeze > requirements.txt
```

### Database
```bash
# Connect to MongoDB
mongosh

# View collections
show collections
db.articles.find().limit(5)
```

### Docker
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild images
docker-compose build
```

## 🔐 Environment Configuration

### Backend (.env)
```
FLASK_ENV=development
MONGODB_HOST=localhost
MONGODB_DB=trueline_news
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

## 📚 Documentation Map

| Document | Content |
|----------|---------|
| `README_NEW.md` | Project overview, features, tech stack |
| `docs/SETUP.md` | Installation, configuration, troubleshooting |
| `docs/API.md` | All endpoints, request/response formats |
| `docs/ARCHITECTURE.md` | System design, data flows, deployment |
| `CONTRIBUTING.md` | Development guidelines, code style |
| `PROJECT_SUMMARY.md` | What was created, next steps |

## 💡 Common Tasks

### Add a New API Endpoint

1. **Create route** in `backend/app/routes/articles.py` or `verification.py`
```python
@articles_bp.route('/new-endpoint', methods=['GET'])
def new_endpoint():
    return jsonify({'data': 'response'})
```

2. **Test it** with curl or browser
```bash
curl http://localhost:5000/api/articles/new-endpoint
```

### Connect Frontend to API
```javascript
// In frontend/js/main.js
const response = await fetch(`${API_BASE_URL}/endpoint`);
const data = await response.json();
```

### Add MongoDB Index
```javascript
// In mongosh
db.articles.createIndex({ "field": 1 })
db.articles.createIndex({ "field1": 1, "field2": -1 })
```

### Run Verification
```bash
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"query":"your news headline"}'
```

## 🐛 Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| Port already in use | `lsof -ti:5000 \| xargs kill -9` |
| MongoDB not found | Start MongoDB or use Docker |
| Imports failing | Install requirements: `pip install -r requirements.txt` |
| CORS errors | Check Flask-CORS is configured |
| Docker container won't start | Check logs: `docker-compose logs backend` |
| File not found | Ensure you're in correct directory |

## 📊 Project Structure Overview

```
Frontend Layer
    ↓ HTTP/HTTPS
API Gateway (Nginx)
    ↓ Internal Network
Flask Backend
    ├─ Routes (API endpoints)
    ├─ Services (Business logic)
    ├─ Utils (NLP, scraping, scoring)
    └─ Models (Database schemas)
    ↓
MongoDB Database
```

## 🎯 Key Concepts

### Credibility Score
Formula: (Source×0.4) + (Consistency×0.3) + (Spread×0.2) + (Original×0.1)
Range: 0.0 (unreliable) to 1.0 (fully verified)

### Verification Levels
- **basic**: Quick verification (~2 sec)
- **standard**: Full analysis (~5 sec)
- **deep**: Comprehensive check (~15 sec)

### Database Collections
1. **articles** - Verified news items
2. **trusted_sources** - Credible news outlets
3. **verification_logs** - Verification history

## 🔗 External Resources

- MongoDB: https://docs.mongodb.com
- Flask: https://flask.palletsprojects.com
- NLTK: https://www.nltk.org
- Docker: https://docs.docker.com
- Python: https://docs.python.org

## 📞 Getting Help

1. Check `docs/SETUP.md` for installation issues
2. Check `docs/API.md` for endpoint questions
3. Check `docs/ARCHITECTURE.md` for design questions
4. Review code comments and docstrings
5. Check GitHub issues or create new one

## ✅ Verification Checklist

- [ ] Docker installed (for containerized setup)
- [ ] Python 3.11+ installed (for manual setup)
- [ ] MongoDB running (local or Docker)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment files configured (`.env`)
- [ ] Backend server running (`python -m flask run`)
- [ ] Frontend accessible (http://localhost:8000 or :80)
- [ ] API responding (`curl http://localhost:5000/api/health`)

## 🎓 Learning Path

1. **Day 1**: Setup environment, explore code structure
2. **Day 2**: Read architecture docs, understand data flows
3. **Day 3**: Test API endpoints, explore verification logic
4. **Day 4**: Add new feature or endpoint
5. **Day 5**: Write tests, improve code quality

## 🚀 Next Steps After Setup

1. **Create Article**
   ```bash
   curl -X POST http://localhost:5000/api/articles \
     -H "Content-Type: application/json" \
     -d '{"title":"Test","url":"https://example.com","content":"text","source":"BBC"}'
   ```

2. **Verify News**
   ```bash
   curl -X POST http://localhost:5000/api/verify \
     -H "Content-Type: application/json" \
     -d '{"query":"breaking news headline"}'
   ```

3. **View Article**
   ```bash
   curl http://localhost:5000/api/articles?limit=10
   ```

## 📈 Performance Tips

- Use pagination: `?limit=20&offset=0`
- Add database indexes before queries
- Enable response compression in production
- Cache frequently accessed data
- Use connection pooling for database

## 🔒 Security Checklist

- [ ] HTTPS enabled in production
- [ ] Database credentials in `.env` (not in code)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORM)
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error messages don't expose internals
- [ ] Regular security audits

---

**Keep this guide handy for quick reference!**

For detailed information, see the full documentation in `/docs`

**Version:** 1.0.0 | **Updated:** December 27, 2025
