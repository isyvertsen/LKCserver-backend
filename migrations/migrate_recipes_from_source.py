"""Migrate recipe data from nkclarvikkommune1.tbl_rpKalkyle to public schema."""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def migrate_recipes():
    db_url = os.getenv('DATABASE_URL').replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    
    try:
        # First, clear existing test data
        print("Clearing existing test data...")
        await conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
        await conn.execute("DELETE FROM tbl_rpkalkyle")
        
        # Check if source table exists and has data
        source_count = await conn.fetchval("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'nkclarvikkommune1' 
            AND table_name = 'tbl_rpKalkyle'
        """)
        
        if source_count == 0:
            print("Source table nkclarvikkommune1.tbl_rpKalkyle not found!")
            return
            
        # Get column mappings between source and target
        print("Checking source table structure...")
        source_columns = await conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'nkclarvikkommune1' 
            AND table_name = 'tbl_rpKalkyle'
            ORDER BY ordinal_position
        """)
        
        print(f"Source columns: {[col['column_name'] for col in source_columns]}")
        
        # Get target columns
        target_columns = await conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = 'tbl_rpkalkyle'
            ORDER BY ordinal_position
        """)
        
        print(f"Target columns: {[col['column_name'] for col in target_columns]}")
        
        # Find common columns
        source_col_names = {col['column_name'].lower() for col in source_columns}
        target_col_names = {col['column_name'].lower() for col in target_columns}
        common_columns = source_col_names.intersection(target_col_names)
        
        print(f"\nCommon columns: {common_columns}")
        
        if not common_columns:
            print("No common columns found! Checking with case variations...")
            # Try case-insensitive mapping
            column_mapping = {}
            for src_col in source_columns:
                src_name = src_col['column_name']
                for tgt_col in target_columns:
                    tgt_name = tgt_col['column_name']
                    if src_name.lower() == tgt_name.lower():
                        column_mapping[src_name] = tgt_name
                        break
            
            if column_mapping:
                print(f"Column mapping: {column_mapping}")
                source_cols = list(column_mapping.keys())
                target_cols = list(column_mapping.values())
            else:
                print("No matching columns found!")
                return
        else:
            # Use common columns directly
            common_list = list(common_columns)
            source_cols = common_list
            target_cols = common_list
        
        # Count source records
        source_count = await conn.fetchval(f"SELECT COUNT(*) FROM nkclarvikkommune1.\"tbl_rpKalkyle\"")
        print(f"\nFound {source_count} recipes in source table")
        
        if source_count > 0:
            # Build the migration query
            source_cols_str = ', '.join([f'"{col}"' for col in source_cols])
            target_cols_str = ', '.join([f'"{col}"' for col in target_cols])
            
            # Migrate the data
            print(f"\nMigrating recipes...")
            query = f"""
                INSERT INTO public.tbl_rpkalkyle ({target_cols_str})
                SELECT {source_cols_str}
                FROM nkclarvikkommune1."tbl_rpKalkyle"
                ON CONFLICT (kalkylekode) DO NOTHING
            """
            
            result = await conn.execute(query)
            print(f"Migration query executed: {result}")
            
            # Verify migration
            migrated_count = await conn.fetchval("SELECT COUNT(*) FROM public.tbl_rpkalkyle")
            print(f"Migrated {migrated_count} recipes successfully")
            
            # Show sample migrated data
            samples = await conn.fetch("""
                SELECT kalkylekode, kalkylenavn, antallporsjoner, gruppeid
                FROM public.tbl_rpkalkyle
                LIMIT 5
            """)
            
            print("\nSample migrated recipes:")
            for sample in samples:
                print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} ({sample['antallporsjoner']} porsjoner)")
        
        # Now migrate recipe details if they exist
        print("\n\nChecking for recipe details...")
        detail_source_exists = await conn.fetchval("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'nkclarvikkommune1' 
            AND table_name = 'tbl_rpKalkyleDetaljer'
        """)
        
        if detail_source_exists:
            detail_count = await conn.fetchval('SELECT COUNT(*) FROM nkclarvikkommune1."tbl_rpKalkyleDetaljer"')
            print(f"Found {detail_count} recipe details in source")
            
            if detail_count > 0:
                # Get detail columns
                detail_source_columns = await conn.fetch("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'nkclarvikkommune1' 
                    AND table_name = 'tbl_rpKalkyleDetaljer'
                """)
                
                detail_target_columns = await conn.fetch("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = 'tbl_rpkalkyledetaljer'
                """)
                
                # Find common columns for details
                detail_mapping = {}
                for src_col in detail_source_columns:
                    src_name = src_col['column_name']
                    for tgt_col in detail_target_columns:
                        tgt_name = tgt_col['column_name']
                        if src_name.lower() == tgt_name.lower():
                            detail_mapping[src_name] = tgt_name
                            break
                
                if detail_mapping:
                    print(f"Detail column mapping: {detail_mapping}")
                    detail_source_cols = list(detail_mapping.keys())
                    detail_target_cols = list(detail_mapping.values())
                    
                    detail_source_cols_str = ', '.join([f'"{col}"' for col in detail_source_cols])
                    detail_target_cols_str = ', '.join([f'"{col}"' for col in detail_target_cols])
                    
                    print("Migrating recipe details...")
                    detail_query = f"""
                        INSERT INTO public.tbl_rpkalkyledetaljer ({detail_target_cols_str})
                        SELECT {detail_source_cols_str}
                        FROM nkclarvikkommune1."tbl_rpKalkyleDetaljer"
                        ON CONFLICT DO NOTHING
                    """
                    
                    await conn.execute(detail_query)
                    
                    detail_migrated = await conn.fetchval("SELECT COUNT(*) FROM public.tbl_rpkalkyledetaljer")
                    print(f"Migrated {detail_migrated} recipe details")
        
        # Check for recipe groups
        print("\n\nChecking for recipe groups...")
        group_source_exists = await conn.fetchval("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'nkclarvikkommune1' 
            AND table_name = 'tbl_rpKalkyleGruppe'
        """)
        
        if group_source_exists:
            group_count = await conn.fetchval('SELECT COUNT(*) FROM nkclarvikkommune1."tbl_rpKalkyleGruppe"')
            print(f"Found {group_count} recipe groups in source")
            
            if group_count > 0:
                # Clear existing groups first
                await conn.execute("DELETE FROM public.tbl_rpkalkylegruppe")
                
                print("Migrating recipe groups...")
                group_query = """
                    INSERT INTO public.tbl_rpkalkylegruppe (gruppeid, gruppenavn, merknad)
                    SELECT "GruppeID", "GruppeNavn", "Merknad"
                    FROM nkclarvikkommune1."tbl_rpKalkyleGruppe"
                    ON CONFLICT DO NOTHING
                """
                
                await conn.execute(group_query)
                
                group_migrated = await conn.fetchval("SELECT COUNT(*) FROM public.tbl_rpkalkylegruppe")
                print(f"Migrated {group_migrated} recipe groups")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_recipes())