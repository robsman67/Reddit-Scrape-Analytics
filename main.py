import praw
from variable import cliend_id, client_secret, password, user_agent, username
import datetime



# Create a new instance of Reddit praw
reddit = praw.Reddit(
    client_id=cliend_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
)

def get_comments(reddit: reddit, submission_id: str, limit:int = 10) -> list:
    submission = reddit.submission(id=submission_id)
    submission.comment_limit = limit
    submission.comments.replace_more(limit=0)
    submission.comment_sort = "top"
    comments = submission.comments.list()
    return comments


# List of subreddit to scrap
list_subreddit_news = ["Bitcoin"]

#list_subreddit_news = ["Bitcoin", "Ethereum", "CryptoCurrency", "btc"]

# Everything after 2024
start_date = '01-01-24 00:00:00'
start_date = datetime.datetime.strptime(start_date, '%d-%m-%y %H:%M:%S').timestamp()

for a in list_subreddit_news:

    subreddit = reddit.subreddit(a)

    #Post of a subredit
    top_posts = subreddit.top(limit=0)
    new_posts = subreddit.new(limit=5)
    hot_posts = subreddit.hot(limit=0)
    #print(new_posts)

    list_posts = [top_posts, new_posts, hot_posts]


    #check for each post (hot, new, top)
    for post in list_posts:

        for poste in post:
            #Check if the date it's after 2024
            date = poste.created_utc

            if date > start_date:
                #Save to csv file
                #print(post.title)
                #print(post.url)
                #print(poste.id)

                # Comment from one post with his id
                post_id = reddit.submission(id=poste.id)


                list_comments = get_comments(reddit, poste.id, 500)
                print("here",list_comments)

                #Get all the ids
                ids = [comment.id for comment in list_comments]


                for id in ids:
                    com = reddit.comment(id=id)
                    come = com.body
                    score = com.score
                    print(come)
                    print(score)
                    # Create the file in the correct directory and write it
                    with open('file/news/' + a, 'a', newline='', encoding='utf-8') as file:
                        file.write(come+'\n')
                        file.write('name,age\n')

                print(len(list_comments))

                """
                # Comments from one post
                comments = post.comments
                for comment in comments:
                    print("**********")
                    print(comment.body)
                    print(comment.author)
                    print(comment.score)
                    print(comment.created_utc)    
                """

print ("**********")
