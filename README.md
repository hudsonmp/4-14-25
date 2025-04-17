# Vibe Coding Project Finder

A smart application that helps developers find weekend vibe coding project ideas by analyzing posts from programming subreddits. The application uses vector embeddings and semantic search to recommend personalized project ideas based on user interests.

## Configuration System

The project uses a centralized configuration system in `config.py` to manage all application settings. This approach provides several benefits:

- Centralized management of all application settings
- Easy environment variable handling
- Flexible configuration for different deployment scenarios
- Clear documentation of available settings

### Environment Variables

The application uses the following environment variables (stored in `.env`):

```env
# Reddit API credentials
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

# Pinecone configuration (to be implemented)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# OpenAI configuration (to be implemented)
OPENAI_API_KEY=your_openai_api_key
```

### Configuration Sections

#### 1. Reddit API Configuration
- Manages Reddit API credentials and authentication
- Defines target subreddits for project idea scraping
- Controls rate limiting and data refresh intervals

#### 2. Pinecone Vector Database
- Configures vector storage and similarity search
- Sets up index name and embedding dimensions
- Manages connection settings and environment

#### 3. OpenAI Integration
- Controls API access and model selection
- Manages rate limiting for API calls
- Configures model-specific parameters

#### 4. Application Settings
- Controls Flask server configuration
- Manages debug mode and port settings
- Sets up logging and error handling

#### 5. Vector Search Settings
The application implements a sophisticated similarity search system with the following features:

##### Base Threshold Configuration
- `BASE_SIMILARITY_THRESHOLD`: Default starting point (0.75)
- `MIN_SIMILARITY_THRESHOLD`: Lower bound (0.65)
- `MAX_SIMILARITY_THRESHOLD`: Upper bound (0.85)

##### Dynamic Threshold Adjustment
The system automatically adjusts similarity thresholds based on:

1. **Query Specificity**
   - Longer, more detailed queries increase the threshold
   - `QUERY_LENGTH_THRESHOLD`: 50 characters
   - `SPECIFICITY_BOOST`: 0.05 per threshold increase

2. **Interest Diversity**
   - More interest categories lower the threshold
   - `MAX_INTEREST_CATEGORIES`: 5
   - `INTEREST_DIVERSITY_BOOST`: 0.03 per category

3. **Result Modes**
   - `RESULT_MODE_FIXED`: Return exactly N results
   - `RESULT_MODE_THRESHOLD`: Return all results above threshold
   - Configurable result counts with min/max bounds

## Reddit Scraping Service

The application uses a dedicated Reddit Scraping Service to collect project ideas from programming subreddits. This service leverages the PRAW (Python Reddit API Wrapper) library to interact with the Reddit API in a responsible and efficient way.

### Service Features

- **Multi-subreddit Scraping**: Collects posts from multiple subreddits in a single operation
- **Data Processing**: Cleans and standardizes post data for embedding and storage
- **Scheduled Refreshes**: Automatically refreshes data at configurable intervals
- **Rate Limit Handling**: Respects Reddit API rate limits to avoid throttling

### Targeted Subreddits

The service is configured to scrape the following programming and project-focused subreddits:
- r/SideProject
- r/learnprogramming
- r/vibecoding
- r/ChatGPTCoding
- r/webdev

### Setting Up Reddit API Credentials

To use the Reddit Scraping Service, you need to create a Reddit API application:

1. **Create a Reddit Account**: If you don't already have one, sign up at [reddit.com](https://www.reddit.com)

2. **Create a Reddit API Application**:
   - Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App" at the bottom
   - Fill in the details:
     - **Name**: VibeCodeProjectFinder (or any name you prefer)
     - **App Type**: Choose "script"
     - **Description**: App to find vibe coding project ideas
     - **About URL**: (Optional) Your GitHub repository URL
     - **Redirect URI**: http://localhost:8000/reddit_callback (not actually used for script apps)
   - Click "Create App"

3. **Get Your Credentials**:
   - After creating the app, note down the following:
     - **Client ID**: The string under "personal use script"
     - **Client Secret**: The string labeled "secret"

4. **Configure Environment Variables**:
   - Add the credentials to your `.env` file:
     ```
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_CLIENT_SECRET=your_client_secret
     REDDIT_USER_AGENT=VibeCodeProjectFinder/1.0 by YourUsername
     ```
   - Optionally, add username and password for script authentication (if needed):
     ```
     REDDIT_USERNAME=your_reddit_username
     REDDIT_PASSWORD=your_reddit_password
     ```

### Authentication Methods

The service supports two authentication methods:

1. **Read-only Authentication** (Recommended for this application)
   - Only requires `client_id`, `client_secret`, and `user_agent`
   - Limited to read-only operations (which is all we need for scraping)
   - No need to expose your Reddit account credentials

2. **Script Authentication**
   - Requires additional `username` and `password`
   - Allows both read and write operations
   - Higher rate limits in some cases
   - Only use if additional functionality is needed beyond scraping

### Best Practices for Reddit API Usage

The service follows these best practices:

1. **Respect Rate Limits**: Reddit limits API calls to 60 requests per minute
2. **Use Appropriate User-Agent**: Always use a descriptive user-agent string
3. **Implement Exponential Backoff**: Gradually increase delays between retries on failures
4. **Cache Results**: Store scraped data to minimize API calls
5. **Schedule Off-peak Refreshes**: Run batch operations during off-peak hours

### Implementation Approach

The configuration system follows these principles:

1. **Separation of Concerns**
   - Environment variables are loaded once at startup
   - Configuration values are accessed through constants
   - Service-specific settings are grouped logically

2. **Flexibility**
   - All settings can be overridden through environment variables
   - Default values are provided for development
   - Production settings can be configured separately

3. **Maintainability**
   - Clear documentation of each setting
   - Logical grouping of related settings
   - Easy to add new configuration options

4. **Security**
   - Sensitive credentials are stored in environment variables
   - No hardcoded secrets in configuration files
   - Clear separation of development and production settings

### Best Practices

1. **Environment Variables**
   - Always use environment variables for sensitive data
   - Provide default values for development
   - Document all required environment variables

2. **Configuration Updates**
   - Update documentation when adding new settings
   - Consider backward compatibility
   - Test configuration changes in development

3. **Error Handling**
   - Validate configuration values at startup
   - Provide clear error messages for missing settings
   - Log configuration changes for debugging

4. **Performance**
   - Load configuration once at startup
   - Cache frequently accessed values
   - Minimize environment variable access

## Development Setup

1. Clone the repository
2. Create a `.env` file with required environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python backend/app.py`

## Contributing

When adding new features that require configuration:

1. Add new settings to `config.py`
2. Document the settings in this README
3. Update the `.env.example` file
4. Test the configuration in development
5. Submit a pull request with changes
