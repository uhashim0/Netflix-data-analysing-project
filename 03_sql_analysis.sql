-- =============================================
-- Netflix Data Analysis Queries Collection
-- =============================================


-- 1. Checking all data
SELECT COUNT(*) AS total_count
FROM works;


-- 2. Movie vs. TV Show Ratio
SELECT type,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM works), 1) AS percentage
FROM works
GROUP BY type;


-- 3. Top 10 Contents by Genre
SELECT genre_name,
       COUNT(*) AS content_count
FROM works_genres_raw
GROUP BY genre_name
ORDER BY content_count DESC
LIMIT 10;


-- 4. Annual New Content Trend
SELECT strftime('%Y', date_added) AS year,
       COUNT(*) AS added_count
FROM works
WHERE date_added IS NOT NULL
GROUP BY year
ORDER BY year;


-- 5. Top 10 Contents by Country
SELECT country,
       COUNT(*) AS content_count
FROM works
WHERE country != 'Unknown'
GROUP BY country
ORDER BY content_count DESC
LIMIT 10;


-- 6. Movie vs TV Show Ratio by Country
SELECT country,
       SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movies,
       SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
       COUNT(*) AS total
FROM works
WHERE country != 'Unknown'
GROUP BY country
HAVING total >= 10
ORDER BY total DESC;


-- 7. TV Show Ratio by Country
SELECT country,
       COUNT(*) AS total,
       SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
       ROUND(SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS tv_ratio
FROM works
WHERE country IN ('South Korea', 'United States', 'Japan', 'India', 'United Kingdom')
GROUP BY country
ORDER BY tv_ratio DESC;


-- 8. Korean Content Genre Distribution
SELECT g.genre_name,
       COUNT(*) AS count
FROM works w
JOIN works_genres_raw g ON w.show_id = g.show_id
WHERE w.country = 'South Korea'
GROUP BY g.genre_name
ORDER BY count DESC;


-- 9. Korean TV Show Annual Trends
SELECT strftime('%Y', date_added) AS year,
       COUNT(*) AS korean_tv_count
FROM works
WHERE country = 'South Korea'
  AND type = 'TV Show'
  AND date_added IS NOT NULL
GROUP BY year
ORDER BY year;