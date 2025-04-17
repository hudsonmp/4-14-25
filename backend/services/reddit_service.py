def scrape_subreddits(subreddits, limit=100):
    """
    Scrape posts from multiple subreddits using PRAW.
    
    This function connects to the Reddit API and retrieves posts from the specified subreddits.
    It fetches a maximum number of posts defined by the limit parameter from each subreddit.
    
    Args:
        subreddits (list): A list of subreddit names (without the 'r/' prefix) to scrape.
            Example: ["SideProject", "learnprogramming"]
        limit (int, optional): Maximum number of posts to retrieve from each subreddit.
            Defaults to 100.
    
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
        >>> subreddits = ["SideProject", "learnprogramming"]
        >>> posts = scrape_subreddits(subreddits, limit=50)
        >>> len(posts)
        100  # 50 posts from each of the 2 subreddits
    
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
    
    The default schedule is to refresh the data every other day, but this can be
    configured through environment variables or configuration files.
    
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
