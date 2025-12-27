# API Documentation - TrueLine News

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API is open for public access. Future versions will implement JWT authentication.

## Response Format

All responses follow this standard format:

### Success Response (2xx)
```json
{
  "data": { /* response data */ },
  "message": "Success",
  "status": 200
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message",
  "status": 400
}
```

## Endpoints

### Health Check
Check if the API is running.

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "TrueLine News API is running"
}
```

---

## Articles

### Get All Articles

Retrieve paginated list of verified articles.

```
GET /articles
```

**Query Parameters:**
- `limit` (integer, default: 20) - Number of articles per page
- `offset` (integer, default: 0) - Pagination offset
- `status` (string) - Filter by status: `verified`, `pending`, `unverified`
- `source` (string) - Filter by news source name

**Example:**
```
GET /articles?limit=10&offset=0&status=verified&source=BBC
```

**Response:**
```json
{
  "total": 150,
  "limit": 10,
  "offset": 0,
  "articles": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Breaking News Story",
      "url": "https://example.com/news",
      "excerpt": "Article summary...",
      "source": "BBC",
      "author": "John Smith",
      "credibility_score": 0.95,
      "verified_sources": 5,
      "is_original": true,
      "is_verified": true,
      "cross_checked": true,
      "keywords": ["politics", "election"],
      "sentiment_score": 0.2,
      "reporting_sources": ["Reuters", "AP News"],
      "published_date": "2025-12-27T10:30:00",
      "verified_date": "2025-12-27T11:00:00",
      "status": "verified"
    }
  ]
}
```

---

### Get Single Article

Retrieve details of a specific article.

```
GET /articles/{article_id}
```

**Parameters:**
- `article_id` (string, required) - MongoDB object ID

**Example:**
```
GET /articles/507f1f77bcf86cd799439011
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Breaking News Story",
  "url": "https://example.com/news",
  "content": "Full article content...",
  "excerpt": "Article summary...",
  "source": "BBC",
  "author": "John Smith",
  "credibility_score": 0.95,
  "verified_sources": 5,
  "is_original": true,
  "is_verified": true,
  "cross_checked": true,
  "keywords": ["politics", "election", "news"],
  "sentiment_score": 0.2,
  "reporting_sources": ["Reuters", "AP News", "Guardian"],
  "published_date": "2025-12-27T10:30:00",
  "verified_date": "2025-12-27T11:00:00",
  "status": "verified"
}
```

---

### Create Article

Create a new article (admin only).

```
POST /articles
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Article Title",
  "url": "https://example.com/article",
  "content": "Full article content...",
  "excerpt": "Brief summary...",
  "source": "BBC",
  "author": "John Doe",
  "keywords": ["topic1", "topic2"],
  "reporting_sources": ["Reuters", "AP News"],
  "status": "pending"
}
```

**Required Fields:**
- `title` (string)
- `url` (string, unique)
- `content` (string)
- `source` (string)

**Optional Fields:**
- `excerpt` (string)
- `author` (string)
- `keywords` (array)
- `reporting_sources` (array)
- `status` (string): `verified`, `pending`, `unverified`

**Response:** (201 Created)
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Article Title",
  "url": "https://example.com/article",
  "content": "Full article content...",
  "excerpt": "Brief summary...",
  "source": "BBC",
  "author": "John Doe",
  "credibility_score": 0.0,
  "verified_sources": 0,
  "is_original": false,
  "is_verified": false,
  "cross_checked": false,
  "keywords": ["topic1", "topic2"],
  "sentiment_score": null,
  "reporting_sources": ["Reuters", "AP News"],
  "status": "pending",
  "verified_date": "2025-12-27T12:00:00"
}
```

---

### Update Article

Update an existing article.

```
PUT /articles/{article_id}
Content-Type: application/json
```

**Updatable Fields:**
- `title`
- `excerpt`
- `content`
- `credibility_score`
- `verified_sources`
- `is_original`
- `is_verified`
- `cross_checked`
- `status`
- `sentiment_score`

**Response:** (200 OK)
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Updated Title",
  "credibility_score": 0.92,
  "verified_sources": 4,
  "status": "verified"
  /* ... other fields ... */
}
```

---

### Get Trusted Sources

Retrieve all active trusted news sources.

```
GET /articles/sources
```

**Response:**
```json
{
  "total": 50,
  "sources": [
    {
      "id": "607f1f77bcf86cd799439001",
      "name": "BBC",
      "url": "https://www.bbc.com",
      "domain": "bbc.com",
      "trustworthiness_score": 0.98,
      "article_count": 5420,
      "verification_rate": 0.97,
      "category": "news",
      "country": "UK",
      "is_active": true
    },
    {
      "id": "607f1f77bcf86cd799439002",
      "name": "Reuters",
      "url": "https://www.reuters.com",
      "domain": "reuters.com",
      "trustworthiness_score": 0.97,
      "article_count": 8932,
      "verification_rate": 0.98,
      "category": "news",
      "country": "UK",
      "is_active": true
    }
  ]
}
```

---

## Verification

### Verify News Story

Verify authenticity of a news headline, URL, or story.

```
POST /verify
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "Your news headline or URL here",
  "depth": "standard"
}
```

**Parameters:**
- `query` (string, required) - News headline or URL
- `depth` (string, optional) - Verification depth: `basic`, `standard`, `deep` (default: `standard`)

**Response:**
```json
{
  "is_verified": true,
  "credibility_score": 0.87,
  "verified_sources": 4,
  "is_original": true,
  "status": "verified",
  "sources": ["Reuters", "AP News", "BBC", "Guardian"],
  "keywords": ["politics", "election"],
  "details": {
    "source_reliability": 0.88,
    "content_consistency": 0.85,
    "spread_pattern_healthy": true
  }
}
```

---

### Analyze Credibility

Deep credibility analysis of a specific article URL.

```
POST /verify/analyze-credibility
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "url": "https://example.com/article",
  "sentiment_score": 0.25,
  "keywords": ["politics", "election", "vote"],
  "similar_articles": 15,
  "manipulation_score": 0.1,
  "analysis_timestamp": "2025-12-27T12:00:00"
}
```

---

### Compare Multiple Sources

Compare reporting across multiple sources for the same story.

```
POST /verify/compare-sources
Content-Type: application/json
```

**Request Body:**
```json
{
  "urls": [
    "https://source1.com/article",
    "https://source2.com/article",
    "https://source3.com/article"
  ]
}
```

**Requirements:**
- Minimum 2 URLs
- Maximum 10 URLs

**Response:**
```json
{
  "compared_sources": 3,
  "consistency_score": 0.89,
  "common_keywords": ["politics", "election", "vote"],
  "source_reliability": {
    "source1.com": 0.92,
    "source2.com": 0.88,
    "source3.com": 0.85
  },
  "verdict": "Consistent reporting"
}
```

---

### Verification History

Get recent verification attempts.

```
GET /verify/history
```

**Query Parameters:**
- `limit` (integer, default: 50) - Number of records to return

**Response:**
```json
{
  "total": 150,
  "logs": [
    {
      "query": "News headline to verify",
      "credibility_score": 0.87,
      "is_verified": true,
      "timestamp": "2025-12-27T12:15:00"
    },
    {
      "query": "https://example.com/article",
      "credibility_score": 0.62,
      "is_verified": false,
      "timestamp": "2025-12-27T12:10:00"
    }
  ]
}
```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists (e.g., duplicate URL) |
| 500 | Internal Error | Server error |

---

## Rate Limiting

Currently no rate limiting. Future versions will implement:
- 100 requests per minute for public endpoints
- 1000 requests per minute for authenticated endpoints

---

## Best Practices

1. **Use appropriate depth parameter** for verification:
   - `basic`: Quick check (~2 seconds)
   - `standard`: Full analysis (~5 seconds)
   - `deep`: Comprehensive analysis (~15 seconds)

2. **Cache results** when possible to reduce API calls

3. **Handle errors gracefully** with appropriate fallbacks

4. **Monitor verification accuracy** and provide feedback

5. **Update trusted sources** registry regularly

---

## Example Requests

### Using cURL

```bash
# Get articles
curl http://localhost:5000/api/articles?limit=10&status=verified

# Verify a news story
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"query":"Your news headline","depth":"standard"}'

# Create article
curl -X POST http://localhost:5000/api/articles \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Article Title",
    "url":"https://example.com",
    "content":"Content here",
    "source":"BBC"
  }'
```

### Using JavaScript

```javascript
// Get articles
fetch('/api/articles?limit=10&status=verified')
  .then(res => res.json())
  .then(data => console.log(data));

// Verify news
fetch('/api/verify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'Your news headline',
    depth: 'standard'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### Using Python

```python
import requests

# Get articles
response = requests.get('http://localhost:5000/api/articles', 
                       params={'limit': 10, 'status': 'verified'})
print(response.json())

# Verify news
response = requests.post('http://localhost:5000/api/verify',
                        json={
                          'query': 'Your news headline',
                          'depth': 'standard'
                        })
print(response.json())
```

---

**Last Updated:** December 27, 2025  
**API Version:** 1.0.0
