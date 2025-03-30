# Setting Up Supabase for Local Development

This guide explains how to set up Supabase locally for development with Google OAuth authentication.

## Prerequisites

- Docker and Docker Compose
- Supabase CLI

## Installing Supabase CLI

```bash
# Using npm
npm install -g supabase

# Or using Homebrew (macOS)
brew install supabase/tap/supabase
```

## Starting Local Supabase

1. Initialize Supabase in your project folder:

```bash
supabase init
```

2. Start the local Supabase instance:

```bash
supabase start
```

This will start a local Supabase stack, including PostgreSQL, GoTrue (Auth), PostgREST, and other services.

3. Update your `.env.local` file with the local Supabase URL and key:

```
SUPABASE_URL=http://localhost:54321
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Use the anon key from supabase start output
SUPABASE_JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
```

## Configuring Google OAuth

To use Google OAuth with local Supabase:

1. Create a Google OAuth 2.0 Client ID in the [Google Cloud Console](https://console.cloud.google.com/):
   - Create a new project
   - Go to "APIs & Services" > "Credentials"
   - Create an OAuth client ID
   - Set the authorized redirect URI to `http://localhost:54321/auth/v1/callback`

2. Update Supabase Auth configuration:

```bash
supabase functions config set SUPABASE_AUTH_GOOGLE_CLIENT_ID="your-google-client-id"
supabase functions config set SUPABASE_AUTH_GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

3. Configure Google OAuth in the Supabase dashboard:
   - Open the local Supabase dashboard at `http://localhost:54323`
   - Go to Authentication > Providers
   - Enable Google and enter your Client ID and Client Secret

## Testing Google Authentication

1. Navigate to `http://localhost:8000/api/v1/auth/login/google` in your browser
2. You should be redirected to Google's login page
3. After authenticating, you'll be redirected back to your application

## Using with Production Supabase

When ready for production:

1. Create a Supabase project at [app.supabase.io](https://app.supabase.io)
2. Set up Google OAuth in the Supabase dashboard
3. Update your environment variables with production values:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-supabase-jwt-secret
```

## Switching Between Local and Supabase Authentication

The template is designed to work in two modes:

1. **Local Authentication**: If Supabase configuration is missing, it falls back to local JWT-based authentication
2. **Supabase Authentication**: When Supabase URL and key are provided, it uses Supabase Auth

This allows for smooth development and testing without requiring Supabase to be running.

## Data Migration

When moving from local development to Supabase:

1. Export your SQLite data
2. Transform it to match Supabase's schema
3. Import into Supabase PostgreSQL

A migration script example is available in `scripts/migrate_to_supabase.py`
