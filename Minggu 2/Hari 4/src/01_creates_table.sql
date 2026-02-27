CREATE DATABASE IF NOT EXISTS praktek_etl_simple;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT REFERENCES users (user_id),
    title TEXT NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE joined_analytics (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title_length INT NOT NULL,
    body_length INT NOT NULL,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL
);