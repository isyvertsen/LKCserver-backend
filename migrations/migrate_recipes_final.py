"""Final migration script for recipes from nkclarvikkommune1 database."""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

async def migrate_recipes():
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
        # Clear existing data
        print("\nClearing existing data...")
        await target_conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
        await target_conn.execute("DELETE FROM tbl_rpkalkyle")
        await target_conn.execute("DELETE FROM tbl_rpkalkylegruppe")
        
        # 1. Migrate recipe groups
        print("\nMigrating recipe groups...")
        groups = await source_conn.fetch('SELECT * FROM "tbl_rpKalkyleGruppe"')
        
        for group in groups:
            await target_conn.execute("""
                INSERT INTO tbl_rpkalkylegruppe (gruppeid, kalykegruppenavn)
                VALUES ($1, $2)
                ON CONFLICT (gruppeid) DO UPDATE SET
                    kalykegruppenavn = EXCLUDED.kalykegruppenavn
            """, group['GruppeID'], group.get('KalykeGruppeNavn'))
        
        print(f"  Migrated {len(groups)} recipe groups")
        
        # 2. Migrate recipes with column mapping
        print("\nMigrating recipes...")
        
        # Get the actual columns from source
        source_cols = await source_conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'tbl_rpKalkyle'
            ORDER BY ordinal_position
        """)
        
        print(f"Source columns: {[col['column_name'] for col in source_cols[:10]]}...")
        
        # Fetch all recipes
        recipes = await source_conn.fetch('SELECT * FROM "tbl_rpKalkyle"')
        
        migrated = 0
        for recipe in recipes:
            try:
                # Map the columns - use get() to handle missing columns
                await target_conn.execute("""
                    INSERT INTO tbl_rpkalkyle (
                        kalkylekode, kalkylenavn, ansattid, opprettetdato, 
                        revidertdato, informasjon, refporsjon, kategorikode,
                        antallporsjoner, produksjonsmetode, gruppeid, alergi,
                        leveringsdato, merknad, brukestil, enhet, naeringsinnhold, twporsjon
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 
                        $11, $12, $13, $14, $15, $16, $17, $18
                    )
                    ON CONFLICT (kalkylekode) DO NOTHING
                """,
                recipe.get('Kalkylekode'),
                recipe.get('KalyleNavn') or recipe.get('Kalkylenavn'),
                recipe.get('AnsattID'),
                recipe.get('OpprettetDato'),
                recipe.get('RevidertDato'),
                recipe.get('Informasjon'),
                recipe.get('RefPorsjon'),
                recipe.get('Kategorikode'),
                recipe.get('AntallPorsjoner'),
                recipe.get('Produksjonsmetode'),
                recipe.get('GruppeID'),
                recipe.get('Alergi'),
                recipe.get('LeveringsDato'),
                recipe.get('Merknad'),
                recipe.get('BrukesTil'),
                recipe.get('Enhet'),
                recipe.get('Naeringsinnhold'),
                recipe.get('TwPorsjon'))
                
                migrated += 1
                
            except Exception as e:
                print(f"  Error migrating recipe {recipe.get('Kalkylekode')}: {e}")
        
        print(f"  Migrated {migrated} recipes")
        
        # 3. Migrate recipe details
        print("\nMigrating recipe details...")
        
        # Get detail columns
        detail_cols = await source_conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'tbl_rpKalkyledetaljer'
            ORDER BY ordinal_position
        """)
        
        print(f"Detail columns: {[col['column_name'] for col in detail_cols[:10]]}...")
        
        # Migrate in batches
        batch_size = 500
        offset = 0
        total_details = 0
        
        while True:
            details = await source_conn.fetch(f"""
                SELECT * FROM "tbl_rpKalkyledetaljer"
                ORDER BY "tblKalkyledetaljerID"
                LIMIT {batch_size} OFFSET {offset}
            """)
            
            if not details:
                break
            
            for detail in details:
                try:
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
                    detail.get('tblKalkyledetaljerID'),
                    detail.get('Kalkylekode'),
                    detail.get('ProduktID'),
                    detail.get('ProduktNavn'),
                    detail.get('LeverandorsProduktNr'),
                    detail.get('Pris'),
                    detail.get('Porsjonsmengde'),
                    detail.get('Enh'),
                    detail.get('TotMeng'),
                    detail.get('KostPris'),
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
                    
                    total_details += 1
                    
                except Exception as e:
                    pass  # Skip individual errors
            
            offset += batch_size
            print(f"  Processed {offset} details...")
        
        print(f"  Total details migrated: {total_details}")
        
        # Verify migration
        print("\nVerifying migration...")
        final_group_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkylegruppe")
        final_recipe_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyle")
        final_detail_count = await target_conn.fetchval("SELECT COUNT(*) FROM tbl_rpkalkyledetaljer")
        
        print(f"\nFinal counts:")
        print(f"  - Recipe groups: {final_group_count}")
        print(f"  - Recipes: {final_recipe_count}")
        print(f"  - Recipe details: {final_detail_count}")
        
        # Show samples
        if final_recipe_count > 0:
            samples = await target_conn.fetch("""
                SELECT k.kalkylekode, k.kalkylenavn, k.antallporsjoner, g.kalykegruppenavn
                FROM tbl_rpkalkyle k
                LEFT JOIN tbl_rpkalkylegruppe g ON k.gruppeid = g.gruppeid
                ORDER BY k.kalkylekode
                LIMIT 10
            """)
            
            print("\nSample recipes:")
            for sample in samples:
                portions = sample['antallporsjoner'] or 'N/A'
                group = sample['kalykegruppenavn'] or 'No group'
                print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} ({portions} porsjoner) - {group}")
        
        print("\nMigration completed!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await source_conn.close()
        await target_conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_recipes())