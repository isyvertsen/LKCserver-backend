"""Migrate recipe data from nkclarvikkommune1 database to current database with case handling."""
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
        # Check if source tables exist - looking for case variations
        print("\nChecking source tables in nkclarvikkommune1...")
        
        # Look for recipe groups
        group_tables = await source_conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name ILIKE 'tbl_rpkalkylegruppe'
        """)
        
        source_group_table = None
        if group_tables:
            source_group_table = group_tables[0]['table_name']
            print(f"Found recipe group table: {source_group_table}")
            count = await source_conn.fetchval(f'SELECT COUNT(*) FROM "{source_group_table}"')
            print(f"  Records: {count}")
        
        # Look for main recipe table
        recipe_tables = await source_conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name ILIKE 'tbl_rpkalkyle'
            AND table_name NOT ILIKE '%detaljer%'
            AND table_name NOT ILIKE '%gruppe%'
        """)
        
        source_recipe_table = None
        if recipe_tables:
            source_recipe_table = recipe_tables[0]['table_name']
            print(f"Found recipe table: {source_recipe_table}")
            count = await source_conn.fetchval(f'SELECT COUNT(*) FROM "{source_recipe_table}"')
            print(f"  Records: {count}")
        
        # Look for recipe details
        detail_tables = await source_conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name ILIKE 'tbl_rpkalkyledetaljer'
        """)
        
        source_detail_table = None
        if detail_tables:
            source_detail_table = detail_tables[0]['table_name']
            print(f"Found recipe detail table: {source_detail_table}")
            count = await source_conn.fetchval(f'SELECT COUNT(*) FROM "{source_detail_table}"')
            print(f"  Records: {count}")
        
        if not source_recipe_table:
            print("No recipe table found in source database!")
            return
        
        # Clear existing data in target
        print("\nClearing existing data in target database...")
        await target_conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
        await target_conn.execute("DELETE FROM tbl_rpkalkyle")
        await target_conn.execute("DELETE FROM tbl_rpkalkylegruppe")
        
        # Migrate recipe groups first if they exist
        if source_group_table:
            print("\nMigrating recipe groups...")
            
            # Get columns with proper case
            source_cols = await source_conn.fetch(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = '{source_group_table}'
                ORDER BY ordinal_position
            """)
            
            print(f"Source group columns: {[col['column_name'] for col in source_cols]}")
            
            # Map columns (case-insensitive)
            column_map = {
                'gruppeid': None,
                'gruppenavn': None,
                'merknad': None
            }
            
            for src_col in source_cols:
                col_lower = src_col['column_name'].lower()
                if col_lower in column_map:
                    column_map[col_lower] = src_col['column_name']
            
            if column_map['gruppeid']:
                groups = await source_conn.fetch(f'SELECT * FROM "{source_group_table}"')
                
                for group in groups:
                    await target_conn.execute("""
                        INSERT INTO tbl_rpkalkylegruppe (gruppeid, gruppenavn, merknad)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (gruppeid) DO UPDATE SET
                            gruppenavn = EXCLUDED.gruppenavn,
                            merknad = EXCLUDED.merknad
                    """, 
                    group[column_map['gruppeid']], 
                    group.get(column_map['gruppenavn']) if column_map['gruppenavn'] else None,
                    group.get(column_map['merknad']) if column_map['merknad'] else None)
                
                print(f"  Migrated {len(groups)} recipe groups")
        
        # Migrate recipes
        print("\nMigrating recipes...")
        
        # Get source columns
        source_cols = await source_conn.fetch(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = '{source_recipe_table}'
            ORDER BY ordinal_position
        """)
        
        # Get target columns
        target_cols = await target_conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyle'
            ORDER BY ordinal_position
        """)
        
        source_col_map = {col['column_name'].lower(): col['column_name'] for col in source_cols}
        target_col_names = [col['column_name'] for col in target_cols]
        
        # Build column mapping
        column_pairs = []
        for target_col in target_col_names:
            if target_col.lower() in source_col_map:
                column_pairs.append((source_col_map[target_col.lower()], target_col))
        
        if not column_pairs:
            print("No matching columns found!")
            return
        
        print(f"Mapped {len(column_pairs)} columns")
        
        # Fetch and migrate recipes
        source_cols_str = ', '.join([f'"{pair[0]}"' for pair in column_pairs])
        target_cols_str = ', '.join([pair[1] for pair in column_pairs])
        placeholders = ', '.join([f'${i+1}' for i in range(len(column_pairs))])
        
        recipes = await source_conn.fetch(f'SELECT {source_cols_str} FROM "{source_recipe_table}"')
        
        migrated = 0
        for recipe in recipes:
            values = [recipe[pair[0]] for pair in column_pairs]
            try:
                await target_conn.execute(f"""
                    INSERT INTO tbl_rpkalkyle ({target_cols_str})
                    VALUES ({placeholders})
                    ON CONFLICT (kalkylekode) DO NOTHING
                """, *values)
                migrated += 1
            except Exception as e:
                print(f"  Error migrating recipe: {e}")
        
        print(f"  Migrated {migrated} recipes")
        
        # Migrate recipe details if they exist
        if source_detail_table:
            print("\nMigrating recipe details...")
            
            # Get columns
            source_detail_cols = await source_conn.fetch(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = '{source_detail_table}'
                ORDER BY ordinal_position
            """)
            
            target_detail_cols = await target_conn.fetch("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'tbl_rpkalkyledetaljer'
                ORDER BY ordinal_position
            """)
            
            source_detail_col_map = {col['column_name'].lower(): col['column_name'] for col in source_detail_cols}
            target_detail_col_names = [col['column_name'] for col in target_detail_cols]
            
            # Build column mapping for details
            detail_column_pairs = []
            for target_col in target_detail_col_names:
                if target_col.lower() in source_detail_col_map:
                    detail_column_pairs.append((source_detail_col_map[target_col.lower()], target_col))
            
            if detail_column_pairs:
                print(f"Mapped {len(detail_column_pairs)} detail columns")
                
                # Migrate in batches
                batch_size = 500
                offset = 0
                total_migrated = 0
                
                source_detail_cols_str = ', '.join([f'"{pair[0]}"' for pair in detail_column_pairs])
                target_detail_cols_str = ', '.join([pair[1] for pair in detail_column_pairs])
                detail_placeholders = ', '.join([f'${i+1}' for i in range(len(detail_column_pairs))])
                
                while True:
                    details = await source_conn.fetch(f"""
                        SELECT {source_detail_cols_str} 
                        FROM "{source_detail_table}"
                        ORDER BY 1
                        LIMIT {batch_size} OFFSET {offset}
                    """)
                    
                    if not details:
                        break
                    
                    for detail in details:
                        values = [detail[pair[0]] for pair in detail_column_pairs]
                        try:
                            await target_conn.execute(f"""
                                INSERT INTO tbl_rpkalkyledetaljer ({target_detail_cols_str})
                                VALUES ({detail_placeholders})
                                ON CONFLICT DO NOTHING
                            """, *values)
                            total_migrated += 1
                        except Exception as e:
                            pass  # Skip errors for individual records
                    
                    offset += batch_size
                    print(f"  Migrated {total_migrated} details...")
                
                print(f"  Total recipe details migrated: {total_migrated}")
        
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
                SELECT k.kalkylekode, k.kalkylenavn, k.antallporsjoner
                FROM tbl_rpkalkyle k
                ORDER BY k.kalkylekode
                LIMIT 10
            """)
            
            print("\nSample migrated recipes:")
            for sample in samples:
                print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} ({sample['antallporsjoner']} porsjoner)")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await source_conn.close()
        await target_conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_recipes_cross_db())