"""Populate recipe tables with test data."""
import asyncio
import asyncpg
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def populate_recipes():
    db_url = os.getenv('DATABASE_URL').replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    
    try:
        # First, ensure we have recipe groups
        existing_groups = await conn.fetch('SELECT gruppeid FROM tbl_rpkalkylegruppe')
        if not existing_groups:
            print("Creating recipe groups...")
            await conn.execute("""
                INSERT INTO tbl_rpkalkylegruppe (gruppeid, gruppenavn, merknad)
                VALUES 
                (1, 'Hovedretter', 'Varme hovedretter'),
                (2, 'Desserter', 'Søte desserter og kaker')
            """)
        
        # Insert sample recipes
        print("Inserting sample recipes...")
        recipes = [
            (1, 'Fiskegrateng med potet', 1, 'Klassisk fiskegrateng med kokte poteter', 4, 1),
            (2, 'Kjøttkaker i brun saus', 1, 'Tradisjonelle kjøttkaker med kålstuing', 4, 1),
            (3, 'Kylling tikka masala', 1, 'Indisk kyllingrett med ris', 4, 1),
            (4, 'Vegetar lasagne', 1, 'Lasagne med grønnsaker og ostesaus', 6, 1),
            (5, 'Laks med grønnsaker', 1, 'Ovnsbakt laks med rotgrønnsaker', 4, 1),
            (6, 'Eplekake med vaniljesaus', 2, 'Hjemmelaget eplekake', 8, 2),
            (7, 'Sjokoladepudding', 2, 'Kremet sjokoladepudding', 4, 2),
            (8, 'Fruktssalat', 2, 'Frisk fruktssalat med sesongfrukt', 4, 2),
        ]
        
        for recipe in recipes:
            await conn.execute("""
                INSERT INTO tbl_rpkalkyle (
                    kalkylekode, kalkylenavn, ansattid, informasjon, 
                    antallporsjoner, gruppeid, opprettetdato, enhet
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (kalkylekode) DO NOTHING
            """, recipe[0], recipe[1], recipe[2], recipe[3], recipe[4], recipe[5], datetime.now(), 'P')
        
        # Insert sample recipe details (ingredients)
        print("Inserting recipe ingredients...")
        
        # Get some products to use as ingredients
        products = await conn.fetch("""
            SELECT produktid, produktnavn 
            FROM tblprodukter 
            WHERE utgatt = false 
            LIMIT 20
        """)
        
        if products:
            # Add ingredients to recipes
            ingredient_count = 0
            recipe_ids = [1, 2, 3, 4, 5]  # First 5 recipes
            
            for recipe_id in recipe_ids:
                for i, product in enumerate(products[:5]):
                    # Generate unique ID
                    detail_id = (recipe_id * 1000) + i + 1
                    
                    await conn.execute("""
                        INSERT INTO tbl_rpkalkyledetaljer (
                            tblkalkyledetaljerid, kalkylekode, produktid, produktnavn,
                            porsjonsmengde, enh, totmeng
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        ON CONFLICT DO NOTHING
                    """, detail_id, recipe_id, product['produktid'], product['produktnavn'],
                        (i+1) * 100, 'g', (i+1) * 0.1)
                    ingredient_count += 1
            
            print(f"Added {ingredient_count} ingredients to recipes")
        
        # Verify data
        recipe_count = await conn.fetchval('SELECT COUNT(*) FROM tbl_rpkalkyle')
        print(f"\nTotal recipes in database: {recipe_count}")
        
        # Show sample recipes
        sample_recipes = await conn.fetch("""
            SELECT k.kalkylekode, k.kalkylenavn, k.gruppeid
            FROM tbl_rpkalkyle k
            LIMIT 5
        """)
        
        print("\nSample recipes:")
        for recipe in sample_recipes:
            print(f"  - {recipe['kalkylekode']}: {recipe['kalkylenavn']} (gruppe {recipe['gruppeid']})")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_recipes())