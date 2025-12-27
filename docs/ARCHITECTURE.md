# Architecture Documentation - TrueLine News

## System Overview

TrueLine News is a full-stack application designed to verify news authenticity and provide credibility scoring before publication.

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         Client Layer                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Web Browser / Frontend Application              │   │
│  │  (HTML5, CSS3, JavaScript, React.js - optional)         │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬───────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                       API Gateway Layer                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            Nginx Reverse Proxy / Load Balancer          │   │
│  │         (SSL/TLS, Request Routing, Compression)         │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬───────────────────────────────────────┘
                         │ Internal Network
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                    Application Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Flask Web Server (Gunicorn)                   │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         RESTful API Endpoints                      │  │  │
│  │  │  • Articles Management                             │  │  │
│  │  │  • News Verification                               │  │  │
│  │  │  • Credibility Analysis                            │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Business Logic Layer                       │  │  │
│  │  │  • Verification Service                            │  │  │
│  │  │  • Source Validation                               │  │  │
│  │  │  • Credibility Scoring                             │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌──────────┐  ┌─────────────┐  ┌──────────────┐
    │ Database │  │ NLP Engine  │  │ Web Scraper  │
    │ (MongoDB)│  │(NLTK,       │  │(BeautifulSoup│
    │          │  │scikit-learn)│  │+ Requests)   │
    └──────────┘  └─────────────┘  └──────────────┘
```

## Component Architecture

### Frontend (Client Layer)

**Technology Stack:**
- HTML5, CSS3, JavaScript
- React.js (optional for advanced UI)
- Chart.js for data visualization
- Responsive design for mobile support

**Key Components:**
1. **Home Page**: Landing page with platform overview
2. **News Feed**: Display verified articles
3. **Verification Tool**: User interface for verifying news
4. **Results Dashboard**: Display verification results with charts
5. **About Section**: Platform information

**Directory Structure:**
```
frontend/
├── index.html          # Main entry point
├── css/
│   └── style.css       # Styling
├── js/
│   └── main.js         # Application logic
├── assets/             # Images, fonts, icons
└── nginx.conf          # Web server config
```

### Backend (Application Layer)

**Technology Stack:**
- Python 3.11+
- Flask 2.3+
- RESTful API design
- MongoEngine ORM

**Architecture Layers:**

#### 1. Routes Layer (`app/routes/`)

Handles HTTP request routing and response formatting.

```
routes/
├── articles.py         # Article management endpoints
├── verification.py     # News verification endpoints
└── __init__.py         # Blueprint registration
```

**Responsibilities:**
- Request validation
- Parameter parsing
- Response formatting
- Error handling

#### 2. Services Layer (`app/services/`)

Contains business logic and core functionality.

```
services/
├── verification_service.py  # Main verification logic
└── __init__.py
```

**VerificationService:**
- Coordinates verification workflow
- Orchestrates other services
- Calculates credibility scores
- Manages source validation

#### 3. Models Layer (`app/models/`)

Database schema and data validation.

```
models/
├── __init__.py              # Model definitions
  ├── Article              # News article model
  ├── VerificationLog      # Verification history
  └── TrustedSource        # Trusted news sources
```

**Model Relationships:**
```
Article
├── source (TrustedSource reference)
├── keywords (array)
├── reporting_sources (array)
└── verification_logs (array)

TrustedSource
├── trustworthiness_score
├── articles (Article array)
└── verification_history (VerificationLog array)

VerificationLog
├── query (Article search)
├── found_sources (TrustedSource array)
└── timestamp
```

#### 4. Utils Layer (`app/utils/`)

Utility functions and helper services.

```
utils/
├── nlp_processor.py          # NLP operations
├── web_scraper.py            # Web scraping
├── credibility_analyzer.py   # Credibility scoring
└── __init__.py
```

**NLP Processor:**
- Keyword extraction
- Sentiment analysis
- Text similarity calculation
- Sensationalism detection

**Web Scraper:**
- Content extraction
- Metadata parsing
- URL validation
- Rate limiting

**Credibility Analyzer:**
- Multi-factor scoring
- Source evaluation
- Misinformation detection
- Evidence collection

### Database Layer (MongoDB)

**Collections:**

#### Articles Collection
```javascript
{
  _id: ObjectId,
  title: String,
  url: String (unique),
  content: String,
  excerpt: String,
  source: String,
  author: String,
  
  // Verification fields
  credibility_score: Double (0-1),
  verified_sources: Integer,
  is_original: Boolean,
  is_verified: Boolean,
  cross_checked: Boolean,
  
  // Analysis
  keywords: [String],
  sentiment_score: Double (-1 to 1),
  reporting_sources: [String],
  
  // Metadata
  published_date: Date,
  verified_date: Date,
  last_updated: Date,
  status: String (verified|pending|unverified),
  
  indexes: {
    url: unique,
    source: standard,
    verified_date: descending,
    credibility_score: descending
  }
}
```

#### TrustedSource Collection
```javascript
{
  _id: ObjectId,
  name: String (unique),
  url: String,
  domain: String (unique),
  description: String,
  
  // Metrics
  trustworthiness_score: Double (0-1),
  article_count: Integer,
  verification_rate: Double (0-1),
  
  // Classification
  category: String (news|investigative|specialized|international),
  country: String,
  language: String,
  
  // Status
  is_active: Boolean,
  added_date: Date,
  last_verified: Date,
  
  indexes: {
    domain: unique,
    name: unique,
    trustworthiness_score: descending,
    is_active: standard
  }
}
```

#### VerificationLog Collection
```javascript
{
  _id: ObjectId,
  query: String,
  credibility_score: Double,
  verified_sources: Integer,
  is_verified: Boolean,
  is_original: Boolean,
  
  matching_articles: [String],
  found_sources: [String],
  
  timestamp: Date,
  
  indexes: {
    timestamp: descending,
    query: standard
  }
}
```

## Verification Workflow

### Step-by-Step Process

```
User Input (News Headline/URL)
    │
    ▼
1. Input Processing & Validation
   └─ Normalize text
   └─ Extract URL if present
   └─ Validate input format
    │
    ▼
2. Content Analysis (NLP)
   └─ Extract keywords
   └─ Analyze sentiment
   └─ Detect language patterns
    │
    ▼
3. Source Discovery
   └─ Search for similar articles in database
   └─ Scrape if URL provided
   └─ Identify reporting sources
    │
    ▼
4. Source Validation
   └─ Check TrustedSource registry
   └─ Retrieve trustworthiness scores
   └─ Evaluate source reliability
    │
    ▼
5. Content Consistency Analysis
   └─ Compare articles across sources
   └─ Calculate similarity scores
   └─ Identify inconsistencies
    │
    ▼
6. Spread Pattern Analysis
   └─ Check how news disseminates
   └─ Identify original vs. reshared content
   └─ Analyze social media patterns (future)
    │
    ▼
7. Credibility Scoring
   ├─ Source Reliability (40%)
   ├─ Content Consistency (30%)
   ├─ Spread Pattern (20%)
   └─ Original Reporting (10%)
    │
    ▼
8. Verification Decision
   └─ Score >= 0.6 & Multiple Sources → Verified
   └─ Score < 0.6 → Unverified
    │
    ▼
9. Log & Return Results
   └─ Save to VerificationLog
   └─ Return detailed report to user
```

## API Communication Flow

### Example: Verify News Story

```
Browser (Frontend)
    │
    │ POST /api/verify
    │ {query: "...", depth: "standard"}
    │
    ▼
Nginx (Reverse Proxy)
    │ Route to /api/*
    │ Handle SSL/TLS
    │ Request/response logging
    │
    ▼
Flask Application
    │ URL Routing
    │ Request unpacking
    │
    ▼
verification_bp.verify_news()
    │ Validate input
    │ Call VerificationService
    │
    ▼
VerificationService.verify()
    │ NLP analysis
    │ Source discovery
    │ Credibility calculation
    │
    ▼
Return Result JSON
    │
    ▼
Browser (Receive & Display)
```

## Deployment Architecture

### Docker Containers

```
Docker Network (trueline-network)
│
├─ MongoDB Container
│  ├─ Port: 27017
│  ├─ Volume: mongodb_data
│  └─ Health check: mongosh ping
│
├─ Backend Container
│  ├─ Port: 5000 (internal)
│  ├─ Depends on: MongoDB
│  ├─ Volume: app code (development)
│  └─ Command: gunicorn or flask run
│
└─ Nginx Container
   ├─ Port: 80 (external)
   ├─ Proxies to: Backend (5000)
   ├─ Serves: Frontend (static files)
   └─ Config: nginx.conf
```

### Production Deployment

```
Typical Production Setup:

Load Balancer
    │
    ├─ Nginx Reverse Proxy #1
    │
    ├─ Nginx Reverse Proxy #2
    │
    └─ Nginx Reverse Proxy #N
        │
        ├─ Flask API Server #1
        ├─ Flask API Server #2
        └─ Flask API Server #N
            │
            └─ MongoDB Replica Set
                ├─ Primary
                ├─ Secondary #1
                └─ Secondary #2
            
        Redis Cache (optional)
```

## Data Flow Diagram

### Articles Ingestion Flow

```
External News Sources
    │
    ├─ Manual Submission
    │
    ├─ Web Scraper (Automated)
    │
    └─ API Integration
        │
        ▼
    Verification Pipeline
    ├─ Content Analysis
    ├─ Source Validation
    ├─ Credibility Scoring
    │
    ▼
    MongoDB Storage
    ├─ Articles Collection
    ├─ VerificationLog
    │
    ▼
    API Endpoints
    │
    ▼
    Frontend Display
```

## Scalability Considerations

### Horizontal Scaling
- Multiple Flask instances behind load balancer
- Database replication for read distribution
- Caching layer (Redis) for frequently accessed data
- Queue system (Celery) for background jobs

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries with proper indexing
- Implement pagination for large result sets
- Compress API responses

### Database Optimization
- Sharding for very large datasets
- Archive old verification logs
- Query performance monitoring
- Regular index optimization

## Security Architecture

### Security Layers

```
Client → TLS/HTTPS → Nginx (SSL termination)
    │
    ├─ Input Validation
    ├─ Rate Limiting
    └─ CORS Configuration
        │
        ▼
    Flask Application
    ├─ Authentication (future)
    ├─ Authorization (future)
    ├─ Input Sanitization
    └─ Error Handling
        │
        ▼
    Database
    ├─ Connection Pooling
    ├─ Query Parameterization
    └─ Data Encryption (at rest)
```

### Security Measures

1. **Transport Security**
   - HTTPS/TLS for all communications
   - Certificate management

2. **Application Security**
   - Input validation and sanitization
   - SQL injection prevention (using ORM)
   - CORS configuration
   - Rate limiting

3. **Data Security**
   - MongoDB access control
   - Database encryption
   - Regular backups
   - Data anonymization where needed

4. **Infrastructure Security**
   - Firewall configuration
   - Network isolation
   - Container security scanning
   - Secrets management

## Performance Optimization

### Frontend Optimization
- Minified CSS/JS
- Lazy loading for images
- Client-side caching
- Compression (gzip)

### Backend Optimization
- Database query optimization
- Response caching
- Connection pooling
- Asynchronous processing

### Database Optimization
- Indexing strategy
- Query profiling
- Batch operations
- Archiving old data

## Monitoring and Logging

### Monitoring Metrics

```
Application Metrics:
├─ API Response Time
├─ Request Success Rate
├─ Error Rate
├─ Active Connections
│
Database Metrics:
├─ Query Performance
├─ Index Efficiency
├─ Connection Pool Usage
├─ Disk Usage
│
System Metrics:
├─ CPU Usage
├─ Memory Usage
├─ Network I/O
└─ Disk I/O
```

### Logging Strategy

```
Log Levels:
├─ DEBUG (development)
├─ INFO (general operations)
├─ WARNING (potential issues)
├─ ERROR (error conditions)
└─ CRITICAL (system failures)

Log Destinations:
├─ Console (development)
├─ File (application)
├─ Structured logs (JSON)
└─ ELK Stack (production)
```

## Future Enhancements

### Planned Improvements

1. **Advanced NLP**
   - Semantic analysis
   - Named entity recognition
   - Multi-language support

2. **ML/AI Integration**
   - Fake news classification
   - Automated fact-checking
   - Predictive credibility scoring

3. **Performance**
   - Real-time processing
   - Machine learning inference
   - Edge computing capabilities

4. **Integration**
   - Social media APIs
   - Browser extensions
   - Third-party integrations

5. **Features**
   - User accounts and profiles
   - Community fact-checking
   - Notification system
   - Advanced analytics

---

**Last Updated:** December 27, 2025  
**Architecture Version:** 1.0.0
