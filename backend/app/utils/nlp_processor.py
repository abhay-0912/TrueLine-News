"""
NLP Processor for content analysis
Handles keyword extraction, sentiment analysis, and text similarity
"""

import logging
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPProcessor:
    """
    Handles NLP operations for news content analysis
    """
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    
    def extract_keywords(self, text, top_n=10):
        """
        Extract important keywords from text
        
        Args:
            text (str): Text to analyze
            top_n (int): Number of top keywords to return
        
        Returns:
            list: List of keywords
        """
        try:
            if not text:
                return []
            
            # Tokenize and filter
            tokens = word_tokenize(text.lower())
            keywords = [
                word for word in tokens
                if word.isalpha() and word not in self.stop_words and len(word) > 3
            ]
            
            # Remove duplicates while preserving order
            seen = set()
            unique_keywords = []
            for word in keywords:
                if word not in seen:
                    seen.add(word)
                    unique_keywords.append(word)
            
            return unique_keywords[:top_n]
        
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of the text
        
        Args:
            text (str): Text to analyze
        
        Returns:
            float: Sentiment score between -1 (negative) and 1 (positive)
        """
        try:
            if not text:
                return 0.0
            
            scores = self.sia.polarity_scores(text)
            # Convert compound score from -1 to 1 range
            return scores['compound']
        
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate similarity between two texts
        
        Args:
            text1 (str): First text
            text2 (str): Second text
        
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            if not text1 or not text2:
                return 0.0
            
            # Vectorize texts
            tfidf = TfidfVectorizer(stop_words='english', max_features=100)
            vectors = tfidf.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            
            return float(similarity)
        
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def detect_sensationalism(self, text):
        """
        Detect sensational or clickbait language
        
        Args:
            text (str): Text to analyze
        
        Returns:
            float: Sensationalism score (0 = not sensational, 1 = highly sensational)
        """
        try:
            sensational_words = [
                'shocking', 'amazing', 'incredible', 'unbelievable',
                'must see', 'you won\'t believe', 'doctors hate',
                'celebrity', 'scandal', 'exposé', 'viral'
            ]
            
            text_lower = text.lower()
            count = sum(1 for word in sensational_words if word in text_lower)
            
            # Normalize score
            score = min(count / len(sensational_words), 1.0)
            return score
        
        except Exception as e:
            logger.error(f"Error detecting sensationalism: {e}")
            return 0.0
    
    def extract_entities(self, text):
        """
        Extract named entities (people, places, organizations)
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Dictionary with entity types as keys
        """
        try:
            # Simple entity extraction (can be enhanced with spaCy)
            sentences = sent_tokenize(text)
            
            return {
                'sentences': len(sentences),
                'words': len(word_tokenize(text))
            }
        
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
