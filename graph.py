import os
import pandas as pd
import matplotlib.pyplot as plt

# Extract the scores from the "Score" column
def extract_scores(score_str):
    score_str = score_str.replace("Score: ", "")
    scores = score_str.split(", ")
    return float(scores[0]), int(scores[1]), float(scores[2]), int(scores[3])

# Create a boxplot with the given data
def create_boxplot(subreddit_names, sentiment_data, chart_title, y_label, output_path, whis=1.5):
    fig, ax = plt.subplots()

    # Create the boxplot
    ax.boxplot(sentiment_data, tick_labels=subreddit_names, showmeans=True, whis=whis)

    # Add labels and title
    ax.set_ylabel(y_label)
    ax.set_title(chart_title)
    ax.set_ylim([-1, 1])  # Grade between -1 and 1
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# Function to process and plot boxplots for a given category
def process_and_plot_boxplots(csv_directory, output_directory, category_name, whis=2.0):
    os.makedirs(output_directory, exist_ok=True)

    subreddit_names = []
    title_sentiments_data = []
    comment_sentiments_data = []

    # Get all the CSV files in the directory
    for csv_file in os.listdir(csv_directory):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_directory, csv_file)
            df = pd.read_csv(csv_path)

            df[['Title Sentiment', 'Title Votes', 'Average Comment Sentiment', 'Comment Votes']] = df['Score'].apply(lambda x: pd.Series(extract_scores(x)))

            # Get the subreddit information
            subreddit_name = csv_file.replace('analyse_', '').replace('.csv', '')
            subreddit_names.append(subreddit_name)

            title_sentiments_data.append(df['Title Sentiment'].values)
            comment_sentiments_data.append(df['Average Comment Sentiment'].values)

    # Create the boxplot for the titles
    title_output_path = os.path.join(output_directory, f"{category_name}_titles_boxplot.png")
    create_boxplot(subreddit_names, title_sentiments_data, f"Sentiment des titres - {category_name}", 'Sentiment', title_output_path, whis)

    # Create the boxplot for the comments
    comment_output_path = os.path.join(output_directory, f"{category_name}_comments_boxplot.png")
    create_boxplot(subreddit_names, comment_sentiments_data, f"Sentiment des commentaires - {category_name}", 'Sentiment', comment_output_path, whis)
