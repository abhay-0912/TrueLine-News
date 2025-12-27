# TrueLine News - Visual Guides

## System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  Frontend Application (HTML/CSS/JavaScript)                 │   │
│  │  ├─ Article Feed (News Display)                             │   │
│  │  ├─ Verification Tool (Input Query)                         │   │
│  │  ├─ Results Dashboard (Chart.js Visualization)              │   │
│  │  └─ Navigation (Smooth Scrolling)                           │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                    HTTP/HTTPS Requests
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │                                        │
        │  NGINX REVERSE PROXY                   │
        │  ├─ SSL/TLS Termination                │
        │  ├─ Request Routing                    │
        │  ├─ Response Compression               │
        │  └─ Static File Serving                │
        │                                        │
        └────────────────────────────────────────┘
                             │
                    Internal Network
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐       ┌───────────┐        ┌──────────┐
    │         │       │           │        │          │
    │ FLASK   │       │   FLASK   │        │  FLASK   │
    │ API #1  │       │   API #2  │        │  API #N  │
    │         │       │           │        │          │
    └─────────┘       └───────────┘        └──────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    Database Queries
                             │
                             ▼
         ┌──────────────────────────────────────┐
         │                                      │
         │  MONGODB DATABASE                    │
         │  ├─ Articles Collection              │
         │  ├─ TrustedSource Collection         │
         │  └─ VerificationLog Collection       │
         │                                      │
         └──────────────────────────────────────┘
```

## Request Flow Diagram

```
USER ACTION
    │
    ▼ (Example: Verify News)
POST /api/verify
{query: "Breaking news headline"}
    │
    ▼
FLASK VERIFICATION ENDPOINT
    │
    ├─ Input Validation
    ├─ Parameter Parsing
    │
    ▼
VERIFICATION SERVICE
    │
    ├─ Step 1: NLP Analysis
    │  ├─ Extract Keywords
    │  ├─ Analyze Sentiment
    │  └─ Detect Language Patterns
    │
    ├─ Step 2: Source Discovery
    │  ├─ Search Database for Similar Articles
    │  ├─ Web Scrape if URL Provided
    │  └─ Identify Reporting Sources
    │
    ├─ Step 3: Source Validation
    │  ├─ Query TrustedSource Registry
    │  ├─ Get Trustworthiness Scores
    │  └─ Evaluate Source Reliability
    │
    ├─ Step 4: Consistency Analysis
    │  ├─ Compare Articles Across Sources
    │  ├─ Calculate Similarity Scores
    │  └─ Identify Inconsistencies
    │
    ├─ Step 5: Spread Pattern Analysis
    │  ├─ Check Multi-Source Reporting
    │  ├─ Identify Original vs. Reshared
    │  └─ Analyze Dissemination Pattern
    │
    ├─ Step 6: Credibility Scoring
    │  ├─ Source Reliability Weight (40%)
    │  ├─ Content Consistency Weight (30%)
    │  ├─ Spread Pattern Weight (20%)
    │  └─ Original Reporting Weight (10%)
    │
    ▼
VERIFICATION RESULT
{
  "is_verified": true,
  "credibility_score": 0.87,
  "verified_sources": 4,
  "status": "verified"
}
    │
    ├─ Save to VerificationLog
    │
    ▼
JSON RESPONSE
    │
    ▼
FRONTEND RECEIVES
    │
    ├─ Parse Response
    ├─ Update UI
    ├─ Display Credibility Score
    ├─ Draw Chart.js Visualization
    │
    ▼
USER SEES RESULTS
```

## Data Model Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ARTICLE                                                    │
│  ├─ _id (ObjectId)                                          │
│  ├─ title                                                   │
│  ├─ url (unique)                                            │
│  ├─ content                                                 │
│  ├─ source ─────────────────────┐                           │
│  ├─ credibility_score           │                           │
│  ├─ verified_sources            │                           │
│  ├─ keywords                    │                           │
│  ├─ reporting_sources ──────┐   │                           │
│  ├─ sentiment_score         │   │                           │
│  ├─ is_original             │   │                           │
│  ├─ is_verified             │   │                           │
│  ├─ published_date          │   │                           │
│  ├─ verified_date           │   │                           │
│  └─ status                  │   │                           │
│                             │   │                           │
└─────────────────────────────┼───┼───────────────────────────┘
                              │   │
                  References  │   │ References
                              │   │
      ┌───────────────────────┘   └───────────────────┐
      │                                               │
      ▼                                               ▼
┌──────────────────────┐                   ┌──────────────────────┐
│ TRUSTED_SOURCE       │                   │ VERIFICATION_LOG     │
│ ├─ _id               │                   │ ├─ _id               │
│ ├─ name              │                   │ ├─ query             │
│ ├─ url               │                   │ ├─ credibility_score │
│ ├─ domain            │                   │ ├─ verified_sources  │
│ ├─ trustworthiness   │                   │ ├─ is_verified       │
│ ├─ article_count     │                   │ ├─ found_sources     │
│ ├─ verification_rate │                   │ └─ timestamp         │
│ ├─ category          │                   │                      │
│ ├─ country           │                   │ (Logs all            │
│ └─ is_active         │                   │  verification        │
│                      │                   │  attempts)           │
└──────────────────────┘                   └──────────────────────┘
```

## Verification Scoring Formula

```
CREDIBILITY SCORE CALCULATION

Final Score = (S × 0.4) + (C × 0.3) + (P × 0.2) + (O × 0.1)

Where:
  S = Source Reliability Score
      └─ Based on TrustedSource trustworthiness_score
      └─ Boosted by number of sources reporting
      └─ Range: 0.0 to 1.0

  C = Content Consistency Score
      └─ Based on similarity between articles
      └─ Higher when articles align closely
      └─ Range: 0.0 to 1.0

  P = Spread Pattern Score
      └─ 0.8 if multiple independent sources
      └─ 0.3 if single or related sources
      └─ Range: 0.0 to 1.0

  O = Original Reporting Score
      └─ 0.7 if original reporting detected
      └─ 0.5 if simply reshared
      └─ Range: 0.0 to 1.0

FINAL INTERPRETATION:
  >= 0.8  → Highly Credible (Publish)
  >= 0.6  → Credible (Publish with review)
  >= 0.4  → Moderately Credible (Requires verification)
  <  0.4  → Low Credibility (Do Not Publish)

PUBLICATION RULES:
  ✓ Score >= 0.6 AND Multiple Sources → VERIFIED
  ✗ Score < 0.6 OR Single Source      → UNVERIFIED
```

## Docker Container Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      DOCKER NETWORK                            │
│           (Internal communication bridge)                      │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   MONGODB    │  │   BACKEND    │  │   FRONTEND   │          │
│  │  CONTAINER   │  │  CONTAINER   │  │  CONTAINER   │          │
│  │              │  │              │  │              │          │
│  │ Port: 27017  │  │ Port: 5000   │  │ Port: 80     │          │
│  │              │  │  (internal)  │  │              │          │
│  │ Image: mongo │  │ Image: python│  │ Image: nginx │          │
│  │              │  │ Flask app    │  │              │          │
│  │ Volume:      │  │              │  │ Serves:      │          │
│  │ mongodb_data │  │ Volume:      │  │ Frontend     │          │
│  │              │  │ app code     │  │ files        │          │
│  │              │  │              │  │              │          │
│  │ Health Check │  │ Depends on:  │  │ Depends on:  │          │
│  │ mongosh ping │  │ MongoDB      │  │ Backend      │          │
│  │              │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
│                  Docker Network Bridge                         │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             │
                    External Port Mapping
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   Host Port           Host Port             Host Port
      27017               5000                   80
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    User Access from Browser
```

## File Organization Tree

```
TrueLine-News/
│
├─ 📄 Configuration Files (Root)
│  ├─ docker-compose.yml       ← Start here for deployment
│  ├─ LICENSE                   ← MIT License
│  ├─ .gitignore               ← Git configuration
│  ├─ CONTRIBUTING.md          ← Developer guidelines
│  │
│  └─ 📚 Documentation (Multiple Guides)
│     ├─ README_NEW.md         ← Main project overview
│     ├─ QUICK_REFERENCE.md    ← Fast answers
│     ├─ PROJECT_SUMMARY.md    ← What was created
│     ├─ COMPLETION_SUMMARY.md ← This completion
│     └─ IMPLEMENTATION_CHECKLIST.md ← Feature list
│
├─ 🌐 Frontend (`frontend/`)    ← User Interface
│  ├─ index.html               ← Main HTML page
│  ├─ css/
│  │  └─ style.css             ← All styling
│  ├─ js/
│  │  └─ main.js               ← All client logic
│  ├─ assets/                  ← Images, fonts
│  ├─ .env.example             ← Config template
│  └─ nginx.conf               ← Web server
│
├─ 🔧 Backend (`backend/`)      ← API Server
│  ├─ app/
│  │  ├─ __init__.py           ← Flask setup
│  │  ├─ models/
│  │  │  └─ __init__.py        ← Database models
│  │  ├─ routes/
│  │  │  ├─ articles.py        ← Article endpoints
│  │  │  ├─ verification.py    ← Verification endpoints
│  │  │  └─ __init__.py        ← Route registration
│  │  ├─ services/
│  │  │  ├─ verification_service.py ← Verification logic
│  │  │  └─ __init__.py
│  │  └─ utils/
│  │     ├─ nlp_processor.py   ← NLP operations
│  │     ├─ web_scraper.py     ← Web scraping
│  │     ├─ credibility_analyzer.py ← Scoring
│  │     └─ __init__.py
│  ├─ tests/                   ← Unit tests
│  ├─ requirements.txt         ← Python packages
│  ├─ .env.example             ← Config template
│  ├─ Dockerfile               ← Container image
│  └─ .dockerignore            ← Docker ignore
│
├─ 💾 Database (`database/`)    ← Data Layer
│  ├─ schema.mongodb           ← MongoDB definition
│  └─ init.sh                  ← Init script
│
└─ 📖 Documentation (`docs/`)   ← Detailed Guides
   ├─ API.md                   ← All endpoints
   ├─ SETUP.md                 ← Installation
   └─ ARCHITECTURE.md          ← System design
```

## Development Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      DEVELOPMENT CYCLE                           │
└──────────────────────────────────────────────────────────────────┘

START
  │
  ▼
1. SETUP ENVIRONMENT
   ├─ Clone repository
   ├─ Install dependencies
   ├─ Configure .env
   └─ Start services (Docker or manual)
  │
  ▼
2. UNDERSTAND SYSTEM
   ├─ Read QUICK_REFERENCE.md
   ├─ Review docs/ARCHITECTURE.md
   ├─ Explore code structure
   └─ Test API endpoints
  │
  ▼
3. DEVELOP FEATURE
   ├─ Create feature branch
   ├─ Write code
   ├─ Follow style guide
   └─ Add comments/docstrings
  │
  ▼
4. TEST CODE
   ├─ Write unit tests
   ├─ Run pytest
   ├─ Check code coverage
   └─ Verify functionality
  │
  ▼
5. CODE REVIEW
   ├─ Check PEP 8 compliance
   ├─ Review docstrings
   ├─ Verify error handling
   └─ Test edge cases
  │
  ▼
6. COMMIT & PUSH
   ├─ Write clear commit message
   ├─ Push to feature branch
   └─ Create Pull Request
  │
  ▼
7. MERGE & DEPLOY
   ├─ Code review approval
   ├─ Merge to main
   ├─ Build Docker image
   └─ Deploy to environment
  │
  ▼
END
```

## Deployment Pipeline

```
LOCAL DEVELOPMENT
       │
       ▼ (git push)
   ┌────────────┐
   │ GitHub Repo│ ← Version Control
   └────────────┘
       │
       ▼ (docker build)
   ┌──────────────────────┐
   │ Docker Images        │
   │ ├─ Backend Image     │
   │ ├─ Frontend Image    │
   │ └─ MongoDB Image     │
   └──────────────────────┘
       │
       ▼ (docker push, optional)
   ┌──────────────────────┐
   │ Docker Registry      │ (Docker Hub, AWS ECR, etc.)
   └──────────────────────┘
       │
       ▼ (docker-compose up)
   ┌──────────────────────┐
   │ STAGING ENV          │
   │ ├─ Test Containers   │
   │ ├─ Run Tests         │
   │ └─ Verify Deployment │
   └──────────────────────┘
       │
       ▼ (manual approval)
   ┌──────────────────────┐
   │ PRODUCTION ENV       │
   │ ├─ Live Containers   │
   │ ├─ Load Balancer     │
   │ ├─ Database Repl.    │
   │ └─ Monitoring        │
   └──────────────────────┘
       │
       ▼
   USERS ACCESS PLATFORM
```

---

**Visual Guides Complete!** 📊

These diagrams help understand:
- System architecture
- Request flows
- Data relationships
- Container setup
- File organization
- Development workflow
- Deployment process

Use these in conjunction with the detailed documentation for complete understanding.
