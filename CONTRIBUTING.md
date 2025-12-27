# Contributing to TrueLine News

Thank you for your interest in contributing to TrueLine News! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### 1. Reporting Bugs

If you find a bug, please create an issue with:

- **Title**: Clear, concise description
- **Description**: Detailed explanation of the bug
- **Reproduction Steps**: How to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, Docker version, etc.
- **Screenshots**: If applicable

### 2. Suggesting Enhancements

For feature requests:

- **Title**: Clear, concise feature description
- **Motivation**: Why this feature is needed
- **Implementation**: How it could be implemented (optional)
- **Examples**: Use cases or examples
- **References**: Related issues or PRs

### 3. Pull Requests

#### Before Starting

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Set up development environment (see SETUP.md)
4. Keep your branch updated with main: `git pull origin main`

#### While Developing

1. **Follow Code Style**
   - Use Python PEP 8 for backend
   - Use standard JavaScript conventions for frontend
   - Use meaningful variable and function names
   - Add comments for complex logic

2. **Write Tests**
   - Add unit tests for new functions
   - Update tests for modified functions
   - Aim for >80% code coverage
   - Run tests before submitting: `pytest`

3. **Commit Messages**
   ```
   type(scope): subject
   
   body (optional)
   footer (optional)
   ```
   
   Types: feat, fix, docs, style, refactor, perf, test, chore
   
   Example:
   ```
   feat(verification): add sentiment analysis
   
   - Add sentiment analysis to content evaluation
   - Update credibility scoring with sentiment
   
   Closes #123
   ```

4. **Keep Commits Clean**
   - One logical change per commit
   - Don't include unrelated changes
   - Rebase if needed: `git rebase -i origin/main`

#### Creating Pull Request

1. Push to your fork: `git push origin feature/your-feature-name`
2. Create PR with detailed description:
   - What changes were made
   - Why these changes were needed
   - How to test the changes
   - Related issues

3. PR Title Format:
   ```
   [type] Brief description
   ```
   Example: `[feat] Add multi-language support to NLP processor`

4. Link related issues:
   ```
   Closes #123
   Related to #456
   ```

#### Code Review

- Respond to feedback promptly
- Make requested changes in new commits
- Request re-review after changes
- Be respectful and professional

## Development Workflow

### Setup Development Environment

```bash
# Clone and navigate
git clone https://github.com/yourusername/TrueLine-News.git
cd TrueLine-News

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
cd backend
pip install -r requirements.txt
pip install pytest pytest-flask black flake8

# Start MongoDB
mongod

# Run backend
python -m flask run
```

### Testing Checklist

Before submitting PR:

- [ ] Code follows style guide
- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black app/`
- [ ] No linting errors: `flake8 app/`
- [ ] Documentation is updated
- [ ] Commits are clean and well-documented

### Code Style Guide

#### Python (Backend)

```python
# Use type hints
def verify_article(url: str, depth: str = "standard") -> dict:
    """Verify article authenticity.
    
    Args:
        url: Article URL to verify
        depth: Verification depth level
        
    Returns:
        Credibility assessment dictionary
    """
    pass

# Use meaningful names
verified_sources = []  # Good
vs = []  # Bad

# Comment complex logic
# Calculate weighted credibility score based on multiple factors
credibility = (
    source_reliability * 0.4 +
    content_consistency * 0.3 +
    spread_pattern * 0.2 +
    original_reporting * 0.1
)

# Keep functions focused
# Good: Single responsibility
def extract_keywords(text: str) -> list:
    """Extract keywords from text."""
    pass

# Bad: Multiple responsibilities
def process_text(text: str):
    """Process text for analysis."""
    keywords = extract(text)
    sentiment = analyze_sentiment(text)
    clean = remove_stopwords(text)
    return keywords, sentiment, clean
```

#### JavaScript (Frontend)

```javascript
// Use meaningful names
const verificationResult = {};  // Good
const vr = {};  // Bad

// Use const/let (not var)
const API_URL = 'http://localhost:5000/api';  // Good
var apiUrl = 'http://localhost:5000/api';    // Bad

// Comment complex logic
// Calculate credibility score from multiple factors
const score = (source * 0.4) + (content * 0.3) + (spread * 0.2);

// Use arrow functions
const verifyNews = async (query) => {  // Good
  return await fetch('/api/verify', { body: JSON.stringify({query}) });
};

// Use async/await over callbacks
// Good
const data = await fetchData();
console.log(data);

// Bad
fetchData().then(data => {
  console.log(data);
});
```

## Documentation

### Docstrings (Python)

Use Google-style docstrings:

```python
def calculate_credibility_score(sources: list, content_similarity: float) -> float:
    """Calculate credibility score based on multiple factors.
    
    Determines overall news authenticity by analyzing source reliability,
    content consistency, and spread patterns.
    
    Args:
        sources (list): List of reporting sources with trustworthiness scores.
        content_similarity (float): Similarity score between articles (0-1).
        
    Returns:
        float: Credibility score between 0 and 1.
        
    Raises:
        ValueError: If sources list is empty.
        TypeError: If content_similarity is not a float.
        
    Example:
        >>> score = calculate_credibility_score(
        ...     sources=[('BBC', 0.98), ('Reuters', 0.97)],
        ...     content_similarity=0.85
        ... )
        >>> print(score)
        0.876
    """
    if not sources:
        raise ValueError("Sources list cannot be empty")
    
    # Implementation here
    return score
```

### Comments

- Use comments to explain WHY, not WHAT
- Keep comments up-to-date with code
- Use clear, concise language

```python
# Good: Explains the reason
# MongoDB's TTL index automatically deletes documents after 30 days
# to prevent verification logs from consuming unlimited storage
db.verification_logs.create_index("timestamp", expireAfterSeconds=2592000)

# Bad: States what the code does
# Create an index on timestamp
db.verification_logs.create_index("timestamp", expireAfterSeconds=2592000)
```

## Testing Guidelines

### Unit Tests

```python
import pytest
from app.utils.nlp_processor import NLPProcessor

class TestNLPProcessor:
    """Test suite for NLP processor."""
    
    @pytest.fixture
    def processor(self):
        """Fixture for NLP processor instance."""
        return NLPProcessor()
    
    def test_extract_keywords_basic(self, processor):
        """Test basic keyword extraction."""
        text = "This is a test article about politics and elections"
        keywords = processor.extract_keywords(text)
        
        assert isinstance(keywords, list)
        assert "politics" in keywords
        assert "elections" in keywords
    
    def test_extract_keywords_empty(self, processor):
        """Test keyword extraction with empty text."""
        keywords = processor.extract_keywords("")
        assert keywords == []
    
    def test_sentiment_analysis(self, processor):
        """Test sentiment analysis."""
        positive_text = "This is amazing and wonderful news!"
        negative_text = "This is terrible and awful news."
        
        pos_score = processor.analyze_sentiment(positive_text)
        neg_score = processor.analyze_sentiment(negative_text)
        
        assert pos_score > 0
        assert neg_score < 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_nlp_processor.py

# Run specific test
pytest tests/test_nlp_processor.py::TestNLPProcessor::test_extract_keywords

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v

# Run with markers
pytest -m "not slow"
```

## Release Process

### Version Numbering

Use Semantic Versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Update documentation
- [ ] Run full test suite
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] Update deployment

## Getting Help

### Resources

- **Documentation**: See `/docs` folder
- **Issues**: Search existing issues first
- **Discussions**: GitHub Discussions tab
- **Email**: support@trueline-news.com

### Communication

- Be respectful and professional
- Provide context and details
- Include error messages and logs
- Follow up on discussions

## Recognition

Contributors will be recognized:
- In CONTRIBUTORS.md file
- In release notes for major contributions
- In project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask! Create an issue or reach out to maintainers.

---

**Thank you for contributing to TrueLine News!** 🎉

Your efforts help make verified information more accessible and combat misinformation.
