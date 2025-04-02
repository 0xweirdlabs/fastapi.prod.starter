# Quick Start Guide

This guide will help you get started with this FastAPI template, focusing on Supabase authentication and protected CRUD operations.

## Setup Overview

1. Create a Supabase project
2. Set up Google OAuth
3. Configure your environment variables
4. Run the application
5. Test authentication and CRUD operations

## 1. Creating a Supabase Project

1. Go to [app.supabase.io](https://app.supabase.io) and sign up or log in
2. Create a new project
3. Note your project URL and anon key from the API settings

## 2. Setting Up Google OAuth

1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project (or use an existing one)
3. Create OAuth 2.0 Client ID credentials:
   - Application type: Web application
   - Authorized redirect URI: `https://[YOUR_PROJECT_ID].supabase.co/auth/v1/callback`
4. Note your Client ID and Client Secret
5. In your Supabase dashboard, go to Authentication → Providers
6. Enable Google and enter your Client ID and Client Secret

## 3. Configuring Environment Variables

Create a `.env.local` file with the following content:

```
# Environment settings
ENVIRONMENT=development
DEBUG=true

# Database settings
DATABASE_URL=sqlite:///./app.db

# Supabase Authentication settings
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret

# OAuth settings
OAUTH_REDIRECT_URL=http://localhost:8000/api/v1/auth/callback
FRONTEND_URL=http://localhost:3000

# Security settings
SECRET_KEY=your-random-secret-key
```

Replace:
- `your-project-id.supabase.co` with your Supabase project URL
- `your-supabase-anon-key` with your Supabase anon key
- `your-jwt-secret` with your JWT secret from Supabase settings

## 4. Running the Application

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run the application:
```bash
python scripts/run.py
```

The application will create the SQLite database and start on `http://localhost:8000`.

## 5. Testing Authentication and CRUD Operations

### Authentication Flow

1. Open your browser and navigate to:
```
http://localhost:8000/api/v1/auth/login/google
```

2. This will redirect you to Google's login page.

3. After logging in, you'll be redirected to your frontend URL (`http://localhost:3000` by default) with a token parameter.

4. For testing purposes, you can extract the token from the URL and use it for API calls.

### Testing Protected CRUD Operations

You'll need to include the token in the `Authorization` header for all requests.

#### Creating an Item

```bash
curl -X POST http://localhost:8000/api/v1/items/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Item", "description": "This is a test item"}'
```

#### Getting Your Items

```bash
curl -X GET http://localhost:8000/api/v1/items/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Getting a Specific Item

```bash
curl -X GET http://localhost:8000/api/v1/items/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Updating an Item

```bash
curl -X PUT http://localhost:8000/api/v1/items/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "description": "Updated description"}'
```

#### Deleting an Item

```bash
curl -X DELETE http://localhost:8000/api/v1/items/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Using with a Frontend

In a real application, your frontend would:

1. Redirect users to `/api/v1/auth/login/google` for login
2. Handle the callback and store the token
3. Include the token in all API requests
4. Use the `/api/v1/auth/me` endpoint to get the current user info

## Next Steps

- Set up automatic token refresh
- Add more CRUD operations for your specific domain
- Deploy your application to production
