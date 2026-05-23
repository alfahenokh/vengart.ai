"""
Database management script for Verdant AI Integrated Dashboard
This script can be used to initialize, migrate, and manage the database
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app.core.config import settings
    from app.core.db_utils import (
        initialize_database,
        create_database,
        check_database_connection,
        get_database_info
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False


def print_usage():
    """Print usage information"""
    print("Database Management Script for Verdant AI Integrated Dashboard")
    print("Usage: python manage_db.py [command]")
    print()
    print("Commands:")
    print("  init     - Initialize database with tables")
    print("  check    - Check database connection")
    print("  info     - Show database information")
    print("  create   - Create database tables")
    print("  schema   - Show database schema SQL")
    print("  help     - Show this help message")


def show_schema():
    """Show the database schema SQL"""
    schema_sql = """
-- Verdant AI Integrated Dashboard Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User roles enum
CREATE TYPE userrole AS ENUM ('admin', 'operator', 'analyst', 'viewer');

-- Fleet unit types and status enums
CREATE TYPE fleetunittype AS ENUM ('collection', 'transport', 'processing');
CREATE TYPE fleetunitstatus AS ENUM ('active', 'idle', 'maintenance', 'offline');
CREATE TYPE capacityunit AS ENUM ('tons', 'cubic_meters');

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role userrole NOT NULL DEFAULT 'viewer',
    profile JSONB,
    preferences JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_login_at TIMESTAMP WITH TIME ZONE
);

-- Fleet units table
CREATE TABLE fleet_units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier VARCHAR(20) UNIQUE NOT NULL,
    type fleetunittype NOT NULL,
    status fleetunitstatus NOT NULL DEFAULT 'idle',
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    address VARCHAR(255),
    zone VARCHAR(100),
    current_capacity DECIMAL(10,2) NOT NULL DEFAULT 0,
    maximum_capacity DECIMAL(10,2) NOT NULL,
    capacity_unit capacityunit NOT NULL DEFAULT 'tons',
    assigned_route JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Maintenance records table
CREATE TABLE maintenance_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fleet_unit_id UUID NOT NULL REFERENCES fleet_units(id),
    maintenance_type VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_date TIMESTAMP WITH TIME ZONE,
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    estimated_duration_hours DECIMAL(5,2),
    actual_duration_hours DECIMAL(5,2),
    status VARCHAR(50) NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Waste forecasts table
CREATE TABLE waste_forecasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    predictions JSONB NOT NULL,
    accuracy DECIMAL(5,2),
    model_version VARCHAR(50),
    confidence_interval DECIMAL(5,2),
    parameters JSONB,
    factors JSONB,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- KPI metrics table
CREATE TABLE kpi_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    value DECIMAL(15,4) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    target DECIMAL(15,4),
    previous_value DECIMAL(15,4),
    change_percent DECIMAL(5,2),
    trend VARCHAR(10),
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    metadata JSONB,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Analytics reports table
CREATE TABLE analytics_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    filters JSONB,
    data JSONB NOT NULL,
    summary JSONB,
    file_path VARCHAR(500),
    file_format VARCHAR(10),
    file_size DECIMAL(10,0),
    generated_by UUID NOT NULL REFERENCES users(id),
    generation_time_ms DECIMAL(10,0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Simulation scenarios table
CREATE TABLE simulation_scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parameters JSONB NOT NULL,
    tags JSONB,
    version VARCHAR(20) DEFAULT '1.0',
    created_by UUID NOT NULL REFERENCES users(id),
    is_public VARCHAR(10) NOT NULL DEFAULT 'false',
    execution_count INTEGER NOT NULL DEFAULT 0,
    last_executed TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Simulation executions table
CREATE TABLE simulation_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_id UUID NOT NULL REFERENCES simulation_scenarios(id),
    execution_name VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'running',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    execution_time_ms DECIMAL(10,0),
    results JSONB,
    summary JSONB,
    efficiency_score DECIMAL(5,2),
    cost_savings DECIMAL(12,2),
    carbon_reduction DECIMAL(10,2),
    error_message TEXT,
    error_details JSONB,
    executed_by UUID NOT NULL REFERENCES users(id),
    execution_parameters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Simulation logs table
CREATE TABLE simulation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID NOT NULL REFERENCES simulation_executions(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    data JSONB,
    step_number INTEGER,
    step_name VARCHAR(100),
    memory_usage_mb DECIMAL(10,2),
    cpu_usage_percent DECIMAL(5,2)
);

-- Route optimizations table
CREATE TABLE route_optimizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID NOT NULL REFERENCES simulation_executions(id),
    route_name VARCHAR(255) NOT NULL,
    fleet_unit_id UUID REFERENCES fleet_units(id),
    original_route JSONB,
    optimized_route JSONB NOT NULL,
    distance_reduction_km DECIMAL(8,2),
    time_reduction_minutes DECIMAL(8,2),
    fuel_savings_liters DECIMAL(8,2),
    cost_savings DECIMAL(10,2),
    waypoints JSONB NOT NULL,
    constraints JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_fleet_units_identifier ON fleet_units(identifier);
CREATE INDEX idx_fleet_units_status ON fleet_units(status);
CREATE INDEX idx_waste_forecasts_region ON waste_forecasts(region);
CREATE INDEX idx_waste_forecasts_region_date ON waste_forecasts(region, start_date, end_date);
CREATE INDEX idx_kpi_metrics_name ON kpi_metrics(name);
CREATE INDEX idx_simulation_scenarios_created_by ON simulation_scenarios(created_by);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fleet_units_updated_at BEFORE UPDATE ON fleet_units FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_maintenance_records_updated_at BEFORE UPDATE ON maintenance_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_kpi_metrics_updated_at BEFORE UPDATE ON kpi_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_simulation_scenarios_updated_at BEFORE UPDATE ON simulation_scenarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""
    print(schema_sql)


async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_usage()
        return
    
    if command == "schema":
        show_schema()
        return
    
    if not DEPENDENCIES_AVAILABLE:
        print("Error: Required dependencies not installed.")
        print("Please install dependencies first:")
        print("  pip install fastapi sqlalchemy asyncpg alembic")
        return
    
    try:
        if command == "init":
            print("Initializing database...")
            await initialize_database()
            print("Database initialization complete!")
            
        elif command == "create":
            print("Creating database tables...")
            await create_database()
            print("Database tables created!")
            
        elif command == "check":
            print("Checking database connection...")
            success = await check_database_connection()
            if success:
                print("✓ Database connection successful")
            else:
                print("✗ Database connection failed")
                
        elif command == "info":
            print("Getting database information...")
            info = await get_database_info()
            if info:
                print(f"Database: {info['database_name']}")
                print(f"Version: {info['version']}")
                print(f"Size: {info['size']}")
                print(f"Tables: {info['table_count']}")
            else:
                print("Could not retrieve database information")
                
        else:
            print(f"Unknown command: {command}")
            print_usage()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if sys.version_info >= (3, 7):
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())