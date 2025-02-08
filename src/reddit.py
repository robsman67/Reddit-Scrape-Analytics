import praw
from variable import client_secret, password, user_agent, username, cliend_id
import datetime


class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=cliend_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )
        self.list_ids_post = []

    def get_comments(self, submission_id: str, limit: int = 10) -> list:
        submission = self.reddit.submission(id=submission_id)
        submission.comment_limit = limit
        submission.comments.replace_more(limit=None)
        submission.comment_sort = "top"
        return submission.comments.list()

    def scrape_subreddits(self, list_subreddit_news, list_subreddit_trade, start_date: str):
        list_subreddit_all = [list_subreddit_news, list_subreddit_trade]
        start_timestamp = datetime.datetime.strptime(start_date, '%d-%m-%y %H:%M:%S').timestamp()

        for list_subreddit in list_subreddit_all:
            save_in = "news" if list_subreddit == list_subreddit_news else "trade"

            for subreddit_name in list_subreddit:
                # Go through top, new and hot posts
                subreddit = self.reddit.subreddit(subreddit_name)
                list_posts = [subreddit.new(limit=000), subreddit.top(limit=1000), subreddit.hot(limit=0000)]

                for posts in list_posts:
                    for post in posts:
                        if post.created_utc > start_timestamp and post.id not in self.list_ids_post:
                            self.list_ids_post.append(post.id)
                            self.save_post_and_comments(post, subreddit_name, save_in)

        print("**********")

    def save_post_and_comments(self, post, subreddit_name, save_in):
        # Get comments (max 500 because of Reddit API limit)
        list_comments = self.get_comments(post.id, 100)
        ids = [comment.id for comment in list_comments]

        with open(f'file/' + save_in + '/' + subreddit_name, 'a', newline='', encoding='utf-8') as file:
            file.write(f"Title: {post.title}\n")
            file.write(f"{post.score}\n")

            if len(ids) == 0:
                file.write("\n")
            else:
                for comment_id in ids:
                    comment = self.reddit.comment(id=comment_id)
                    cleaned_comment = comment.body.replace("\n", ".")
                    score = comment.score
                    file.write(f"{cleaned_comment}\n")
                    file.write(f"{score}\n")
            print("save")

    # Count the number of post and comment
    def count_number_post_comment(self, list_subreddit_news, list_subreddit_trade):
        count_news_post = 0
        count_trade_post = 0
        count_trade_comment = 0
        count_news_comment = 0

        # In news
        for news in list_subreddit_news:
            with open(f'file/news/' + news, 'r', newline='', encoding='utf-8') as file:
                # read line by line
                for line in file:
                    if line.startswith("Title:"):
                        count_news_post += 1
                    elif line == "\n":
                        pass
                    elif line.isdigit():
                        pass
                    else:
                        count_news_comment += 1

        # In trade
        for trade in list_subreddit_trade:
            with open(f'file/trade/' + trade, 'r', newline='', encoding='utf-8') as file:
                for line in file:
                    if line.startswith("Title:"):
                        count_trade_post += 1
                    elif line == "\n":
                        pass
                    elif line.isdigit():
                        count_trade_comment += 1
                    else:
                        count_trade_comment += 1

        list_count = [count_news_post, count_news_comment, count_trade_post, count_trade_comment]

        return list_count
