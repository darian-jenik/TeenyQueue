-- db_setup/db.sql

-- 1. Create the database
CREATE DATABASE mydatabase;

-- 2. Connect to the new database
\c mydatabase;

-- 3. Create the restricted user
CREATE USER queue_user WITH PASSWORD 'change_this_to_the_queue_user_password';

-- 4. Grant permissions to the restricted user
GRANT CONNECT ON DATABASE mydatabase TO queue_user;
GRANT USAGE ON SCHEMA public TO queue_user;

-- 5. Create the table
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- Required for gen_random_uuid()

CREATE TABLE queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pub_module_name VARCHAR NOT NULL,
    topic VARCHAR NOT NULL,
    message_body TEXT NOT NULL,
    _authentication_key VARCHAR,
    has_authentication BOOLEAN DEFAULT FALSE NOT NULL,
    target_module_name VARCHAR,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    delivered_at TIMESTAMPTZ,
    schedule_date TIMESTAMPTZ,
    delivered_to_module VARCHAR
);

-- 6. Grant permissions on the table to the restricted user
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE queue TO queue_user;

-- end
