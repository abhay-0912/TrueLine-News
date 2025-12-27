"""
TrueLine News - Backend Flask Application
Main entry point for the news verification API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for frontend communication
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure MongoDB connection
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('MONGODB_DB', 'trueline_news'),
    'host': os.getenv('MONGODB_HOST', 'localhost'),
    'port': int(os.getenv('MONGODB_PORT', 27017)),
    'username': os.getenv('MONGODB_USER'),
    'password': os.getenv('MONGODB_PASSWORD'),
}

# Initialize database
db = MongoEngine(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routes
from app.routes import articles_bp, verification_bp

# Register blueprints
app.register_blueprint(articles_bp)
app.register_blueprint(verification_bp)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'TrueLine News API is running'}), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG', False),
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )
