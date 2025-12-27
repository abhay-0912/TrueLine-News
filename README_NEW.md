# TrueLine News - Verified-First Digital News Platform

A comprehensive news platform that publishes only pre-verified and fact-checked articles. TrueLine News uses advanced verification mechanisms including natural language processing, source validation, and credibility analysis to prevent misinformation spread at the source level.

## Overview

TrueLine News is a full-scale news website where every article undergoes rigorous authenticity validation before publication. The platform:

- **Verifies news sources** by tracing original publication sources and cross-checking multiple independent reliable sources
- **Analyzes dissemination patterns** to distinguish legitimate news from reshared or manipulated content
- **Implements credibility scoring** using source trustworthiness, content similarity analysis, and spread behavior metrics
- **Prevents misinformation** by blocking unverified content before it reaches the public
- **Maintains transparency** through evidence-based verification without censorship or opinion bias

## Key Features

### 🔍 News Verification
- **Multi-Source Validation**: Ensures news is independently reported by multiple trusted sources
- **Source Trustworthiness Analysis**: Evaluates credibility of reporting sources
- **Content Similarity Detection**: Identifies reshared vs. original content
- **Spread Pattern Analysis**: Analyzes how news disseminates across platforms

### 📊 Credibility Scoring
- **Multi-Factor Analysis**: Considers source reliability, content consistency, and spread patterns
- **Transparent Metrics**: Shows users verification details and evidence
- **Real-Time Verification**: Instant credibility assessment of news stories
- **Historical Tracking**: Maintains logs of all verification attempts

### 🎓 Educational Impact
- **Media Literacy**: Teaches users how to identify misinformation
- **Critical Thinking**: Encourages evidence-based news consumption
- **Transparency Reports**: Provides detailed verification evidence
- **Learning Resources**: Educational materials about news verification

## Real-World Use Cases

- **Students**: Access reliable news and avoid viral misinformation
- **Journalists**: Quick background validation of ongoing stories
- **Educators**: Teach media literacy and critical thinking with real examples
- **Social Media Users**: Consume trustworthy news instead of rumors
- **Organizations**: Ensure internal communications are based on verified information

## Technology Stack

### Frontend
- **HTML5, CSS3, JavaScript** - Core web technologies
- **React.js** (optional) - For advanced interactive UI
- **Chart.js** - Visualization of credibility indicators and verification metrics
- **Responsive Design** - Mobile-friendly interface

### Backend
- **Python** - Core language
- **Flask / FastAPI** - Lightweight web framework
- **RESTful APIs** - Standard API design for content delivery and verification workflows
- **NLTK & scikit-learn** - Natural Language Processing capabilities
- **BeautifulSoup4** - Web scraping from trusted news portals

### Data Processing & Analysis
- **Natural Language Processing (NLP)** - Content similarity detection
- **Keyword Extraction** - Topic consistency analysis
- **Sentiment Analysis** - Detection of sensational or misleading tone
- **Web Scraping** - Data collection from verified news sources

### Database
- **MongoDB** - NoSQL document database for flexible data storage
- **PostgreSQL** (optional) - For complex relational queries
- Stores: Verified source registry, article history, verification logs

### Deployment
- **Docker & Docker Compose** - Containerization and orchestration
- **Nginx** - Reverse proxy and static file serving
- **Gunicorn** - Python WSGI application server

## Project Structure

```
TrueLine-News/
├── frontend/                 # Frontend application
│   ├── index.html           # Main HTML entry point
│   ├── css/
│   │   └── style.css        # Stylesheet
│   ├── js/
│   │   └── main.js          # JavaScript logic
│   ├── assets/              # Images and static assets
│   └── nginx.conf           # Nginx configuration
│
├── backend/                  # Backend application
│   ├── app/
│   │   ├── __init__.py      # Flask app initialization
│   │   ├── models/          # Database models
│   │   │   └── __init__.py
│   │   ├── routes/          # API routes
│   │   │   ├── articles.py
│   │   │   ├── verification.py
│   │   │   └── __init__.py
│   │   ├── services/        # Business logic
│   │   │   ├── verification_service.py
│   │   │   └── __init__.py
│   │   └── utils/           # Utility functions
│   │       ├── nlp_processor.py
│   │       ├── web_scraper.py
│   │       ├── credibility_analyzer.py
│   │       └── __init__.py
│   ├── tests/               # Unit tests
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── Dockerfile           # Docker configuration
│
├── database/                 # Database setup
│   ├── schema.mongodb       # MongoDB schema definition
│   └── init.sh              # Database initialization script
│
├── docs/                    # Documentation
│   ├── API.md              # API documentation
│   ├── SETUP.md            # Setup guide
│   └── ARCHITECTURE.md     # Architecture documentation
│
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+ (optional, for advanced frontend)
- Docker & Docker Compose (for containerized deployment)
- MongoDB 5.0+ or Docker
- 2GB RAM minimum

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TrueLine-News.git
cd TrueLine-News
```

#### 2. Using Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# The application will be available at:
# Frontend: http://localhost
# API: http://localhost/api
```

#### 3. Manual Installation

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the Flask server
python -m flask run
```

**Frontend Setup:**

```bash
cd frontend

# For simple HTTP server (Python 3):
python -m http.server 8000

# Or use any other static server
# Then open http://localhost:8000 in your browser
```

**Database Setup:**

```bash
# Ensure MongoDB is running
# On Windows, Mac, or Linux with MongoDB installed:
mongosh

# Or using Docker:
docker run -d -p 27017:27017 --name trueline-mongodb mongo:latest
```

## API Documentation

### Articles Endpoints

#### Get All Articles
```
GET /api/articles?limit=20&offset=0&status=verified&source=BBC
```

Response:
```json
{
  "total": 100,
  "limit": 20,
  "offset": 0,
  "articles": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Breaking News Story",
      "url": "https://example.com/news",
      "source": "BBC",
      "credibility_score": 0.95,
      "verified_sources": 5,
      "is_original": true,
      "status": "verified",
      "keywords": ["politics", "election", "news"],
      "sentiment_score": 0.2,
      "published_date": "2025-12-27T10:30:00",
      "verified_date": "2025-12-27T11:00:00"
    }
  ]
}
```

#### Get Single Article
```
GET /api/articles/{article_id}
```

#### Create Article
```
POST /api/articles
Content-Type: application/json

{
  "title": "Article Title",
  "url": "https://example.com/article",
  "content": "Full article content...",
  "source": "BBC",
  "author": "John Doe",
  "keywords": ["topic1", "topic2"],
  "reporting_sources": ["Reuters", "AP News"]
}
```

### Verification Endpoints

#### Verify News Story
```
POST /api/verify
Content-Type: application/json

{
  "query": "News headline or URL to verify",
  "depth": "standard"
}
```

Response:
```json
{
  "is_verified": true,
  "credibility_score": 0.87,
  "verified_sources": 4,
  "is_original": true,
  "status": "verified",
  "sources": ["Reuters", "AP News", "BBC", "Guardian"],
  "keywords": ["topic1", "topic2"],
  "details": {
    "source_reliability": 0.88,
    "content_consistency": 0.85,
    "spread_pattern_healthy": true
  }
}
```

#### Analyze Credibility
```
POST /api/verify/analyze-credibility
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

#### Compare Sources
```
POST /api/verify/compare-sources
Content-Type: application/json

{
  "urls": [
    "https://source1.com/article",
    "https://source2.com/article",
    "https://source3.com/article"
  ]
}
```

#### Get Verification History
```
GET /api/verify/history?limit=50
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

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
MONGODB_USER=admin
MONGODB_PASSWORD=password

# API Configuration
API_TIMEOUT=30
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Running Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Architecture

### Verification Flow

1. **Input Processing**: Accept news headline, URL, or article content
2. **Content Analysis**: Extract keywords, analyze sentiment, detect language patterns
3. **Source Discovery**: Search for matching articles across trusted sources
4. **Source Validation**: Check trustworthiness scores of reporting sources
5. **Consistency Analysis**: Compare content across sources for inconsistencies
6. **Credibility Scoring**: Calculate multi-factor credibility score
7. **Verification Decision**: Determine if content meets publication threshold
8. **Result Return**: Provide detailed verification report to user

### Credibility Score Factors

- **Source Reliability (40%)**: Track record and reputation of news sources
- **Content Consistency (30%)**: Alignment of reporting across sources
- **Spread Pattern (20%)**: How news spreads indicates legitimacy
- **Original Reporting (10%)**: Evidence of independent investigation

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

## Security Considerations

- Never publish API keys or credentials
- Validate and sanitize all user inputs
- Use HTTPS in production
- Implement rate limiting on APIs
- Regular security audits of dependencies
- Secure database access with strong authentication

## Deployment

### Production Deployment with Docker

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose -f docker-compose.yml up -d

# Monitor logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale backend=3
```

### Environment-Specific Setup

Update configuration for production:
- Set `FLASK_ENV=production`
- Configure strong database credentials
- Enable HTTPS/TLS
- Set up monitoring and logging
- Configure backups

## Monitoring and Maintenance

- Monitor API response times
- Track database performance
- Analyze verification accuracy
- Update trusted sources registry regularly
- Review and update NLP models
- Audit user access logs

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Verify connection string in .env
```

### API Port Already in Use
```bash
# Change port in .env
# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### Dependencies Not Installing
```bash
# Upgrade pip
pip install --upgrade pip

# Clear cache and reinstall
pip install --no-cache-dir -r requirements.txt
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for verified information in the digital age
- Built with modern web technologies and best practices
- Community contributions and feedback welcome

## Contact & Support

For questions, issues, or feedback:
- Create an issue on GitHub
- Email: support@trueline-news.com
- Documentation: See `/docs` folder

## Roadmap

- [ ] Advanced ML models for fact-checking
- [ ] Browser extension for instant verification
- [ ] Mobile applications (iOS/Android)
- [ ] Multi-language support
- [ ] Integration with major news aggregators
- [ ] AI-powered misinformation detection
- [ ] Community fact-checking features
- [ ] API for third-party integrations

---

**TrueLine News** - Making the internet a more trustworthy place, one verified article at a time.
