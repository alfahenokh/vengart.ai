-- Verdant AI Integrated Dashboard Database Initialization
-- This file is executed when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist (handled by Docker environment variables)
-- CREATE DATABASE verdant_ai;

-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable PostGIS extension for spatial data (if needed for future geo features)
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- Create indexes for performance optimization
-- Note: These will be created by Alembic migrations, but we can add some basic ones here

-- Performance indexes for common queries
-- These will be recreated by migrations, but having them here ensures basic performance

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Grant necessary permissions
-- GRANT ALL PRIVILEGES ON DATABASE verdant_ai TO postgres;

-- Set timezone
SET timezone = 'UTC';