import praw
from variable import cliend_id, client_secret, password, user_agent, username

# Create a new instance of Reddit praw
reddit = praw.Reddit(
    client_id=cliend_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
)
print(reddit.user.me())



subreddit = reddit.subreddit("python")
print("Logged in")

#Post of a subredit
top_posts = subreddit.top(limit=1)
new_posts = subreddit.new(limit=1)
hot_posts = subreddit.hot(limit=1)
print(new_posts)

for post in top_posts:
    print(post.title)
    print(post.url)
    print(post.id)


#Comment from one post with his id
post = reddit.submission(id="g53lxf")

comments = post.comments

for comment in comments:
    print("**********")
    print(comment.body)
    print(comment.author)
    print(comment.score)
    print(comment.created_utc)