import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Preprocessing function for text
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token.isalnum()]  # Keep only alphanumeric words
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


# Sentiment analysis function with score inversion for negative votes
def get_sentiment(text, votes):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sentiment_score = scores['compound']

    # Invert the score if the vote is negative
    if votes < 0:
        sentiment_score = sentiment_score - 2 * sentiment_score

    return sentiment_score


def sentiment_analysis(list_subreddit_news, list_subreddit_trade):
    list_subreddit_all = [list_subreddit_news, list_subreddit_trade]

    for list_subreddit in list_subreddit_all:
        print(list_subreddit)
        save_in = "news" if list_subreddit == list_subreddit_news else "trade"

        for subreddit_name in list_subreddit:
            print(subreddit_name)

            # Read the CSV file line by line
            with open('file/' + save_in + '/' + subreddit_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Variables to store the results
            posts_data = []
            current_post = None
            comments = []

            # Iterate through the lines in the file
            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace and newlines

                if line.startswith("Title:"):
                    # If a new line starts with "Title", it means we are starting a new post
                    if current_post:
                        # Save the previous post to the list before processing a new one
                        current_post['comments'] = comments
                        posts_data.append(current_post)

                    # Initialize a new post
                    current_post = {'title': line.replace("Title:", "").strip(), 'votes': 0, 'comments': []}
                    comments = []

                elif line.isdigit():
                    # If the line is a number, it is the vote count for the title or a comment
                    if not current_post['votes']:
                        # If the title vote count has not been set yet
                        current_post['votes'] = int(line)
                    else:
                        # Otherwise, it is the vote count for a comment
                        comments[-1]['votes'] = int(line)

                elif line:
                    # If the line is neither a title nor a number, it's a comment
                    comments.append({'text': line, 'votes': 0})

            # Add the last post if necessary
            if current_post:
                current_post['comments'] = comments
                posts_data.append(current_post)

            # Sentiment analysis and DataFrame creation
            post_titles = []
            post_scores = []

            for post in posts_data:
                # Sentiment analysis for the title
                processed_title = preprocess_text(post['title'])
                title_sentiment = get_sentiment(processed_title, post['votes'])

                # Ensure that the preprocessed and analyzed text is not empty
                print(f"Processed Title: {processed_title}, Sentiment: {title_sentiment}")

                # Sentiment analysis for the comments
                comment_sentiments = []
                total_comment_votes = 0

                for comment in post['comments']:
                    processed_comment = preprocess_text(comment['text'])
                    comment_sentiment = get_sentiment(processed_comment, comment['votes'])
                    comment_sentiments.append(comment_sentiment * comment['votes'])  # Weight by the number of votes
                    total_comment_votes += comment['votes']

                # Calculate the weighted average sentiment of the comments
                if comment_sentiments and total_comment_votes > 0:
                    avg_sentiment = sum(comment_sentiments) / total_comment_votes
                else:
                    avg_sentiment = 0  # No comments, so set to 0

                # Store the results
                post_titles.append(post['title'])

                # Add the "Score" section with title sentiment, title votes, average comment sentiment, and comment votes
                post_scores.append(f"Score: {title_sentiment}, {post['votes']}, {avg_sentiment}, {total_comment_votes}")

            # Create a Pandas DataFrame with the "Score:" section
            df = pd.DataFrame({
                'Title': post_titles,
                'Score': post_scores  # Score with the requested values
            })

            # Save to a CSV file
            save_in_two = "analyse_news" if save_in == "news" else "analyse_trade"
            df.to_csv('file/' + save_in_two + '/analyse_' + subreddit_name + '.csv', index=False)

