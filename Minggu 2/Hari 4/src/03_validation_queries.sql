SELECT COUNT(*) FROM joined_analytics;

SELECT COUNT(*) FROM joined_analytics
WHERE post_id IS NULL OR user_name IS NULL OR user_id IS NULL;

SELECT user_name, COUNT(*) AS post_count
FROM joined_analytics
GROUP BY user_name
ORDER BY post_count DESC, user_name ASC;

SELECT AVG(title_length) FROM joined_analytics;