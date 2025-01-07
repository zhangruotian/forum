# Forum Application Project Plan

## Overview

A forum application where users can publish articles with images and interact through comments.

## Tech Stack

### Backend

- FastAPI + Pydantic
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- Python-Jose (JWT tokens)
- Passlib (Password hashing)
- Google OAuth2
- AWS S3 (Image storage)

### Frontend

- Next.js
- Tailwind CSS (for styling)
- NextAuth.js (authentication)
- Axios (API calls)

### Deployment

- Railway.app

## Features Breakdown

### 1. Authentication System

- Email/Password registration and login
- Google OAuth integration
- JWT token-based authentication
- User profiles with avatars

### 2. Article System

- CRUD operations for articles
- Multiple image upload support
- Pagination (10 articles per page)
- Users can only edit/delete their own articles

### 3. Comment System

- Basic comments on articles
- Edit/Delete functionality for own comments
- No nested replies

## Database Schema

### Users

```sql
CREATE TABLE users (
id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
hashed_password VARCHAR(255),
full_name VARCHAR(255),
avatar_url VARCHAR(255),
google_id VARCHAR(255) UNIQUE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Articles

```sql
CREATE TABLE articles (
id SERIAL PRIMARY KEY,
title VARCHAR(255) NOT NULL,
content TEXT NOT NULL,
user_id INTEGER REFERENCES users(id),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Article Images

```sql
CREATE TABLE article_images (
id SERIAL PRIMARY KEY,
article_id INTEGER REFERENCES articles(id),
image_url VARCHAR(255) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Comments

```sql
CREATE TABLE comments (
id SERIAL PRIMARY KEY,
content TEXT NOT NULL,
article_id INTEGER REFERENCES articles(id),
user_id INTEGER REFERENCES users(id),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Phases

### Phase 1: Backend Setup

1. Project structure setup
2. Database configuration
3. User authentication implementation
4. AWS S3 configuration

### Phase 2: Core Backend Features

1. Article CRUD endpoints
2. Comment CRUD endpoints
3. Image upload functionality
4. Pagination implementation

### Phase 3: Frontend Setup

1. Next.js project setup
2. Authentication UI
3. Basic layout and navigation

### Phase 4: Frontend Features

1. Article creation/editing interface
2. Image upload interface
3. Comments interface
4. User profile page

### Phase 5: Deployment

1. Database setup on Railway
2. Backend deployment
3. Frontend deployment
4. Testing and bug fixes

