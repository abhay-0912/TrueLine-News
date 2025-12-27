"""
Core verification service for TrueLine News
Handles news validation, source analysis, and credibility scoring
"""

from app.utils.nlp_processor import NLPProcessor
from app.utils.web_scraper import WebScraper
from app.utils.credibility_analyzer import CredibilityAnalyzer
from app.models import Article, TrustedSource
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VerificationService:
    """
    Main service for news verification and credibility analysis
    """
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.web_scraper = WebScraper()
        self.credibility_analyzer = CredibilityAnalyzer()
    
    def verify(self, query, depth='standard'):
        """
        Verify a news story and return credibility assessment
        
        Args:
            query (str): News headline or URL to verify
            depth (str): Verification depth - basic, standard, or deep
        
        Returns:
            dict: Verification result with credibility score and details
        """
        try:
            # Search for matching articles
            matching_articles = self._find_matching_articles(query)
            
            # If query is a URL, scrape and analyze it
            if query.startswith('http'):
                content = self.web_scraper.scrape(query)
                if content:
                    matching_articles.append({'url': query, 'content': content})
            
            if not matching_articles:
                return {
                    'is_verified': False,
                    'credibility_score': 0.0,
                    'verified_sources': 0,
                    'is_original': False,
                    'status': 'No matching articles found',
                    'sources': []
                }
            
            # Extract key information from query
            keywords = self.nlp_processor.extract_keywords(query)
            
            # Find reporting sources
            sources = self._find_reporting_sources(matching_articles, keywords)
            
            # Analyze source trustworthiness
            source_reliability = self._analyze_source_reliability(sources)
            
            # Calculate credibility score
            credibility_score = self.credibility_analyzer.calculate_score(
                num_sources=len(sources),
                source_reliability=source_reliability,
                content_consistency=self._check_content_consistency(matching_articles),
                spread_pattern=self._analyze_spread_pattern(matching_articles)
            )
            
            # Determine if original reporting
            is_original = self._is_original_reporting(matching_articles)
            
            # Final verification decision
            is_verified = credibility_score >= 0.6 and len(sources) > 1
            
            return {
                'is_verified': is_verified,
                'credibility_score': credibility_score,
                'verified_sources': len(sources),
                'is_original': is_original,
                'status': 'verified' if is_verified else 'unverified',
                'sources': sources,
                'keywords': keywords,
                'details': {
                    'source_reliability': source_reliability,
                    'content_consistency': self._check_content_consistency(matching_articles),
                    'spread_pattern_healthy': self._analyze_spread_pattern(matching_articles)
                }
            }
        
        except Exception as e:
            logger.error(f"Verification failed for query '{query}': {e}")
            return {
                'is_verified': False,
                'credibility_score': 0.0,
                'verified_sources': 0,
                'error': str(e)
            }
    
    def analyze_credibility(self, url):
        """
        Deep credibility analysis of a specific article URL
        """
        try:
            # Scrape the article
            content = self.web_scraper.scrape(url)
            if not content:
                return {'error': 'Failed to scrape URL'}
            
            # Analyze sentiment
            sentiment = self.nlp_processor.analyze_sentiment(content)
            
            # Extract keywords
            keywords = self.nlp_processor.extract_keywords(content)
            
            # Find similar articles
            similar_articles = self._find_similar_articles(content, keywords)
            
            # Analyze for manipulated content
            manipulation_score = self._detect_content_manipulation(content)
            
            # Build credibility profile
            credibility_profile = {
                'url': url,
                'sentiment_score': sentiment,
                'keywords': keywords,
                'similar_articles': len(similar_articles),
                'manipulation_score': manipulation_score,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            return credibility_profile
        
        except Exception as e:
            logger.error(f"Credibility analysis failed for {url}: {e}")
            return {'error': str(e)}
    
    def compare_sources(self, urls):
        """
        Compare multiple sources reporting the same story
        """
        try:
            articles = []
            for url in urls:
                content = self.web_scraper.scrape(url)
                if content:
                    articles.append({'url': url, 'content': content})
            
            if not articles:
                return {'error': 'Failed to retrieve articles'}
            
            # Analyze consistency
            consistency = self._check_content_consistency(articles)
            
            # Find common elements
            common_keywords = self._find_common_elements(articles)
            
            # Source reliability
            source_reliability = self._analyze_source_reliability([url for url in urls])
            
            return {
                'compared_sources': len(articles),
                'consistency_score': consistency,
                'common_keywords': common_keywords,
                'source_reliability': source_reliability,
                'verdict': 'Consistent reporting' if consistency > 0.7 else 'Inconsistent reporting'
            }
        
        except Exception as e:
            logger.error(f"Source comparison failed: {e}")
            return {'error': str(e)}
    
    def _find_matching_articles(self, query):
        """Find articles matching the query"""
        try:
            # Search in database
            keywords = self.nlp_processor.extract_keywords(query)
            articles = Article.objects.filter(keywords__in=keywords, status='verified')
            
            return [
                {'url': a.url, 'content': a.content, 'source': a.source}
                for a in articles
            ]
        except Exception as e:
            logger.warning(f"Error finding matching articles: {e}")
            return []
    
    def _find_reporting_sources(self, articles, keywords):
        """Identify all sources reporting the story"""
        sources = set()
        for article in articles:
            if 'source' in article:
                sources.add(article['source'])
        return list(sources)
    
    def _analyze_source_reliability(self, sources):
        """Analyze trustworthiness of reporting sources"""
        reliability_scores = {}
        
        for source in sources:
            try:
                trusted_source = TrustedSource.objects(name=source).first()
                if trusted_source:
                    reliability_scores[source] = trusted_source.trustworthiness_score
                else:
                    reliability_scores[source] = 0.5  # Default neutral score
            except Exception as e:
                logger.warning(f"Error analyzing source {source}: {e}")
                reliability_scores[source] = 0.5
        
        return reliability_scores
    
    def _check_content_consistency(self, articles):
        """Check consistency of content across sources"""
        if len(articles) < 2:
            return 1.0
        
        try:
            # Simple similarity check (can be enhanced with more sophisticated algorithms)
            consistency_scores = []
            for i in range(len(articles) - 1):
                similarity = self.nlp_processor.calculate_similarity(
                    articles[i].get('content', ''),
                    articles[i + 1].get('content', '')
                )
                consistency_scores.append(similarity)
            
            return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.5
        except Exception as e:
            logger.warning(f"Error checking consistency: {e}")
            return 0.5
    
    def _analyze_spread_pattern(self, articles):
        """Analyze how the news spread across sources"""
        # Returns True if spread pattern is healthy (multiple sources)
        return len(articles) > 1
    
    def _is_original_reporting(self, articles):
        """Determine if any source is doing original reporting"""
        # In a real implementation, this would analyze bylines and citations
        return len(articles) > 0
    
    def _find_similar_articles(self, content, keywords):
        """Find articles with similar content"""
        try:
            similar = Article.objects.filter(keywords__in=keywords).limit(10)
            return list(similar)
        except Exception as e:
            logger.warning(f"Error finding similar articles: {e}")
            return []
    
    def _detect_content_manipulation(self, content):
        """Detect signs of content manipulation or sensationalism"""
        # Analyze for clickbait, manipulated facts, etc.
        return 0.0  # Placeholder
    
    def _find_common_elements(self, articles):
        """Find common keywords across articles"""
        all_keywords = []
        for article in articles:
            keywords = self.nlp_processor.extract_keywords(article.get('content', ''))
            all_keywords.extend(keywords)
        
        # Find most common
        from collections import Counter
        common = Counter(all_keywords).most_common(5)
        return [keyword for keyword, _ in common]
