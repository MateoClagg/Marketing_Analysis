import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Define a function to fetch the customer review data from SQL
def fetch_data_from_sql():

    # Define the connection string with parameters for database connection
    connect_str = (
        "Driver={SQL Server};"
        "Server=T-SMD1038553\\SQLEXPRESS;"
        "Database=PortfolioProject_MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )

    # Establish connection to database
    connect = pyodbc.connect(connect_str)   

    # Define the SQL query to fetch customer reviews data
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"

    # Execute the query and fetch the data into a DataFrame
    df = pd.read_sql(query, connect)

    # Close the connection to free up resources
    connect.close()

    # Return the fetched data as a DataFrame
    return df

# Fetch the customer reviews data from the SQL database
customer_reviews_df = fetch_data_from_sql()

# Initiate the VADER sentiment intensity analyzer for text data
sia = SentimentIntensityAnalyzer()

# Define a funciton to calculate sentiment scores using VADER
def calculate_sentiment(review):
    # Get the sentiment scores for the review text
    sentiment = sia.polarity_scores(review)
    
    # Return the compound score, which is a normalized score between -1 and 1
    return sentiment['compound']


# Define a function to categorize sentiment using sentiment score and review rating
def categorize_sentiment(score, rating):

    if score > 0.05:  # Positive sentiment score
        if rating >=4:
            return 'Positive'  # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating and positive ssentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
        
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'  # Low rating and negative sentiment
        elif rating == 3: 
            return 'Mixed Negative'  # Netural rating and negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
        
    else:  # Netural sentiment score
        if rating >=4:  
            return 'Positive'  # High rating and neutral sentiment 
        elif rating == 3:
            return 'Neutral'  # Neutral rating and neutral sentiment
        else:
            return 'Negative'  # Low rating and neutral sentiment
        

# Define a function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif -0.5 < score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment
    

# Apply sentiment analysis to calculate sentiment scores for each review
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text and rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1
)

# Apply sentiment bucketing to categorize scores into defined ranges
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the DataFrame with sentiment scores, categories, and buckets
print(customer_reviews_df.head())

# Save the DataFrame with sentiment scores, categories, 
customer_reviews_df.to_csv('fact_customer_reviews_with_sentiment.csv', index=False)