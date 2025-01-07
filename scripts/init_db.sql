-- Drop tables if they exist (in correct order)
DROP TABLE IF EXISTS comments;  -- Drop child tables first
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR(255),
    bio TEXT,
    avatar_url VARCHAR(255),
    article_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create articles table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary VARCHAR(500),
    status VARCHAR(20) DEFAULT 'draft',
    tags VARCHAR[],
    comment_count INTEGER DEFAULT 0,
    author_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    article_id INTEGER NOT NULL REFERENCES articles(id),
    author_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create index
CREATE INDEX ix_articles_id ON articles(id);
CREATE INDEX ix_articles_tags ON articles USING GIN (tags);
CREATE INDEX ix_comments_article_id ON comments(article_id);
CREATE INDEX ix_comments_author_id ON comments(author_id);