import logging
import subprocess

from sqlalchemy import text

from src.core.config import settings
from src.core.database.database import engine

logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables using Alembic"""
    try:
        if settings.environment == "production":
            logger.info("Skipping database tables creation in production")
            return

        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True, check=True
        )
        logger.info("Database tables created successfully using Alembic")
        logger.debug(f"Migration output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating database tables: {e}")
        logger.error(f"Migration stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        logger.error("Alembic not found, cannot create tables")
        raise


def drop_tables():
    """Drop all database tables and related objects using direct SQL"""
    try:
        with engine.connect() as connection:
            # Drop all tables with CASCADE to handle foreign keys
            result = connection.execute(
                text(
                    """
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """
                )
            )
            tables = [row[0] for row in result]

            if tables:
                for table in tables:
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                logger.info(f"Dropped {len(tables)} tables: {', '.join(tables)}")
            else:
                logger.info("No tables found to drop")

            # Drop all ENUM types
            result = connection.execute(
                text(
                    """
                SELECT typname 
                FROM pg_type 
                WHERE typtype = 'e' 
                AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
            """
                )
            )
            enums = [row[0] for row in result]

            if enums:
                for enum_name in enums:
                    connection.execute(
                        text(f'DROP TYPE IF EXISTS "{enum_name}" CASCADE')
                    )
                logger.info(f"Dropped {len(enums)} ENUM types: {', '.join(enums)}")
            else:
                logger.info("No ENUM types found to drop")

            # Drop all sequences (except those owned by tables, which are dropped with CASCADE)
            result = connection.execute(
                text(
                    """
                SELECT sequencename 
                FROM pg_sequences 
                WHERE schemaname = 'public'
            """
                )
            )
            sequences = [row[0] for row in result]

            if sequences:
                for sequence in sequences:
                    connection.execute(
                        text(f'DROP SEQUENCE IF EXISTS "{sequence}" CASCADE')
                    )
                logger.info(
                    f"Dropped {len(sequences)} sequences: {', '.join(sequences)}"
                )
            else:
                logger.info("No sequences found to drop")

            connection.commit()

    except Exception as e:
        logger.error(f"Error dropping database objects: {e}")
        raise


def reset_database():
    """Reset database by dropping and recreating all tables"""
    logger.warning("Resetting database - all data will be lost!")
    drop_tables()
    create_tables()


def check_database_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def run_migrations():
    """Run Alembic migrations"""
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True, check=True
        )
        logger.info("Database migrations applied successfully")
        logger.debug(f"Migration output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running migrations: {e}")
        logger.error(f"Migration stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        logger.warning("Alembic not found, skipping migrations")
        return False


def should_use_migrations():
    """Determine whether to use migrations or create_all()"""
    if settings.environment == "production":
        return False

    if settings.use_migrations:
        return True

    return False


def init_database():
    """Initialize database with tables and basic setup"""
    logger.info("Initializing database...")

    if not check_database_connection():
        raise ConnectionError("Cannot connect to database")

    if should_use_migrations():
        logger.info("Using Alembic migrations for database initialization")
        run_migrations()
    else:
        logger.info("Using SQLAlchemy create_all for database initialization")
        create_tables()

    logger.info("Database initialization completed")
