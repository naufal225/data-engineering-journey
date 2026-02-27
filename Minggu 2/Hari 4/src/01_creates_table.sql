CREATE DATABASE praktek_etl_simple;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users (user_id),
    title TEXT NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS joined_analytics (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users (user_id),
    title_length INT NOT NULL,
    body_length INT NOT NULL,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts (user_id);

CREATE INDEX IF NOT EXISTS idx_joined_user_id ON joined_analytics (user_id);

title_length INT NOT NULL CHECK (title_length >= 0),
body_length INT NOT NULL CHECK (body_length >= 0)