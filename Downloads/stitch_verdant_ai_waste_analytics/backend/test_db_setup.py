"""
Test script to verify database setup without full dependencies
"""
import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} successful")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}")
        return False

def check_docker():
    """Check if Docker is available"""
    return run_command("docker --version", "Checking Docker")

def check_docker_compose():
    """Check if Docker Compose is available"""
    return run_command("docker-compose --version", "Checking Docker Compose")

def start_database():
    """Start the database using Docker Compose"""
    return run_command(
        "docker-compose -f docker-compose.dev.yml up -d postgres redis",
        "Starting PostgreSQL and Redis"
    )

def wait_for_database():
    """Wait for database to be ready"""
    print("\nWaiting for database to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        if run_command(
            "docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U postgres",
            f"Database ready check (attempt {attempt + 1}/{max_attempts})"
        ):
            return True
        time.sleep(2)
    return False

def test_database_connection():
    """Test database connection"""
    return run_command(
        'docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d verdant_ai_dev -c "SELECT version();"',
        "Testing database connection"
    )

def show_database_info():
    """Show database information"""
    commands = [
        ('docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d verdant_ai_dev -c "\\l"', "Listing databases"),
        ('docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d verdant_ai_dev -c "\\dt"', "Listing tables"),
        ('docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d verdant_ai_dev -c "SELECT COUNT(*) as extension_count FROM pg_extension;"', "Checking extensions"),
    ]
    
    for command, description in commands:
        run_command(command, description)

def run_migration():
    """Run database migration manually"""
    migration_sql = """
    -- Create UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Create a simple test table
    CREATE TABLE IF NOT EXISTS test_connection (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        message TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Insert test data
    INSERT INTO test_connection (message) VALUES ('Database setup test successful');
    
    -- Query test data
    SELECT * FROM test_connection;
    """
    
    # Write SQL to temporary file
    with open('/tmp/test_migration.sql', 'w') as f:
        f.write(migration_sql)
    
    return run_command(
        'docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d verdant_ai_dev -f /dev/stdin < /tmp/test_migration.sql',
        "Running test migration"
    )

def cleanup():
    """Clean up Docker containers"""
    run_command(
        "docker-compose -f docker-compose.dev.yml down",
        "Stopping containers"
    )

def main():
    """Main test function"""
    print("=== Verdant AI Database Setup Test ===")
    
    # Check prerequisites
    if not check_docker():
        print("Docker is required but not available. Please install Docker.")
        return False
    
    if not check_docker_compose():
        print("Docker Compose is required but not available. Please install Docker Compose.")
        return False
    
    try:
        # Start database
        if not start_database():
            print("Failed to start database containers")
            return False
        
        # Wait for database to be ready
        if not wait_for_database():
            print("Database failed to become ready")
            return False
        
        # Test connection
        if not test_database_connection():
            print("Database connection test failed")
            return False
        
        # Run test migration
        if not run_migration():
            print("Test migration failed")
            return False
        
        # Show database info
        show_database_info()
        
        print("\n=== Database Setup Test Complete ===")
        print("✓ All tests passed!")
        print("✓ PostgreSQL is running and accessible")
        print("✓ Database schema can be created")
        print("✓ Basic operations work correctly")
        
        print("\nNext steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Run Alembic migrations: alembic upgrade head")
        print("3. Start the FastAPI application: python main.py")
        
        return True
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return False
    except Exception as e:
        print(f"\nTest failed with exception: {e}")
        return False
    finally:
        # Ask user if they want to keep containers running
        try:
            keep_running = input("\nKeep database containers running? (y/N): ").lower().strip()
            if keep_running != 'y':
                cleanup()
        except KeyboardInterrupt:
            cleanup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)