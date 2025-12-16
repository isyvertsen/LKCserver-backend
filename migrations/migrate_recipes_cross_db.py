"""Migrate recipe data from nkclarvikkommune1 database to current database."""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

async def migrate_recipes_cross_db():
    # Parse the current database URL
    current_db_url = os.getenv('DATABASE_URL').replace('postgresql+asyncpg://', 'postgresql://')
    parsed = urlparse(current_db_url)
    
    # Build connection URL for source database (nkclarvikkommune1)
    source_db_url = f"postgresql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/nkclarvikkommune1"
    
    print(f"Connecting to source database: nkclarvikkommune1")
    print(f"Connecting to target database: {parsed.path[1:]}")
    
    # Connect to both databases
    source_conn = await asyncpg.connect(source_db_url)
    target_conn = await asyncpg.connect(current_db_url)
    
    try:
        # Check if source tables exist
        print("\nChecking source tables in nkclarvikkommune1...")
        source_tables = await source_conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name ILIKE '%rpkalkyle%'
            ORDER BY table_name
        """)
        
        print("Found source tables:")
        for table in source_tables:
            print(f"  - {table['table_name']}")
            # Quote table name to handle case sensitivity
            count = await source_conn.fetchval(f'SELECT COUNT(*) FROM "{table["table_name"]}"')
            print(f"    Records: {count}")
        
        # Clear existing test data in target
        print("\nClearing existing data in target database...")
        await target_conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
        await target_conn.execute("DELETE FROM tbl_rpkalkyle")
        await target_conn.execute("DELETE FROM tbl_rpkalkylegruppe")
        
        # Migrate recipe groups first
        print("\nMigrating recipe groups...")
        group_count = await source_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkylegruppe")
        if group_count > 0:
            groups = await source_conn.fetch("SELECT * FROM tbl_rpkalkylegruppe")
            
            for group in groups:
                await target_conn.execute("""
                    INSERT INTO tbl_rpkalkylegruppe (gruppeid, gruppenavn, merknad)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (gruppeid) DO UPDATE SET
                        gruppenavn = EXCLUDED.gruppenavn,
                        merknad = EXCLUDED.merknad
                """, group['gruppeid'], group.get('gruppenavn'), group.get('merknad'))
            
            print(f"  Migrated {len(groups)} recipe groups")
        
        # Migrate recipes
        print("\nMigrating recipes...")
        recipe_count = await source_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyle")
        if recipe_count > 0:
            # Get column names from both tables
            source_cols = await source_conn.fetch("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyle'
                ORDER BY ordinal_position
            """)
            
            target_cols = await target_conn.fetch("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyle'
                ORDER BY ordinal_position
            """)
            
            source_col_names = [col['column_name'] for col in source_cols]
            target_col_names = [col['column_name'] for col in target_cols]
            
            # Find common columns
            common_cols = [col for col in source_col_names if col in target_col_names]
            print(f"  Common columns: {common_cols}")
            
            # Fetch recipes in batches
            batch_size = 100
            offset = 0
            total_migrated = 0
            
            while True:
                cols_str = ', '.join(common_cols)
                recipes = await source_conn.fetch(f"""
                    SELECT {cols_str} 
                    FROM tbl_rpkalkyle 
                    ORDER BY kalkylekode 
                    LIMIT {batch_size} OFFSET {offset}
                """)
                
                if not recipes:
                    break
                
                # Insert into target
                for recipe in recipes:
                    values = [recipe[col] for col in common_cols]
                    placeholders = ', '.join([f'${i+1}' for i in range(len(common_cols))])
                    
                    await target_conn.execute(f"""
                        INSERT INTO tbl_rpkalkyle ({cols_str})
                        VALUES ({placeholders})
                        ON CONFLICT (kalkylekode) DO NOTHING
                    """, *values)
                
                total_migrated += len(recipes)
                offset += batch_size
                print(f"  Migrated {total_migrated} recipes...")
            
            print(f"  Total recipes migrated: {total_migrated}")
        
        # Migrate recipe details
        print("\nMigrating recipe details...")
        detail_count = await source_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyledetaljer")
        if detail_count > 0:
            # Get column names
            source_detail_cols = await source_conn.fetch("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyledetaljer'
                ORDER BY ordinal_position
            """)
            
            target_detail_cols = await target_conn.fetch("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyledetaljer'
                ORDER BY ordinal_position
            """)
            
            source_detail_col_names = [col['column_name'] for col in source_detail_cols]
            target_detail_col_names = [col['column_name'] for col in target_detail_cols]
            
            # Find common columns
            common_detail_cols = [col for col in source_detail_col_names if col in target_detail_col_names]
            print(f"  Common detail columns: {common_detail_cols}")
            
            # Migrate in batches
            batch_size = 500
            offset = 0
            total_detail_migrated = 0
            
            while True:
                detail_cols_str = ', '.join(common_detail_cols)
                details = await source_conn.fetch(f"""
                    SELECT {detail_cols_str} 
                    FROM tbl_rpkalkyledetaljer 
                    ORDER BY tblkalkyledetaljerid 
                    LIMIT {batch_size} OFFSET {offset}
                """)
                
                if not details:
                    break
                
                # Insert into target
                for detail in details:
                    values = [detail[col] for col in common_detail_cols]
                    placeholders = ', '.join([f'${i+1}' for i in range(len(common_detail_cols))])
                    
                    try:
                        await target_conn.execute(f"""
                            INSERT INTO tbl_rpkalkyledetaljer ({detail_cols_str})
                            VALUES ({placeholders})
                            ON CONFLICT DO NOTHING
                        """, *values)
                    except Exception as e:
                        print(f"    Error inserting detail {detail.get('tblkalkyledetaljerid')}: {e}")
                
                total_detail_migrated += len(details)
                offset += batch_size
                print(f"  Migrated {total_detail_migrated} recipe details...")
            
            print(f"  Total recipe details migrated: {total_detail_migrated}")
        
        # Verify migration
        print("\nVerifying migration...")
        final_recipe_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyle")
        final_detail_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyledetaljer")
        final_group_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkylegruppe")
        
        print(f"Final counts in target database:")
        print(f"  - Recipe groups: {final_group_count}")
        print(f"  - Recipes: {final_recipe_count}")
        print(f"  - Recipe details: {final_detail_count}")
        
        # Show sample recipes
        if final_recipe_count > 0:
            samples = await target_conn.fetch("""
                SELECT k.kalkylekode, k.kalkylenavn, k.antallporsjoner, g.gruppenavn
                FROM tbl_rpkalkyle k
                LEFT JOIN tbl_rpkalkylegruppe g ON k.gruppeid = g.gruppeid
                ORDER BY k.kalkylekode
                LIMIT 10
            """)
            
            print("\nSample migrated recipes:")
            for sample in samples:
                print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} ({sample['antallporsjoner']} porsjoner) - {sample['gruppenavn'] or 'No group'}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await source_conn.close()
        await target_conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_recipes_cross_db())