"""Migrate recipe details (ingredients) from source database."""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

async def migrate_recipe_details():
    db_url = os.getenv('DATABASE_URL').replace('postgresql+asyncpg://', 'postgresql://')
    parsed = urlparse(db_url)
    source_db_url = f"postgresql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/nkclarvikkommune1"
    
    print("Connecting to databases...")
    source_conn = await asyncpg.connect(source_db_url)
    target_conn = await asyncpg.connect(db_url)
    
    try:
        # Check how many recipe details exist in source
        source_count = await source_conn.fetchval('SELECT COUNT(*) FROM "tbl_rpKalkyledetaljer"')
        print(f"Found {source_count} recipe details in source database")
        
        # Clear existing details
        print("Clearing existing recipe details...")
        await target_conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
        
        # Get the structure of source details table
        source_cols = await source_conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = 'tbl_rpKalkyledetaljer'
            ORDER BY ordinal_position
        """)
        
        print(f"Source columns: {[col['column_name'] for col in source_cols[:15]]}...")
        
        # Check which recipes exist in target
        existing_recipes = await target_conn.fetch("SELECT kalkylekode FROM tbl_rpkalkyle")
        existing_recipe_ids = {r['kalkylekode'] for r in existing_recipes}
        print(f"Found {len(existing_recipe_ids)} recipes in target database")
        
        # Migrate details in batches
        batch_size = 500
        offset = 0
        total_migrated = 0
        skipped_orphans = 0
        errors = 0
        
        print("\nMigrating recipe details...")
        
        while True:
            # Fetch batch of details
            details = await source_conn.fetch(f"""
                SELECT * FROM "tbl_rpKalkyledetaljer"
                ORDER BY "tblKalkyleDetaljerID"
                LIMIT {batch_size} OFFSET {offset}
            """)
            
            if not details:
                break
            
            for detail in details:
                try:
                    # Check if the parent recipe exists
                    recipe_id = detail.get('Kalkylekode')
                    if recipe_id not in existing_recipe_ids:
                        skipped_orphans += 1
                        continue
                    
                    # Map the fields (handle case differences)
                    await target_conn.execute("""
                        INSERT INTO tbl_rpkalkyledetaljer (
                            tblkalkyledetaljerid, kalkylekode, produktid, produktnavn,
                            leverandorsproduktnr, pris, porsjonsmengde, enh,
                            totmeng, kostpris, visningsenhet, svinnprosent,
                            energikj, kalorier, fett, mettetfett, karbohydrater,
                            sukkerarter, kostfiber, protein, salt
                        ) VALUES (
                            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                            $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21
                        )
                        ON CONFLICT DO NOTHING
                    """,
                    detail.get('tblKalkyleDetaljerID'),
                    detail.get('Kalkylekode'),
                    detail.get('ProduktID'),
                    detail.get('Produktnavn') or detail.get('ProduktNavn'),
                    detail.get('LeverandørsProduktNr') or detail.get('LeverandorsProduktNr'),
                    detail.get('Pris'),
                    detail.get('Porsjonsmengde'),
                    detail.get('Enh'),
                    detail.get('TotMeng'),
                    detail.get('KostPris') or detail.get('kostPris'),
                    detail.get('VisningsEnhet'),
                    detail.get('SvinnProsent'),
                    detail.get('EnergiKJ'),
                    detail.get('Kalorier'),
                    detail.get('Fett'),
                    detail.get('MettetFett'),
                    detail.get('Karbohydrater'),
                    detail.get('Sukkerarter'),
                    detail.get('Kostfiber'),
                    detail.get('Protein'),
                    detail.get('Salt'))
                    
                    total_migrated += 1
                    
                except Exception as e:
                    errors += 1
                    if errors <= 5:
                        print(f"  Error: {e}")
            
            offset += batch_size
            if offset % 2000 == 0:
                print(f"  Processed {offset} records...")
        
        print(f"\nMigration complete:")
        print(f"  Successfully migrated: {total_migrated} recipe details")
        print(f"  Skipped (orphaned): {skipped_orphans} details")
        print(f"  Errors: {errors}")
        
        # Verify migration
        final_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyledetaljer")
        print(f"\nTotal recipe details in target: {final_count}")
        
        # Show some example recipes with ingredients
        samples = await target_conn.fetch("""
            SELECT DISTINCT k.kalkylekode, k.kalkylenavn, COUNT(d.tblkalkyledetaljerid) as ingredient_count
            FROM tbl_rpkalkyle k
            INNER JOIN tbl_rpkalkyledetaljer d ON k.kalkylekode = d.kalkylekode
            GROUP BY k.kalkylekode, k.kalkylenavn
            ORDER BY ingredient_count DESC
            LIMIT 10
        """)
        
        print("\nRecipes with most ingredients:")
        for sample in samples:
            print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} ({sample['ingredient_count']} ingredients)")
        
        # Show sample ingredients for a recipe
        if samples:
            recipe_id = samples[0]['kalkylekode']
            ingredients = await target_conn.fetch("""
                SELECT produktnavn, porsjonsmengde, enh, totmeng
                FROM tbl_rpkalkyledetaljer
                WHERE kalkylekode = $1
                ORDER BY produktnavn
                LIMIT 5
            """, recipe_id)
            
            print(f"\nSample ingredients for '{samples[0]['kalkylenavn']}':")
            for ing in ingredients:
                amount = f"{ing['porsjonsmengde']} {ing['enh']}" if ing['porsjonsmengde'] and ing['enh'] else "N/A"
                print(f"  - {ing['produktnavn']}: {amount}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await source_conn.close()
        await target_conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_recipe_details())