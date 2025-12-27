"""
Routes for article management
"""

from flask import Blueprint, request, jsonify
from app.models import Article, TrustedSource
import logging

articles_bp = Blueprint('articles', __name__, url_prefix='/api/articles')
logger = logging.getLogger(__name__)

@articles_bp.route('', methods=['GET'])
def get_articles():
    """
    Get all verified articles with optional filtering
    Query parameters:
    - limit: Number of articles to return (default: 20)
    - offset: Pagination offset (default: 0)
    - source: Filter by source
    - status: Filter by status (verified, pending, unverified)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        source = request.args.get('source', None)
        status = request.args.get('status', 'verified')
        
        # Build query
        query = Article.objects
        
        if status:
            query = query.filter(status=status)
        
        if source:
            query = query.filter(source=source)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        articles = query.order_by('-verified_date').skip(offset).limit(limit)
        
        return jsonify({
            'total': total,
            'limit': limit,
            'offset': offset,
            'articles': [article.to_dict() for article in articles]
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving articles: {e}")
        return jsonify({'error': 'Failed to retrieve articles'}), 500

@articles_bp.route('/<article_id>', methods=['GET'])
def get_article(article_id):
    """
    Get a specific article by ID
    """
    try:
        article = Article.objects(id=article_id).first()
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        return jsonify(article.to_dict()), 200
    
    except Exception as e:
        logger.error(f"Error retrieving article: {e}")
        return jsonify({'error': 'Failed to retrieve article'}), 500

@articles_bp.route('', methods=['POST'])
def create_article():
    """
    Create a new article (admin only)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'url', 'content', 'source']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if article already exists
        if Article.objects(url=data['url']).first():
            return jsonify({'error': 'Article already exists'}), 409
        
        # Create new article
        article = Article(
            title=data['title'],
            url=data['url'],
            content=data['content'],
            excerpt=data.get('excerpt', ''),
            source=data['source'],
            author=data.get('author', ''),
            keywords=data.get('keywords', []),
            reporting_sources=data.get('reporting_sources', []),
            status=data.get('status', 'pending')
        )
        
        article.save()
        
        logger.info(f"Article created: {article.id}")
        return jsonify(article.to_dict()), 201
    
    except Exception as e:
        logger.error(f"Error creating article: {e}")
        return jsonify({'error': 'Failed to create article'}), 500

@articles_bp.route('/<article_id>', methods=['PUT'])
def update_article(article_id):
    """
    Update an existing article
    """
    try:
        article = Article.objects(id=article_id).first()
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = ['title', 'excerpt', 'content', 'credibility_score', 
                          'verified_sources', 'is_original', 'is_verified', 
                          'cross_checked', 'status', 'sentiment_score']
        
        for field in updatable_fields:
            if field in data:
                setattr(article, field, data[field])
        
        article.save()
        
        logger.info(f"Article updated: {article.id}")
        return jsonify(article.to_dict()), 200
    
    except Exception as e:
        logger.error(f"Error updating article: {e}")
        return jsonify({'error': 'Failed to update article'}), 500

@articles_bp.route('/sources', methods=['GET'])
def get_trusted_sources():
    """
    Get all trusted sources
    """
    try:
        sources = TrustedSource.objects.filter(is_active=True)
        
        return jsonify({
            'total': sources.count(),
            'sources': [source.to_dict() for source in sources]
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving sources: {e}")
        return jsonify({'error': 'Failed to retrieve sources'}), 500
