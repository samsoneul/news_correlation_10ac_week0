import psycopg2
import os

from dotenv import load_dotenv


load_dotenv()

pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user=pg_user,
    password=pg_password,
    port="5432"
)
cur = conn.cursor()

# SQL statements to create tables
create_articles_table = """
CREATE TABLE IF NOT EXISTS articles (
    article_id SERIAL PRIMARY KEY,
    source_id INT,
    source_name VARCHAR(255),
    author VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    url VARCHAR(255),
    url_to_image VARCHAR(255),
    published_at TIMESTAMP,
    content TEXT,
    category VARCHAR(255),
    article TEXT,
    title_sentiment VARCHAR(50),
    clean_title TEXT,
    clean_content TEXT,
    predicted_category VARCHAR(255)
);
"""

create_traffic_table = """
CREATE TABLE IF NOT EXISTS traffic (
    Domain VARCHAR(255) PRIMARY KEY,
    GlobalRank INT
);
"""

create_domains_location_table = """
CREATE TABLE IF NOT EXISTS domains_location (
    Domain VARCHAR(255) PRIMARY KEY,
    Country VARCHAR(255),
    SourceCommonName VARCHAR(255)
);
"""

# Execute SQL statements
cur.execute(create_articles_table)
cur.execute(create_traffic_table)
cur.execute(create_domains_location_table)

# Commit the changes
conn.commit()

# Close the connection
cur.close()
conn.close()
