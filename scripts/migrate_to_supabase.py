#!/usr/bin/env python
"""
Script to migrate data from local SQLite database to Supabase.

Usage:
    python migrate_to_supabase.py

Requirements:
    - supabase-py
    - sqlalchemy
    - dotenv
"""
import os
import sys
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any

import httpx
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv('.env.local')

# Configuration
SQLITE_DB_PATH = 'app.db'
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env.local")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def connect_sqlite():
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        sys.exit(1)


def get_tables(conn):
    """Get all tables from SQLite database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def fetch_table_data(conn, table_name):
    """Fetch all data from a table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def migrate_users(conn):
    """Migrate users from SQLite to Supabase Auth"""
    print("Migrating users...")
    try:
        users = fetch_table_data(conn, "users")
        for user in users:
            # Skip if missing required fields
            if not user.get('email') or not user.get('hashed_password'):
                continue
                
            # Create user in Supabase Auth
            try:
                # First check if user already exists
                result = supabase.table('users').select('*').eq('email', user['email']).execute()
                if len(result.data) > 0:
                    print(f"User {user['email']} already exists in Supabase, skipping...")
                    continue
                
                # For admin operations like importing users with passwords,
                # you'd typically use Supabase's admin API which requires service_role key
                # Here we're just creating them as new users
                print(f"Creating user {user['email']} in Supabase...")
                
                # Note: This is a simplified example. In a real migration,
                # you'd want to use the Admin API to preserve password hashes.
                # This example just creates new users, which isn't ideal for production.
                user_data = {
                    'email': user['email'],
                    'password': 'TemporaryPassword123!',  # Temporary password, user should reset
                    'email_confirm': True,
                    'user_metadata': {
                        'full_name': user.get('full_name', ''),
                        'is_superuser': user.get('is_superuser', False),
                    }
                }
                
                # You'll need to use a service_role key for this in real implementation
                # This is just a placeholder for the concept
                print(f"Created user: {user['email']} (would require service_role key)")
                
            except Exception as e:
                print(f"Error creating user {user['email']}: {e}")
                
    except Exception as e:
        print(f"Error migrating users: {e}")


def migrate_table_data(conn, table_name):
    """Migrate table data from SQLite to Supabase"""
    print(f"Migrating table: {table_name}...")
    try:
        data = fetch_table_data(conn, table_name)
        if not data:
            print(f"No data found in table: {table_name}")
            return
            
        # Skip users table as it's handled separately
        if table_name == 'users':
            return
            
        # Insert data in batches
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            try:
                result = supabase.table(table_name).insert(batch).execute()
                print(f"Inserted {len(batch)} rows into {table_name}")
            except Exception as e:
                print(f"Error inserting batch into {table_name}: {e}")
                
    except Exception as e:
        print(f"Error migrating table {table_name}: {e}")


def main():
    """Main migration function"""
    print("Starting migration from SQLite to Supabase...")
    
    # Connect to SQLite
    conn = connect_sqlite()
    
    # Get all tables
    tables = get_tables(conn)
    print(f"Found tables: {', '.join(tables)}")
    
    # Migrate users first
    if 'users' in tables:
        migrate_users(conn)
    
    # Migrate other tables
    for table in tables:
        if table != 'users' and not table.startswith('sqlite_'):
            migrate_table_data(conn, table)
    
    print("Migration completed!")
    conn.close()


if __name__ == "__main__":
    main()
