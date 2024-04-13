import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Print current working directory
print(os.getcwd())

# Load environment variables from .env file
load_dotenv()

# Get PostgreSQL credentials from environment variables
pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')

# Define file paths
rating = "./data/rating.csv"
traffic = "./data/traffic.csv"
domain = "./data/domains_location.csv"


def clean_dataframe(df):
    # Check if 'source_name' column exists
    if 'source_name' not in df.columns:
        print("Error: 'source_name' column not found.")
        return df
    
    # Drop rows where 'source_name' is NaN
    df.dropna(subset=['source_name'], inplace=True)
    
    # Convert 'published_at' to datetime format
    if 'published_at' in df.columns:
        try:
            df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
        except Exception as e:
            print(f"Error converting 'published_at' to datetime: {e}")
            df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
            
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Convert text columns to lowercase and remove leading/trailing whitespaces
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].str.lower().str.strip()

    # Additional cleaning steps can be added here as needed

    return df






try:
    # Read CSV files into pandas DataFrames
    df_r = pd.read_csv(rating)
    df_t = pd.read_csv(traffic)
    df_d = pd.read_csv(domain)

    df_r = clean_dataframe(df_r)
    df_t = clean_dataframe(df_t)
    df_d = clean_dataframe(df_d)

    # Drop rows where 'source_name' is NaN
    df_r.dropna(subset=['source_name'], inplace=True)

    # Connect to PostgreSQL database
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@localhost:5432/postgres')

    # Insert DataFrames into PostgreSQL tables
    df_r.to_sql('articles', engine, if_exists='append', index=False)
    df_t.to_sql('traffic', engine, if_exists='append', index=False)
    df_d.to_sql('domains_location', engine, if_exists='append', index=False)

    print("Data insertion successful!")

except Exception as e:
    print(f"An error occurred: {e}")
