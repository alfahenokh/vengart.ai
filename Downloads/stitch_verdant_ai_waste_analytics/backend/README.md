# Verdant AI Integrated Dashboard - Backend

This is the backend service for the Verdant AI Integrated Dashboard, built with FastAPI and PostgreSQL.

## Database Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for running the application)

### Quick Start

1. **Test Database Setup** (recommended first step):
   ```bash
   python test_db_setup.py
   ```
   This will verify Docker is working and test the basic database setup.

2. **Start Database Services**:
   ```bash
   # For development
   docker-compose -f docker-compose.dev.yml up -d postgres redis
   
   # Or use the main docker-compose.yml
   docker-compose up -d postgres redis
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   # Using Alembic (recommended)
   alembic upgrade head
   
   # Or using the management script
   python manage_db.py init
   ```

5. **Start the Application**:
   ```bash
   python main.py
   ```

### Database Schema

The database includes the following main tables:

- **users**: User authentication and profiles
- **fleet_units**: Fleet vehicle and equipment tracking
- **waste_forecasts**: AI-generated waste volume predictions
- **simulation_scenarios**: Simulation configurations
- **simulation_executions**: Simulation run results
- **kpi_metrics**: Key performance indicators
- **analytics_reports**: Generated reports and exports

### Database Management

Use the `manage_db.py` script for database operations:

```bash
# Check database connection
python manage_db.py check

# Get database information
python manage_db.py info

# Initialize database (create tables)
python manage_db.py init

# Show database schema SQL
python manage_db.py schema
```

### Development Tools

- **pgAdmin**: Available at http://localhost:5050 when using `docker-compose.dev.yml`
  - Email: admin@verdant-ai.local
  - Password: admin

### Configuration

Database configuration is managed through environment variables:

- `POSTGRES_DB`: Database name (default: verdant_ai)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_HOST`: Database host (default: localhost)
- `POSTGRES_PORT`: Database port (default: 5432)

### Migrations

Database migrations are managed with Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### API Endpoints

Once running, the API will be available at:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Database Info**: http://localhost:8000/api/v1/database/info

### Troubleshooting

1. **Database Connection Issues**:
   - Ensure PostgreSQL container is running: `docker-compose ps`
   - Check logs: `docker-compose logs postgres`
   - Verify connection: `python manage_db.py check`

2. **Migration Issues**:
   - Check Alembic configuration in `alembic.ini`
   - Ensure database is accessible
   - Review migration files in `alembic/versions/`

3. **Dependency Issues**:
   - Use `requirements-minimal.txt` for basic setup
   - Install build tools if needed for asyncpg/psycopg2

### Architecture

The backend follows a modular structure:

```
backend/
├── app/
│   ├── core/           # Core configuration and database
│   ├── models/         # SQLAlchemy models
│   ├── api/           # API endpoints (future)
│   └── services/      # Business logic (future)
├── alembic/           # Database migrations
├── main.py           # FastAPI application
└── manage_db.py      # Database management script
```

### Next Steps

After completing the database setup:

1. Implement authentication endpoints
2. Add CRUD operations for all models
3. Set up WebSocket services for real-time updates
4. Integrate AI/ML services
5. Add comprehensive testing

For more information, see the main project documentation.