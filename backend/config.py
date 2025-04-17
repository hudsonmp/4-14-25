import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Using Path ensures cross-platform compatibility
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Reddit API Configuration
# These credentials are required for PRAW to authenticate with Reddit's API
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# List of subreddits to scrape
# These communities were chosen for their relevance to programming projects
SUBREDDITS = [
    'SideProject',
    'learnprogramming',
    'vibecoding',
    'ChatGPTCoding',
    'webdev'
]

# Pinecone Configuration (to be implemented)
# These will be used for vector storage and similarity search
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = 'vibe-coding-projects'  # Name for your Pinecone index
PINECONE_DIMENSION = 384  # Dimension for llama-text-embed-v2 embeddings

# OpenAI Configuration (to be implemented)
# Required for project metadata extraction and plan generation
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = 'o4-mini'  # Default model for generating implementation plans

# Flask Application Settings
DEBUG = os.getenv('FLASK_DEBUG', True)  # Enable debug mode by default
PORT = int(os.getenv('PORT', 5000))     # Default port for Flask server

# Data Refresh Settings
REFRESH_INTERVAL_HOURS = 48  # Refresh Reddit data every 48 hours
MAX_POSTS_PER_SUBREDDIT = 50  # Maximum number of posts to fetch per subreddit

# Vector Search Settings
# Base similarity threshold - can be overridden by dynamic adjustment
BASE_SIMILARITY_THRESHOLD = 0.75

# Dynamic threshold adjustment ranges
MIN_SIMILARITY_THRESHOLD = 0.65  # Minimum allowed threshold
MAX_SIMILARITY_THRESHOLD = 0.85  # Maximum allowed threshold

# Query specificity thresholds
QUERY_LENGTH_THRESHOLD = 50  # Characters above which a query is considered detailed
SPECIFICITY_BOOST = 0.05     # How much to increase threshold for detailed queries

# Interest category thresholds
MAX_INTEREST_CATEGORIES = 5  # Maximum number of interest categories to consider
INTEREST_DIVERSITY_BOOST = 0.03  # How much to decrease threshold per additional interest

# Result count settings
DEFAULT_MAX_RECOMMENDATIONS = 10
MIN_RECOMMENDATIONS = 5
MAX_RECOMMENDATIONS = 20

# Result mode settings
RESULT_MODE_FIXED = 'fixed'      # Return exactly N results
RESULT_MODE_THRESHOLD = 'threshold'  # Return all results above threshold
DEFAULT_RESULT_MODE = RESULT_MODE_FIXED

# API Rate Limiting
REDDIT_RATE_LIMIT = 60  # Maximum requests per minute to Reddit API
OPENAI_RATE_LIMIT = 20  # Maximum requests per minute to OpenAI API
