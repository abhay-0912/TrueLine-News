"""
Routes module initialization
"""

from app.routes.articles import articles_bp
from app.routes.verification import verification_bp

__all__ = ['articles_bp', 'verification_bp']
