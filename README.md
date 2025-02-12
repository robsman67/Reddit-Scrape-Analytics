# Analysis of Reactions and Opinions of Reddit Users on Cryptocurrencies (2024)

## 📊 Project Overview
This project aims to analyze the reactions and opinions of Reddit users regarding cryptocurrencies in 2024. Using **web scraping**, sentiment analysis, and natural language processing techniques, we extracted and studied thousands of posts and comments from various specialized subreddits.

---

## 🚀 Project Objectives
- **Scraping Reddit data** via the PRAW API.
- **Sentiment analysis** with the NLTK library.
- **Data visualization** through box plots and word clouds.
- **Comparison** of results with previous studies on Twitter and socio-demographic data.

---

## 🛠️ Technologies Used
- **Python** (main programming language)
- **PRAW**: Reddit data scraping
- **NLTK**: Sentiment analysis and natural language processing
- **Matplotlib & Seaborn**: Data visualization (box plots)
- **WordCloud**: Generating word clouds

---


## Installation

### Clone the repository
```bash
git@github.com:robsman67/Reddit-Scrape-Analytics.git
cd Reddit-Scrape-Analytics
```

### Install the dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Set up your Reddit API credentials in a file named *variable.py*
```python
client_secret = 'your_client_secret'
password = 'your_password'
user_agent = 'your_user_agent'
username = 'your_username'
cliend_id = 'your_client_id'
```

### Run the main script
```bash
python main.py
```

## 🔍 Methodology
### 1️⃣ Data Collection
- **Scraped Subreddits (11 in total):**
  - *News*: r/Bitcoin, r/CryptoCurrency, r/BitcoinDiscussion, etc.
  - *Trading*: r/CryptoMarkets, r/BitcoinMarkets, r/ethtrader, etc.
- **Data Volume:**
  - **1,590 posts** and **54,000 comments** collected in 2024.

### 2️⃣ Data Analysis
- **Preprocessing:** Data cleaning, tokenization, lemmatization.
- **Sentiment Analysis:** Using VADER to classify sentiments (positive, negative, neutral).
- **Score Calculation:** Weighted average of post and comment sentiments.

### 3️⃣ Visualization
- **Word Clouds:** To identify the most frequent terms.
- **Box Plots:** To visualize the distribution of sentiments.

---

## 📈 Results
### 📊 Box Plots
- Sentiment analysis of titles and comments.
- Comparison between *news* and *trade* categories.

#### 📰 News
![img_7.png](file/img/img_7.png)
#### 📈 Trade
![img_6.png](file/img/img_6.png)

### ☁️ Word Clouds
- **News:** Focus on "bitcoin," "money," "fake," "scam," etc.
- **Trading:** Presence of technical terms like "tipped," "minutes," "learn."

#### 📰 News
![img.png](file/img/img.png)
#### 📈 Trade
![img_1.png](file/img/img_1.png)

