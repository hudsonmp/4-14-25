"""
Reddit Scraping Service for Vibe Coding Project Finder

This module provides functionality to scrape multiple subreddits for project ideas using PRAW
(Python Reddit API Wrapper). It handles the scraping, processing, and scheduling of regular
data refreshes to keep the project database up-to-date.

The service is designed to collect posts from programming and project-related subreddits,
extract relevant information, and prepare the data for embedding and storage in the vector database.

Usage:
    from services.reddit_service import scrape_subreddits, process_posts, schedule_refresh
    
    # Scrape multiple subreddits
    subreddits = ["SideProject", "learnprogramming", "vibecoding", "ChatGPTCoding", "webdev"]
    posts = scrape_subreddits(subreddits)
    
    # Process the posts
    processed_posts = process_posts(posts)
    
    # Schedule regular refresh
    schedule_refresh()
"""

import praw  # Python Reddit API Wrapper for interacting with Reddit's API
import logging  # For logging info, warnings, and errors during scraping
import datetime  # For converting UTC timestamps to readable datetime format
import time  # For implementing rate limit handling and delays
from typing import List, Dict, Any, Optional  # Type hints for better code documentation
from praw.exceptions import PRAWException, APIException, ClientException  # PRAW-specific exceptions

# Import configuration from config file
from ..config import (
    REDDIT_CLIENT_ID,  # OAuth client ID from Reddit API
    REDDIT_CLIENT_SECRET,  # OAuth client secret from Reddit API
    REDDIT_USER_AGENT,  # User agent string for API requests
    SUBREDDITS,  # List of subreddits to scrape
    REDDIT_RATE_LIMIT,  # Maximum requests per minute to Reddit API
    MAX_POSTS_PER_SUBREDDIT,  # Maximum number of posts to fetch per subreddit
    REFRESH_INTERVAL_HOURS,  # Refresh interval in hours
)

# Set up logging for this module
logger = logging.getLogger(__name__)

def initialize_reddit_client() -> praw.Reddit:
    """
    Initialize and return a PRAW Reddit instance.
    
    This function creates a connection to the Reddit API using credentials
    from the config file. It uses read-only authentication since we only
    need to scrape posts and don't need to perform any write operations.
    
    Returns:
        praw.Reddit: Authenticated Reddit instance
        
    Raises:
        PRAWException: If there's an issue with the Reddit API connection
        ClientException: If credentials are invalid
        ValueError: If required credentials are missing
    """
    try:
        # Validate required credentials
        if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
            missing_creds = []
            if not REDDIT_CLIENT_ID:
                missing_creds.append("REDDIT_CLIENT_ID")
            if not REDDIT_CLIENT_SECRET:
                missing_creds.append("REDDIT_CLIENT_SECRET")
            if not REDDIT_USER_AGENT:
                missing_creds.append("REDDIT_USER_AGENT")
            
            error_msg = f"Missing required Reddit credentials: {', '.join(missing_creds)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # Initialize with read-only authentication
        logger.info("Initializing Reddit client with read-only authentication")
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        
        # Verify that the connection works
        logger.info(f"Reddit client initialized. Read-only: {reddit.read_only}")
        return reddit
        
    except (PRAWException, ClientException) as e:
        logger.error(f"Failed to initialize Reddit client: {str(e)}")
        raise

# Create a global Reddit instance to be reused
try:
    reddit_client = initialize_reddit_client()
except Exception as e:
    logger.error(f"Could not initialize Reddit client on module load: {str(e)}")
    reddit_client = None

def scrape_subreddits(subreddits: Optional[List[str]] = None, limit: Optional[int] = None):
    """
    Scrape posts from multiple subreddits using PRAW.
    
    This function connects to the Reddit API and retrieves posts from the specified subreddits.
    It fetches a maximum number of posts defined by the limit parameter from each subreddit.
    
    Args:
        subreddits (list, optional): A list of subreddit names (without the 'r/' prefix) to scrape.
            If None, uses the SUBREDDITS list from config.py.
            Example: ["SideProject", "learnprogramming"]
        limit (int, optional): Maximum number of posts to retrieve from each subreddit.
            If None, uses MAX_POSTS_PER_SUBREDDIT from config.py.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains the raw post data
        with the following keys:
            - id (str): Unique Reddit post ID
            - title (str): Post title
            - selftext (str): Post content text
            - url (str): URL to the post
            - author (str): Username of the post author
            - created_utc (float): UTC timestamp of when the post was created
            - subreddit (str): Subreddit name where the post was published
            - score (int): Post score/upvotes
            - num_comments (int): Number of comments on the post
    
    Example:
        >>> posts = scrape_subreddits()  # Uses default subreddits from config
        >>> posts = scrape_subreddits(["SideProject", "learnprogramming"], limit=50)
    
    Raises:
        praw.exceptions.PRAWException: If there's an issue with the Reddit API connection
        praw.exceptions.ClientException: If there's an issue with the Reddit API client
        praw.exceptions.APIException: If there's an API-specific error
        ValueError: If an invalid subreddit name is provided
    
    Note:
        This function respects Reddit's API rate limits. If you request too many posts
        or make too many requests in a short time, it may take longer to complete.
    """
    pass


def process_posts(posts):
    """
    Process and clean the raw Reddit posts data.
    
    This function takes the raw posts from the scrape_subreddits function and:
    1. Removes deleted or removed posts
    2. Cleans and formats text fields
    3. Extracts relevant information
    4. Standardizes data format
    5. Filters out irrelevant or low-quality posts
    
    Args:
        posts (list): A list of dictionaries containing raw post data as returned by
            the scrape_subreddits function.
    
    Returns:
        list: A list of processed post dictionaries with the following structure:
            - id (str): Unique Reddit post ID
            - title (str): Cleaned post title
            - content (str): Cleaned and combined title and selftext
            - url (str): URL to the post
            - author (str): Username of the post author
            - created_at (str): ISO format datetime when the post was created
            - subreddit (str): Subreddit name
            - score (int): Post score/upvotes
            - comment_count (int): Number of comments
            - is_project (bool): Flag indicating if the post appears to be a project
    
    Example:
        >>> raw_posts = scrape_subreddits(["SideProject"], limit=10)
        >>> processed = process_posts(raw_posts)
        >>> processed[0].keys()
        dict_keys(['id', 'title', 'content', 'url', 'author', 'created_at', 'subreddit', 
                  'score', 'comment_count', 'is_project'])
    
    Raises:
        ValueError: If the input posts list is empty or not in the expected format
        TypeError: If any post in the list is not a dictionary with the expected keys
    
    Note:
        Posts that are [deleted], [removed], or have empty content after cleaning
        will be filtered out from the results.
    """
    pass


def schedule_refresh():
    """
    Schedule a regular job to refresh the Reddit data.
    
    This function sets up a scheduled task that runs periodically to scrape new posts
    from the configured subreddits and update the database. It ensures that the
    project database stays current with fresh project ideas from Reddit.
    
    The refresh interval is configured through REFRESH_INTERVAL_HOURS in config.py,
    which defaults to 48 hours (every other day).
    
    Returns:
        dict: Information about the scheduled job, including:
            - job_id (str): Unique identifier for the scheduled job
            - next_run (str): ISO format datetime of when the job will next run
            - interval (str): Description of the refresh interval
    
    Example:
        >>> job_info = schedule_refresh()
        >>> print(f"Next data refresh scheduled for {job_info['next_run']}")
        Next data refresh scheduled for 2023-05-15T00:00:00Z
    
    Raises:
        SchedulerError: If there's an issue setting up the scheduler
        ConfigError: If there's an issue with the refresh configuration
    
    Note:
        This function requires a scheduler implementation (e.g., APScheduler)
        to be properly configured in the application.
        
        The actual implementation may use different scheduling mechanisms depending
        on the deployment environment (e.g., cron jobs, Celery tasks, etc.).
    """
    pass
