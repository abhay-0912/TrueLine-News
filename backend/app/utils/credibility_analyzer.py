"""
Credibility Analyzer for calculating news authenticity scores
"""

import logging

logger = logging.getLogger(__name__)

class CredibilityAnalyzer:
    """
    Analyzes and scores credibility of news content
    """
    
    def __init__(self):
        self.weights = {
            'source_reliability': 0.4,
            'content_consistency': 0.3,
            'spread_pattern': 0.2,
            'original_reporting': 0.1
        }
    
    def calculate_score(self, num_sources=0, source_reliability=None, 
                       content_consistency=0.5, spread_pattern=False, original_reporting=False):
        """
        Calculate credibility score for a news story
        
        Args:
            num_sources (int): Number of independent sources reporting the story
            source_reliability (dict): Dictionary with source names and reliability scores
            content_consistency (float): Consistency score across sources (0-1)
            spread_pattern (bool): Whether spread pattern indicates legitimate news
            original_reporting (bool): Whether original reporting exists
        
        Returns:
            float: Credibility score between 0 and 1
        """
        try:
            scores = {}
            
            # Source reliability score
            if source_reliability and isinstance(source_reliability, dict):
                avg_reliability = sum(source_reliability.values()) / len(source_reliability)
                # Boost score based on number of sources
                source_score = min(avg_reliability + (num_sources - 1) * 0.1, 1.0)
            else:
                source_score = 0.0 if num_sources < 2 else min(num_sources * 0.2, 1.0)
            
            scores['source_reliability'] = source_score
            
            # Content consistency score
            scores['content_consistency'] = float(content_consistency)
            
            # Spread pattern score
            spread_score = 0.8 if spread_pattern else 0.3
            scores['spread_pattern'] = spread_score
            
            # Original reporting score
            original_score = 0.7 if original_reporting else 0.5
            scores['original_reporting'] = original_score
            
            # Calculate weighted average
            final_score = sum(
                scores.get(key, 0) * weight
                for key, weight in self.weights.items()
            )
            
            return min(max(float(final_score), 0.0), 1.0)
        
        except Exception as e:
            logger.error(f"Error calculating credibility score: {e}")
            return 0.0
    
    def analyze_source_credibility(self, source_name, article_count=0, verification_rate=0.0):
        """
        Analyze credibility of a specific source
        
        Args:
            source_name (str): Name of the source
            article_count (int): Number of articles from this source
            verification_rate (float): Rate of verified articles (0-1)
        
        Returns:
            dict: Detailed credibility analysis
        """
        try:
            # Base credibility factors
            factors = {
                'article_frequency': min(article_count / 100, 1.0),  # Normalized
                'verification_rate': verification_rate,
                'consistency': 0.5  # Placeholder
            }
            
            # Calculate overall score
            overall_score = sum(factors.values()) / len(factors)
            
            return {
                'source': source_name,
                'overall_score': overall_score,
                'factors': factors,
                'assessment': self._get_assessment(overall_score)
            }
        
        except Exception as e:
            logger.error(f"Error analyzing source credibility: {e}")
            return {'source': source_name, 'overall_score': 0.5, 'error': str(e)}
    
    def detect_misinformation_indicators(self, content, sentiment_score=0.0):
        """
        Detect indicators of misinformation in content
        
        Args:
            content (str): Content to analyze
            sentiment_score (float): Sentiment analysis score
        
        Returns:
            dict: List of detected misinformation indicators
        """
        try:
            indicators = {
                'sensational_language': self._check_sensationalism(content),
                'extreme_sentiment': abs(sentiment_score) > 0.8,
                'missing_sources': self._check_missing_citations(content),
                'false_claims': False  # Would require fact-checking service
            }
            
            risk_level = sum(indicators.values()) / len(indicators)
            
            return {
                'indicators': indicators,
                'risk_level': risk_level,
                'recommendation': self._get_misinformation_recommendation(risk_level)
            }
        
        except Exception as e:
            logger.error(f"Error detecting misinformation: {e}")
            return {'error': str(e)}
    
    def _get_assessment(self, score):
        """Get text assessment based on score"""
        if score >= 0.8:
            return "Highly credible"
        elif score >= 0.6:
            return "Credible"
        elif score >= 0.4:
            return "Moderately credible"
        else:
            return "Low credibility"
    
    def _get_misinformation_recommendation(self, risk_level):
        """Get recommendation based on risk level"""
        if risk_level >= 0.7:
            return "High risk - Do not publish"
        elif risk_level >= 0.4:
            return "Medium risk - Requires further verification"
        else:
            return "Low risk - Can be published"
    
    def _check_sensationalism(self, content):
        """Simple check for sensational language"""
        sensational_words = ['shocking', 'amazing', 'unbelievable', 'viral']
        return any(word in content.lower() for word in sensational_words)
    
    def _check_missing_citations(self, content):
        """Check for missing citations or sources"""
        # Placeholder - would need sophisticated NLP
        return 'according to' not in content.lower() and 'sources say' not in content.lower()
