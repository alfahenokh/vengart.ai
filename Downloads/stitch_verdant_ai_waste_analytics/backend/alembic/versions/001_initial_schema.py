"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'operator', 'analyst', 'viewer', name='userrole'), nullable=False, server_default='viewer'),
        sa.Column('profile', sa.JSON(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create fleet_units table
    op.create_table('fleet_units',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('identifier', sa.String(length=20), nullable=False),
        sa.Column('type', sa.Enum('collection', 'transport', 'processing', name='fleetunittype'), nullable=False),
        sa.Column('status', sa.Enum('active', 'idle', 'maintenance', 'offline', name='fleetunitstatus'), nullable=False, server_default='idle'),
        sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
        sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('zone', sa.String(length=100), nullable=True),
        sa.Column('current_capacity', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'),
        sa.Column('maximum_capacity', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('capacity_unit', sa.Enum('tons', 'cubic_meters', name='capacityunit'), nullable=False, server_default='tons'),
        sa.Column('assigned_route', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_update', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fleet_units_identifier'), 'fleet_units', ['identifier'], unique=True)
    op.create_index(op.f('ix_fleet_units_status'), 'fleet_units', ['status'])

    # Create maintenance_records table
    op.create_table('maintenance_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('fleet_unit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('maintenance_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('scheduled_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('estimated_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('actual_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('estimated_duration_hours', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('actual_duration_hours', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='scheduled'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['fleet_unit_id'], ['fleet_units.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create waste_forecasts table
    op.create_table('waste_forecasts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('region', sa.String(length=100), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('predictions', sa.JSON(), nullable=False),
        sa.Column('accuracy', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('confidence_interval', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('factors', sa.JSON(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_waste_forecasts_region'), 'waste_forecasts', ['region'])
    op.create_index('ix_waste_forecasts_region_date', 'waste_forecasts', ['region', 'start_date', 'end_date'])

    # Create kpi_metrics table
    op.create_table('kpi_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('value', sa.Numeric(precision=15, scale=4), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('target', sa.Numeric(precision=15, scale=4), nullable=True),
        sa.Column('previous_value', sa.Numeric(precision=15, scale=4), nullable=True),
        sa.Column('change_percent', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('trend', sa.String(length=10), nullable=True),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('period_end', sa.DateTime(timezone=True), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_kpi_metrics_name'), 'kpi_metrics', ['name'])

    # Create analytics_reports table
    op.create_table('analytics_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('parameters', sa.JSON(), nullable=False),
        sa.Column('filters', sa.JSON(), nullable=True),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('summary', sa.JSON(), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_format', sa.String(length=10), nullable=True),
        sa.Column('file_size', sa.Numeric(precision=10, scale=0), nullable=True),
        sa.Column('generated_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('generation_time_ms', sa.Numeric(precision=10, scale=0), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['generated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create simulation_scenarios table
    op.create_table('simulation_scenarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('version', sa.String(length=20), nullable=True, server_default='1.0'),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_public', sa.String(length=10), nullable=False, server_default='false'),
        sa.Column('execution_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_executed', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_simulation_scenarios_created_by'), 'simulation_scenarios', ['created_by'])

    # Create simulation_executions table
    op.create_table('simulation_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('scenario_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('execution_name', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='running'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('execution_time_ms', sa.Numeric(precision=10, scale=0), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('summary', sa.JSON(), nullable=True),
        sa.Column('efficiency_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('cost_savings', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('carbon_reduction', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_details', sa.JSON(), nullable=True),
        sa.Column('executed_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('execution_parameters', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['executed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['scenario_id'], ['simulation_scenarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create simulation_logs table
    op.create_table('simulation_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('level', sa.String(length=10), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('step_number', sa.Integer(), nullable=True),
        sa.Column('step_name', sa.String(length=100), nullable=True),
        sa.Column('memory_usage_mb', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('cpu_usage_percent', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['execution_id'], ['simulation_executions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create route_optimizations table
    op.create_table('route_optimizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('route_name', sa.String(length=255), nullable=False),
        sa.Column('fleet_unit_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('original_route', sa.JSON(), nullable=True),
        sa.Column('optimized_route', sa.JSON(), nullable=False),
        sa.Column('distance_reduction_km', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('time_reduction_minutes', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('fuel_savings_liters', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('cost_savings', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('waypoints', sa.JSON(), nullable=False),
        sa.Column('constraints', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['execution_id'], ['simulation_executions.id'], ),
        sa.ForeignKeyConstraint(['fleet_unit_id'], ['fleet_units.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create triggers for updated_at columns
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    # Add triggers to tables with updated_at columns
    for table in ['users', 'fleet_units', 'maintenance_records', 'kpi_metrics', 'simulation_scenarios']:
        op.execute(f"""
            CREATE TRIGGER update_{table}_updated_at 
            BEFORE UPDATE ON {table} 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)


def downgrade() -> None:
    # Drop triggers
    for table in ['users', 'fleet_units', 'maintenance_records', 'kpi_metrics', 'simulation_scenarios']:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};")
    
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop tables in reverse order
    op.drop_table('route_optimizations')
    op.drop_table('simulation_logs')
    op.drop_table('simulation_executions')
    op.drop_table('simulation_scenarios')
    op.drop_table('analytics_reports')
    op.drop_table('kpi_metrics')
    op.drop_table('waste_forecasts')
    op.drop_table('maintenance_records')
    op.drop_table('fleet_units')
    op.drop_table('users')
    
    # Drop enums
    op.execute("DROP TYPE IF EXISTS userrole;")
    op.execute("DROP TYPE IF EXISTS fleetunittype;")
    op.execute("DROP TYPE IF EXISTS fleetunitstatus;")
    op.execute("DROP TYPE IF EXISTS capacityunit;")