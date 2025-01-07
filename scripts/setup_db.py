import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text

from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)


def reset_database():
    """Reset the database - drop all tables and recreate them"""
    # Read the SQL file
    sql_file = Path(__file__).parent / "init_db.sql"
    with open(sql_file) as f:
        sql = f.read()

    # Execute the SQL
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    print("✅ Database reset successfully")


if __name__ == "__main__":
    reset_database()
