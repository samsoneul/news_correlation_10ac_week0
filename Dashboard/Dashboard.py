import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# Load data
df_r = pd.read_csv("../data/rating.csv")
df_t = pd.read_csv("../data/traffic.csv")
df_d = pd.read_csv("../data/domains_location.csv")

# Function to preprocess text
def preprocess_text(text):
    # Implement your preprocessing logic here
    return text

# Function to extract countries from text
def extract_countries(text):
    # Implement your logic to extract countries from text here
    return ''

# Preprocess data
df_r["clean_title"] = df_r["title"].apply(preprocess_text)
df_r["clean_content"] = df_r["content"].apply(preprocess_text)
df_r['countries'] = df_r['category'].apply(extract_countries)

# Sidebar
st.sidebar.title('Navigation')
selected_task = st.sidebar.radio(
    'Go to',
    ['Website Counts', 'Traffic', 'Domain Counts', 'Sentiment Analysis', 'Geographical Distribution']
)

# Main content
if selected_task == 'Website Counts':
    st.header("Website Counts")
    website_count = df_r['source_name'].value_counts().reset_index()
    website_count.columns=["source_name","article_count"]

    top_10 = website_count.sort_values(by='article_count', ascending=False).head(10)
    bottom_10 = website_count.sort_values(by='article_count', ascending=False).tail(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(x='article_count', y='source_name', data=top_10, palette='Blues')
    plt.title('Top 10 websites with largest count of news articles')
    plt.xlabel('Number of articles')
    plt.ylabel('Website')

    plt.subplot(1, 2, 2)
    sns.barplot(x='article_count', y='source_name', data=bottom_10, palette='Blues')
    plt.title('Bottom 10 websites with smallest count of news articles')
    plt.xlabel('Number of articles')
    plt.ylabel('Website')

    st.pyplot(fig)

elif selected_task == 'Traffic':
    st.header("Top 10 Websites with the Highest Traffic")
    top_traffic_websites = df_t.head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='GlobalRank', y='Domain', data=top_traffic_websites, palette='Blues_d')

    plt.xlabel('Global Rank')
    plt.ylabel('Website')
    plt.title('Top 10 Websites with the Highest Traffic')

    st.pyplot(fig)

elif selected_task == 'Domain Counts':
    st.header("Top 10 Countries with the Highest Number of News Media Organisations")
    domain_count = df_d.groupby('Country').size().reset_index()
    domain_count = domain_count.rename(columns={0: 'Count of Domains'})
    domain_count = domain_count.sort_values(by='Count of Domains', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Country', y='Count of Domains', data=domain_count, palette='Blues')

    st.pyplot(fig)

elif selected_task == 'Sentiment Analysis':
    st.header("Sentiment Analysis")

    # TF-IDF Vectorization
    df_r.dropna(subset=['clean_title', 'category'], inplace=True)
    X = df_r['clean_title']
    y = df_r['category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)

    df_r.reset_index(drop=True, inplace=True)
    predicted_categories_df_r = clf.predict(tfidf_vectorizer.transform(df_r["clean_title"]))
    df_r["predicted_category"] = predicted_categories_df_r

    diverse_website = df_r.groupby("source_name")["predicted_category"].nunique().reset_index(name="number of topics")
    diverse_website = diverse_website.sort_values(by="number of topics", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='source_name', y='number of topics', data=diverse_website, palette='Blues')
    plt.title('Top 10 websites with the most diverse topics')
    plt.xlabel('Websites')
    plt.ylabel('Topics covered')
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

elif selected_task == 'Geographical Distribution':
    st.header("Geographical Distribution of Top 10 Websites")

    merged_df = pd.merge(df_r, df_d, left_on='source_name', right_on='SourceCommonName', how='inner')
    country_counts = merged_df['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Article Count']

    top_10_countries = country_counts.head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Article Count', y='Country', data=top_10_countries, palette='Blues')

    plt.title('Top 10 Countries by Geographical Distribution of Articles')
    plt.xlabel('Article Count')
    plt.ylabel('Country')

    st.pyplot(fig)
