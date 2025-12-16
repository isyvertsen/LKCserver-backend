"""Fix the enhet column type in tbl_rpkalkyle to support multiple characters."""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def fix_enhet_column():
    db_url = os.getenv('DATABASE_URL').replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    
    try:
        print("Checking current column type...")
        
        # Check current column type
        col_info = await conn.fetchrow("""
            SELECT data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = 'tbl_rpkalkyle'
            AND column_name = 'enhet'
        """)
        
        print(f"Current type: {col_info['data_type']} ({col_info['character_maximum_length']})")
        
        if col_info['data_type'] == 'character' and col_info['character_maximum_length'] == 1:
            print("Column needs to be fixed. Altering column type...")
            
            # Alter the column type
            await conn.execute("""
                ALTER TABLE tbl_rpkalkyle 
                ALTER COLUMN enhet TYPE varchar(50)
            """)
            
            print("Column type changed to varchar(50)")
            
            # Verify the change
            new_col_info = await conn.fetchrow("""
                SELECT data_type, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'tbl_rpkalkyle'
                AND column_name = 'enhet'
            """)
            
            print(f"New type: {new_col_info['data_type']} ({new_col_info['character_maximum_length']})")
        else:
            print("Column type is already correct")
        
        # Now re-run the recipe migration to get all recipes
        print("\nRe-running recipe migration with fixed column...")
        
        # Connect to source database
        from urllib.parse import urlparse
        parsed = urlparse(db_url)
        source_db_url = f"postgresql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/nkclarvikkommune1"
        source_conn = await asyncpg.connect(source_db_url)
        
        try:
            # Clear existing data
            print("Clearing existing recipes...")
            await conn.execute("DELETE FROM tbl_rpkalkyledetaljer")
            await conn.execute("DELETE FROM tbl_rpkalkyle")
            
            # Migrate recipes again
            print("Migrating recipes...")
            recipes = await source_conn.fetch('SELECT * FROM "tbl_rpKalkyle"')
            
            migrated = 0
            failed = 0
            
            for recipe in recipes:
                try:
                    await conn.execute("""
                        INSERT INTO tbl_rpkalkyle (
                            kalkylekode, kalkylenavn, ansattid, opprettetdato, 
                            revidertdato, informasjon, refporsjon, kategorikode,
                            antallporsjoner, produksjonsmetode, gruppeid, alergi,
                            leveringsdato, merknad, brukestil, enhet, naeringsinnhold, twporsjon
                        ) VALUES (
                            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 
                            $11, $12, $13, $14, $15, $16, $17, $18
                        )
                        ON CONFLICT (kalkylekode) DO UPDATE SET
                            kalkylenavn = EXCLUDED.kalkylenavn,
                            enhet = EXCLUDED.enhet,
                            antallporsjoner = EXCLUDED.antallporsjoner,
                            informasjon = EXCLUDED.informasjon,
                            brukestil = EXCLUDED.brukestil
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
                    recipe.get('Enhet'),  # This should now accept longer values
                    recipe.get('Naeringsinnhold'),
                    recipe.get('TwPorsjon'))
                    
                    migrated += 1
                    
                except Exception as e:
                    failed += 1
                    if failed <= 5:  # Only print first 5 errors
                        print(f"  Error migrating recipe {recipe.get('Kalkylekode')}: {e}")
            
            print(f"\nMigration complete:")
            print(f"  Successfully migrated: {migrated} recipes")
            print(f"  Failed: {failed} recipes")
            
            # Show some examples with units
            samples = await conn.fetch("""
                SELECT kalkylekode, kalkylenavn, enhet, antallporsjoner
                FROM tbl_rpkalkyle
                WHERE enhet IS NOT NULL AND enhet != ''
                ORDER BY kalkylekode
                LIMIT 10
            """)
            
            if samples:
                print("\nSample recipes with units:")
                for sample in samples:
                    print(f"  - {sample['kalkylekode']}: {sample['kalkylenavn']} - {sample['enhet']}")
            
        finally:
            await source_conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_enhet_column())