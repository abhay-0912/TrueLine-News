"""
Database Models for TrueLine News
"""

from mongoengine import Document, StringField, DateTimeField, IntField, FloatField, BooleanField, ListField, DictField
from datetime import datetime

class Article(Document):
    """
    Represents a verified news article
    """
    title = StringField(required=True, max_length=500)
    url = StringField(required=True, unique=True)
    content = StringField(required=True)
    excerpt = StringField(max_length=500)
    source = StringField(required=True)
    author = StringField(max_length=200)
    
    # Verification fields
    credibility_score = FloatField(default=0.0, min_value=0.0, max_value=1.0)
    verified_sources = IntField(default=0)
    is_original = BooleanField(default=False)
    is_verified = BooleanField(default=False)
    cross_checked = BooleanField(default=False)
    
    # Content analysis
    keywords = ListField(StringField())
    sentiment_score = FloatField(min_value=-1.0, max_value=1.0)
    
    # Sourcing information
    reporting_sources = ListField(StringField())
    source_trustworthiness = DictField()
    
    # Metadata
    published_date = DateTimeField()
    verified_date = DateTimeField(default=datetime.utcnow)
    last_updated = DateTimeField(default=datetime.utcnow)
    
    # Status
    status = StringField(choices=['verified', 'pending', 'unverified'], default='pending')
    
    meta = {
        'collection': 'articles',
        'indexes': ['url', 'source', 'verified_date', 'credibility_score']
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'url': self.url,
            'excerpt': self.excerpt,
            'source': self.source,
            'author': self.author,
            'credibility_score': self.credibility_score,
            'verified_sources': self.verified_sources,
            'is_original': self.is_original,
            'is_verified': self.is_verified,
            'cross_checked': self.cross_checked,
            'keywords': self.keywords,
            'sentiment_score': self.sentiment_score,
            'reporting_sources': self.reporting_sources,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'verified_date': self.verified_date.isoformat(),
            'status': self.status
        }

class VerificationLog(Document):
    """
    Logs verification attempts and results
    """
    query = StringField(required=True)
    credibility_score = FloatField()
    verified_sources = IntField()
    is_verified = BooleanField()
    is_original = BooleanField()
    
    # Analysis details
    matching_articles = ListField(StringField())
    found_sources = ListField(StringField())
    
    verification_details = DictField()
    timestamp = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'verification_logs',
        'indexes': ['timestamp', 'query']
    }

class TrustedSource(Document):
    """
    Registry of trusted news sources
    """
    name = StringField(required=True, unique=True)
    url = StringField(required=True)
    description = StringField()
    domain = StringField(required=True, unique=True)
    
    # Trust metrics
    trustworthiness_score = FloatField(default=0.5, min_value=0.0, max_value=1.0)
    article_count = IntField(default=0)
    verification_rate = FloatField(default=0.0)
    
    # Metadata
    category = StringField(choices=['news', 'investigative', 'specialized', 'international'])
    country = StringField()
    language = StringField(default='en')
    
    is_active = BooleanField(default=True)
    added_date = DateTimeField(default=datetime.utcnow)
    last_verified = DateTimeField()
    
    meta = {
        'collection': 'trusted_sources',
        'indexes': ['domain', 'trustworthiness_score', 'is_active']
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'url': self.url,
            'domain': self.domain,
            'trustworthiness_score': self.trustworthiness_score,
            'article_count': self.article_count,
            'verification_rate': self.verification_rate,
            'category': self.category,
            'country': self.country,
            'is_active': self.is_active
        }
