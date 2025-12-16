"""Migration to rename products, nutrients, allergens tables to matinfo_ prefix.

This migration renames the Matinfo lookup tables to have the matinfo_ prefix,
clearly distinguishing them from the internal product catalog (tblprodukter).

Tables renamed:
- products → matinfo_products
- nutrients → matinfo_nutrients
- allergens → matinfo_allergens
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from psycopg2 import sql


def get_db_connection():
    """Get database connection from environment variable."""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    # Convert asyncpg URL to psycopg2 URL
    db_url = db_url.replace('postgresql+asyncpg://', 'postgresql://')

    return psycopg2.connect(db_url)


def check_table_exists(cursor, table_name):
    """Check if a table exists."""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]


def rename_tables(cursor):
    """Rename the Matinfo tables to have matinfo_ prefix."""
    tables_to_rename = [
        ('products', 'matinfo_products'),
        ('nutrients', 'matinfo_nutrients'),
        ('allergens', 'matinfo_allergens')
    ]

    for old_name, new_name in tables_to_rename:
        # Check if old table exists
        if not check_table_exists(cursor, old_name):
            print(f"⚠️  Table '{old_name}' does not exist, skipping...")
            continue

        # Check if new table already exists
        if check_table_exists(cursor, new_name):
            print(f"⚠️  Table '{new_name}' already exists, skipping rename...")
            continue

        print(f"Renaming {old_name} → {new_name}...")
        cursor.execute(
            sql.SQL("ALTER TABLE {} RENAME TO {}").format(
                sql.Identifier(old_name),
                sql.Identifier(new_name)
            )
        )
        print(f"✓ Successfully renamed {old_name} to {new_name}")


def verify_migration(cursor):
    """Verify the migration was successful."""
    print("\n=== Verification ===")

    for table_name in ['matinfo_products', 'matinfo_nutrients', 'matinfo_allergens']:
        if check_table_exists(cursor, table_name):
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"✓ {table_name}: {count:,} rows")
        else:
            print(f"✗ {table_name}: Table not found!")


def main():
    """Run the migration."""
    print("=== Matinfo Tables Rename Migration ===\n")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Show current state
        print("Current state:")
        for table in ['products', 'nutrients', 'allergens']:
            if check_table_exists(cursor, table):
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} rows")

        print("\n" + "="*50 + "\n")

        # Perform the rename
        rename_tables(cursor)

        # Commit the changes
        conn.commit()

        # Verify
        verify_migration(cursor)

        print("\n✅ Migration completed successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
