"""
Database utility functions for initialization and management
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.database import async_engine, Base
from app.core.config import settings

logger = logging.getLogger(__name__)


async def create_database():
    """Create database tables"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise


async def drop_database():
    """Drop all database tables (use with caution!)"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


async def check_database_connection():
    """Check if database connection is working"""
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            await result.fetchone()
        logger.info("Database connection successful")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def get_database_info():
    """Get database information"""
    try:
        async with async_engine.begin() as conn:
            # Get PostgreSQL version
            version_result = await conn.execute(text("SELECT version()"))
            version = await version_result.fetchone()
            
            # Get database size
            size_result = await conn.execute(text(
                f"SELECT pg_size_pretty(pg_database_size('{settings.postgres_db}'))"
            ))
            size = await size_result.fetchone()
            
            # Get table count
            table_result = await conn.execute(text(
                "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            table_count = await table_result.fetchone()
            
            return {
                "version": version[0] if version else "Unknown",
                "size": size[0] if size else "Unknown", 
                "table_count": table_count[0] if table_count else 0,
                "database_name": settings.postgres_db
            }
    except SQLAlchemyError as e:
        logger.error(f"Error getting database info: {e}")
        return None


async def initialize_database():
    """Initialize database with tables and basic data"""
    logger.info("Initializing database...")
    
    # Check connection first
    if not await check_database_connection():
        raise Exception("Cannot connect to database")
    
    # Create tables
    await create_database()
    
    # Get database info
    info = await get_database_info()
    if info:
        logger.info(f"Database initialized: {info['database_name']} "
                   f"({info['table_count']} tables, {info['size']})")
    
    logger.info("Database initialization complete")


if __name__ == "__main__":
    # Allow running this script directly for database management
    import sys
    
    async def main():
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == "init":
                await initialize_database()
            elif command == "create":
                await create_database()
            elif command == "drop":
                await drop_database()
            elif command == "check":
                success = await check_database_connection()
                print(f"Database connection: {'OK' if success else 'FAILED'}")
            elif command == "info":
                info = await get_database_info()
                if info:
                    print(f"Database: {info['database_name']}")
                    print(f"Version: {info['version']}")
                    print(f"Size: {info['size']}")
                    print(f"Tables: {info['table_count']}")
            else:
                print("Usage: python db_utils.py [init|create|drop|check|info]")
        else:
            await initialize_database()
    
    asyncio.run(main())