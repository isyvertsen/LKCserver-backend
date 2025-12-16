"""Add index on leveringsdato for better query performance."""
import asyncio
import os
import sys
from sqlalchemy import create_engine, text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def add_index():
    """Add index on leveringsdato column."""
    # Convert async URL to sync URL
    db_url = str(settings.DATABASE_URL).replace("postgresql+asyncpg", "postgresql")
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        # Check if index already exists
        result = conn.execute(text("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'tblordrer' 
            AND indexname = 'ix_tblordrer_leveringsdato'
        """))
        
        if result.rowcount == 0:
            print("Creating index on tblordrer.leveringsdato...")
            conn.execute(text("""
                CREATE INDEX ix_tblordrer_leveringsdato 
                ON tblordrer(leveringsdato)
            """))
            conn.commit()
            print("Index created successfully!")
        else:
            print("Index already exists")
            
        # Also create composite index for kundegruppe filtering
        result = conn.execute(text("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'tblordrer' 
            AND indexname = 'ix_tblordrer_kundeid'
        """))
        
        if result.rowcount == 0:
            print("Creating index on tblordrer.kundeid...")
            conn.execute(text("""
                CREATE INDEX ix_tblordrer_kundeid 
                ON tblordrer(kundeid)
            """))
            conn.commit()
            print("Index created successfully!")
        else:
            print("Index on kundeid already exists")

if __name__ == "__main__":
    add_index()