import pandas as pd
import os
import sqlite3

# ---- Step 1: Opening the file ----
# Checking if the file exists
if not os.path.exists('netflix_titles.csv'):
    print("The file is not found. Check the location of the file.")
else:
    print("The file is found.")
    df = pd.read_csv('netflix_titles.csv')
    print(f"✅ Data loading complete — {df.shape[0]} row(s), {df.shape[1]} column(s)")

# ---- Step 2: Data Refining ----

    # Checking missing values
    print("\n[Missing value status]")
    print(df.isnull().sum())

    # Major processing
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['country'] = df['country'].fillna('Unknown')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')

    # Separating genres
    df['listed_in'] = df['listed_in'].str.split(', ')

    print("\n✅ Refining complete")
    print(df.dtypes)

# ---- Step 3: DB Design and Structuring ----

    # DB connecting (created automatically if not exists)
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    print("\n✅ DB connected successfully.")

    # --- works table ---
    df_works = df[['show_id', 'type', 'title', 'director',
                   'country', 'release_year', 'date_added',
                   'rating', 'duration']].copy()

    df_works.to_sql('works', conn, if_exists='replace', index=False)
    print(f"✅ works table saved — {len(df_works)} row(s)")

    # --- works_genres_raw table ---
    df_genres = df[['show_id', 'listed_in']].explode('listed_in').copy()
    df_genres.columns = ['show_id', 'genre_name']
    df_genres = df_genres.dropna(subset=['genre_name'])
    df_genres['genre_name'] = df_genres['genre_name'].str.strip()

    df_genres.to_sql('works_genres_raw', conn, if_exists='replace', index=False)
    print(f"✅ works_genres_raw table saved — {len(df_genres)} row(s)")

    # --- cast_members table ---
    df_cast = df[['show_id', 'cast']].copy()
    df_cast = df_cast[df_cast['cast'] != 'Unknown']
    df_cast['cast'] = df_cast['cast'].str.split(', ')
    df_cast = df_cast.explode('cast')
    df_cast.columns = ['show_id', 'actor_name']
    df_cast = df_cast.dropna(subset=['actor_name'])

    df_cast.to_sql('cast_members', conn, if_exists='replace', index=False)
    print(f"✅ cast_members table saved — {len(df_cast)} row(s)")

# Save and Exit
    conn.commit()
    conn.close()
    print("\n✅ All done — netflix.db file has been created.")