"""
Routes for news verification
"""

from flask import Blueprint, request, jsonify
from app.services.verification_service import VerificationService
from app.models import VerificationLog
import logging

verification_bp = Blueprint('verification', __name__, url_prefix='/api/verify')
logger = logging.getLogger(__name__)
verification_service = VerificationService()

@verification_bp.route('', methods=['POST'])
def verify_news():
    """
    Verify a news story
    Request body:
    {
        "query": "news headline or URL to verify",
        "depth": "basic|standard|deep" (optional, default: standard)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query'].strip()
        depth = data.get('depth', 'standard')
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Perform verification
        result = verification_service.verify(query, depth)
        
        # Log verification attempt
        try:
            log = VerificationLog(
                query=query,
                credibility_score=result.get('credibility_score'),
                verified_sources=result.get('verified_sources'),
                is_verified=result.get('is_verified'),
                is_original=result.get('is_original'),
                found_sources=result.get('sources', [])
            )
            log.save()
        except Exception as e:
            logger.warning(f"Failed to log verification: {e}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error verifying news: {e}")
        return jsonify({'error': 'Verification failed'}), 500

@verification_bp.route('/analyze-credibility', methods=['POST'])
def analyze_credibility():
    """
    Deep credibility analysis of a news story
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        # Perform deep analysis
        result = verification_service.analyze_credibility(url)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error analyzing credibility: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

@verification_bp.route('/compare-sources', methods=['POST'])
def compare_sources():
    """
    Compare multiple news sources reporting the same story
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data or not isinstance(data['urls'], list):
            return jsonify({'error': 'List of URLs is required'}), 400
        
        urls = data['urls']
        
        if len(urls) < 2:
            return jsonify({'error': 'At least 2 URLs are required for comparison'}), 400
        
        # Perform comparison
        result = verification_service.compare_sources(urls)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error comparing sources: {e}")
        return jsonify({'error': 'Comparison failed'}), 500

@verification_bp.route('/history', methods=['GET'])
def verification_history():
    """
    Get verification history
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        logs = VerificationLog.objects.order_by('-timestamp').limit(limit)
        
        return jsonify({
            'total': len(logs),
            'logs': [
                {
                    'query': log.query,
                    'credibility_score': log.credibility_score,
                    'is_verified': log.is_verified,
                    'timestamp': log.timestamp.isoformat()
                }
                for log in logs
            ]
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving verification history: {e}")
        return jsonify({'error': 'Failed to retrieve history'}), 500
