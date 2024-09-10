import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Fonction de prétraitement des textes
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


# Fonction d'analyse des sentiments
def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores['compound']


def sentiment_analysis(list_subreddit_news, list_subreddit_trade):
    list_subreddit_all = [list_subreddit_news, list_subreddit_trade]

    for list_subreddit in list_subreddit_all:
        print(list_subreddit)
        save_in = "news" if list_subreddit == list_subreddit_news else "trade"

        for subreddit_name in list_subreddit:
            print(subreddit_name)

            # Lecture du fichier CSV ligne par ligne
            with open('file/' + save_in + '/' + subreddit_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Variables pour stocker les résultats
            posts_data = []
            current_post = None
            comments = []

            # Parcourir les lignes du fichier
            for line in lines:
                line = line.strip()  # Supprimer les espaces blancs et les retours à la ligne

                if line.startswith("Title:"):
                    # Si une nouvelle ligne commence par "Title", cela signifie qu'on commence un nouveau post
                    if current_post:
                        # Sauvegarder l'ancien post dans la liste des posts avant d'en traiter un nouveau
                        current_post['comments'] = comments
                        posts_data.append(current_post)

                    # Initialisation du nouveau post
                    current_post = {'title': line.replace("Title:", "").strip(), 'votes': 0, 'comments': []}
                    comments = []

                elif line.isdigit():
                    # Si la ligne est un nombre, il s'agit des votes pour le titre ou pour un commentaire
                    if not current_post['votes']:
                        # Si le nombre de votes pour le titre n'est pas encore attribué
                        current_post['votes'] = int(line)
                    else:
                        # Sinon, il s'agit des votes pour le commentaire
                        comments[-1]['votes'] = int(line)

                elif line:
                    # Si la ligne n'est ni un titre ni un nombre, c'est un commentaire
                    comments.append({'text': line, 'votes': 0})

            # Ajouter le dernier post si nécessaire
            if current_post:
                current_post['comments'] = comments
                posts_data.append(current_post)

            # Analyse des sentiments et création du DataFrame
            post_titles = []
            title_sentiments = []
            avg_comment_sentiments = []

            for post in posts_data:
                # Analyse du sentiment du titre
                processed_title = preprocess_text(post['title'])
                title_sentiment = get_sentiment(processed_title)

                # Imprimer le titre et son sentiment pour vérifier le résultat
                print(f"Title: {post['title']}, Sentiment: {title_sentiment}")

                # Analyse des sentiments des commentaires
                comment_sentiments = []
                for comment in post['comments']:
                    processed_comment = preprocess_text(comment['text'])
                    comment_sentiment = get_sentiment(processed_comment)
                    comment_sentiments.append(comment_sentiment)

                # Calcul de la moyenne des sentiments des commentaires
                if comment_sentiments:
                    avg_sentiment = sum(comment_sentiments) / len(comment_sentiments)
                else:
                    avg_sentiment = None  # Pas de commentaires

                # Stockage des résultats
                post_titles.append(post['title'])
                title_sentiments.append(title_sentiment)
                avg_comment_sentiments.append(avg_sentiment)

            # Création du DataFrame Pandas
            df = pd.DataFrame({
                'Title': post_titles,
                'Title Sentiment': title_sentiments,
                'Average Comment Sentiment': avg_comment_sentiments
            })

            # Sauvegarde dans un fichier CSV

            if save_in == "news":
                save_in_two = "analyse_news"
            else:
                save_in_two = "analyse_trade"

            df.to_csv('file/' + save_in_two + '/analyse_' + subreddit_name + '.csv', index=False)
            #print(df)
