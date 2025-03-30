# Setting Up a Local Supabase Development Environment

This guide provides step-by-step instructions for setting up a local Supabase development environment using the Supabase CLI. This allows you to develop and test your application without depending on an external Supabase instance.

## Installing the Supabase CLI

### Windows

#### Using Windows Package Manager (winget)
```powershell
winget install supabase.cli
```

#### Using Scoop
```powershell
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

#### Using npm
```powershell
npm install -g supabase
```

### macOS

#### Using Homebrew
```bash
brew install supabase/tap/supabase
```

#### Using npm
```bash
npm install -g supabase
```

### Linux

#### Using npm
```bash
npm install -g supabase
```

#### Using Debian/Ubuntu package
```bash
curl -fsSL https://github.com/supabase/cli/releases/download/v1.83.1/supabase_1.83.1_linux_amd64.deb -o supabase.deb
sudo dpkg -i supabase.deb
```

#### Using Linux binaries
```bash
curl -fsSL https://github.com/supabase/cli/releases/latest/download/supabase_linux_amd64.tar.gz | tar -xz
sudo mv supabase /usr/local/bin/
```

### Verify Installation
To verify that the Supabase CLI has been installed correctly:

```bash
supabase --version
```

## Prerequisites

Before proceeding, make sure you have:

1. **Docker and Docker Compose** installed and running
2. **Git** installed
3. At least 4GB of RAM allocated to Docker

## Setting Up a Local Supabase Project

### 1. Initialize a Local Supabase Project

Navigate to your FastAPI project directory and initialize Supabase:

```bash
cd fastapi.basic.standard
supabase init
```

This creates a `.supabase` directory with configuration files.

### 2. Start the Local Supabase Instance

```bash
supabase start
```

The first time you run this, it will download Docker images which might take some time. Once complete, you should see output similar to:

```
Started supabase local development setup.

         API URL: http://localhost:54321
          DB URL: postgresql://postgres:postgres@localhost:54322/postgres
      Studio URL: http://localhost:54323
    Inbucket URL: http://localhost:54324
        anon key: eyJh...
service_role key: eyJh...
```

Take note of the `anon key` as you'll need it for configuration.

### 3. Update Your Environment Variables

Edit your `.env.local` file to use the local Supabase instance:

```
SUPABASE_URL=http://localhost:54321
SUPABASE_KEY=eyJh...  # Use the anon key from the output
SUPABASE_JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters
```

## Setting Up Google OAuth with Local Supabase

### 1. Create a Google OAuth Client

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" and select "OAuth client ID"
5. Configure the OAuth consent screen
6. Set application type to "Web application"
7. Add `http://localhost:54321/auth/v1/callback` as an authorized redirect URI
8. Note your Client ID and Client Secret

### 2. Configure Supabase Auth with Google Provider

1. Open the Supabase Studio at http://localhost:54323
2. Navigate to Authentication > Providers
3. Find Google in the list and enable it
4. Enter your Google Client ID and Client Secret
5. Save the configuration

### 3. Configure Supabase CLI

```bash
supabase functions config set SUPABASE_AUTH_GOOGLE_CLIENT_ID="your-google-client-id"
supabase functions config set SUPABASE_AUTH_GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

## Using the Local Supabase Instance

### Creating Database Migrations

Create a new migration:

```bash
supabase migration new create_users_table
```

This creates a new SQL file in `supabase/migrations/`.

Edit the migration file to define your database schema, then apply it:

```bash
supabase db reset
```

### Viewing the Database

To access the PostgreSQL database directly:

```bash
supabase db connect
```

### Accessing Supabase Studio

Open http://localhost:54323 in your browser to access Supabase Studio, which provides a UI for managing your database, auth, storage, and more.

## Testing the Authentication

1. Start your FastAPI application:
```bash
python scripts/run.py
```

2. Navigate to the Google login endpoint:
```
http://localhost:8000/api/v1/auth/login/google
```

3. You should be redirected to Google's authentication page, and after logging in, redirected back to your application.

## Stopping the Local Supabase Instance

When you're done developing, you can stop the local Supabase instance:

```bash
supabase stop
```

## Common Issues and Troubleshooting

### Port Conflicts
If you see errors about ports already being in use, you may have another service using one of the required ports (54321-54324). You can:
- Stop the conflicting service
- Configure Supabase to use different ports in `supabase/config.toml`

### Docker Memory Issues
If Docker crashes or the Supabase services keep restarting, you may need to allocate more memory to Docker:
- In Docker Desktop settings, increase the memory allocation to at least 4GB

### Database Connection Issues
If your application can't connect to the Supabase database:
- Check that the URL and key in your `.env.local` file match the output from `supabase start`
- Make sure Docker is running and the Supabase containers are healthy (`docker ps`)

## Advanced Configuration

For more advanced configuration options, see the [Supabase CLI documentation](https://supabase.com/docs/reference/cli/introduction).
