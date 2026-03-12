import pandas as pd
import sqlite3

# DB Connecting
conn = sqlite3.connect('netflix.db')

# Save each query result as a data frame
df_type = pd.read_sql("""
    SELECT type,
           COUNT(*) AS count,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM works), 1) AS percentage
    FROM works
    GROUP BY type
""", conn)


df_genre = pd.read_sql("""
    SELECT genre_name,
           COUNT(*) AS content_count
    FROM works_genres_raw
    GROUP BY genre_name
    ORDER BY content_count DESC
    LIMIT 10
""", conn)

df_year = pd.read_sql("""
    SELECT strftime('%Y', date_added) AS year,
           COUNT(*) AS added_count
    FROM works
    WHERE date_added IS NOT NULL
    GROUP BY year
    ORDER BY year
""", conn)

df_contents = pd.read_sql("""
    SELECT country,
       COUNT(*) AS content_count
    FROM works
    WHERE country != 'Unknown'
    GROUP BY country
    ORDER BY content_count DESC
    LIMIT 10;
""", conn)


df_country = pd.read_sql("""
    SELECT country,
       SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movies,
       SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
       COUNT(*) AS total
    FROM works
    WHERE country != 'Unknown'
    GROUP BY country
    HAVING total >= 10
    ORDER BY total DESC;
""", conn)


df_tvCountry = pd.read_sql("""
    SELECT country,
       COUNT(*) AS total,
       SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
       ROUND(SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS tv_ratio
    FROM works
    WHERE country IN ('South Korea', 'United States', 'Japan', 'India', 'United Kingdom')
    GROUP BY country
    ORDER BY tv_ratio DESC;
""", conn)


df_koreanGenre = pd.read_sql("""
    SELECT g.genre_name,
       COUNT(*) AS count
    FROM works w
    JOIN works_genres_raw g ON w.show_id = g.show_id
    WHERE w.country = 'South Korea'
    GROUP BY g.genre_name
    ORDER BY count DESC;
""", conn)


df_koreanTVShowTrend = pd.read_sql("""
    SELECT strftime('%Y', date_added) AS year,
        COUNT(*) AS korean_tv_count
    FROM works
    WHERE country = 'South Korea'
    AND type = 'TV Show'
    AND date_added IS NOT NULL
    GROUP BY year
    ORDER BY year;
""", conn)



conn.close()

# Save to Excel (separate by sheet)
with pd.ExcelWriter('netflix_analysis.xlsx', engine='openpyxl') as writer:
    df_type.to_excel(writer, sheet_name='Overall Movie vs TV Show', index=False)
    df_genre.to_excel(writer, sheet_name='Contents by Genre', index=False)
    df_year.to_excel(writer, sheet_name='Changes by Year', index=False)
    df_contents.to_excel(writer, sheet_name='Top 10 Contents by Genre', index=False)
    df_country.to_excel(writer, sheet_name='Movie vs TV Show by Country', index=False)
    df_tvCountry.to_excel(writer, sheet_name='TV Show by Country', index=False)
    df_koreanGenre.to_excel(writer, sheet_name='Korean Genre Distribution', index=False)
    df_koreanTVShowTrend.to_excel(writer, sheet_name='Korean TV Show Trends', index=False)

print("✅ netflix_analysis.xlsx file has been created.")