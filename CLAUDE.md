# Claude Memory - Catering System

## Important Database Information

### Product Tables Distinction
**IMPORTANT**: There are two different product-related tables in the system that serve different purposes:

1. **`matinfo_products` table** (in matinfo_products.py model as `MatinfoProduct`):
   - **READ-ONLY lookup table** from Matinfo.no
   - Contains Norwegian food product reference data
   - Used ONLY for looking up nutritional information and allergen data
   - Has detailed product information including:
     - GTIN codes (EAN-koder)
     - Allergen information (`matinfo_allergens` table)
     - Nutritional data (`matinfo_nutrients` table)
     - Brand names, producer names
     - Ingredient statements
   - Located in the matinfo_products module
   - Synchronized from Matinfo.no via API (tracked in `matinfo_gtin_updates` and `matinfo_sync_logs` tables)

2. **`tblprodukter` table** (in produkter.py model as `Produkter`):
   - **This is the MAIN internal product catalog**
   - Used for the catering system's own product management
   - Contains pricing, inventory, and category information
   - Does NOT have nutritional or allergen data (these columns were removed)
   - Used in menu planning and order management
   - Can link to Matinfo products via `ean_kode` field

### Key Differences:
- `matinfo_*` tables = External lookup data from Matinfo.no (read-only reference)
- `tblprodukter` = Main internal product catalog (what you manage/sell in the catering system)

### Matinfo Tables:
- `matinfo_products` - Main product information
- `matinfo_nutrients` - Nutritional data per product
- `matinfo_allergens` - Allergen information per product
- `matinfo_gtin_updates` - Tracks GTIN updates from Matinfo API
- `matinfo_sync_logs` - Synchronization history and error logs

## Recent Changes

### Naming Conventions and File Structure (2025-10-22)
**IMPORTANT**: Established consistent naming conventions:

**File Naming:**
- Python files: Use underscores (`kunde_gruppe.py`, `meny_produkt.py`, `periode_meny.py`)
- Models, schemas, and API files all follow this pattern

**URL/Endpoint Naming:**
- API endpoints: Use hyphens (`/kunde-gruppe`, `/meny-produkt`, `/periode-meny`)
- Example: `kunde_gruppe.py` → endpoint `/kunde-gruppe`

**Class Naming:**
- Always PascalCase (`KundeGruppe`, `MenyProdukt`, `PeriodeMeny`)
- Matinfo models prefixed: `MatinfoProduct`, `MatinfoAllergen`, `MatinfoNutrient`

**Files Renamed:**
- `askony.py` → `asko_ny.py` (endpoint: `/asko-ny-produkter`)
- `kundegruppe.py` → `kunde_gruppe.py` (endpoint: `/kunde-gruppe`)
- `menyprodukt.py` → `meny_produkt.py` (endpoint: `/meny-produkt`)
- `periodemeny.py` → `periode_meny.py` (endpoint: `/periode-meny`)
- `rpkalkyle.py` → `oppskrifter.py` (endpoint: `/oppskrifter`)

**Deleted Duplicate Files:**
- `kalkyle.py` - Duplicate recipe implementation
- `recipes.py` - English duplicate
- `kalkyle_service.py` - Unused service
- `rpkalkyle_v2.py` - Unused refactored version

### Matinfo Tables Rename (2025-10-22)
Tables renamed to clearly distinguish from internal products:
- `products` → `matinfo_products`
- `nutrients` → `matinfo_nutrients`
- `allergens` → `matinfo_allergens`

Models renamed:
- `Product` → `MatinfoProduct`
- `Nutrient` → `MatinfoNutrient`
- `Allergen` → `MatinfoAllergen`

### Removed Columns from tblprodukter (2025-07-03)
The following columns were removed from the `tblprodukter` table and should not be included in the model:
- allergenprodukt
- energikj
- kalorier
- fett
- mettetfett
- karbohydrater
- sukkerarter
- kostfiber
- protein
- salt
- monodisakk
- matvareid
- webshopsted

### Export Functionality
- Added support for exporting products in three formats:
  - JSON (single file)
  - JSONL (multiple files, 100 products each)
  - Markdown (one file per product)
- Exports can be downloaded as ZIP files
- Frontend integration completed with ProductExport component

## Testing

### Test Database
- Test database: `catering_test` (separate from development database)
- Configuration: `backend/.env.test`
- Seed script: `backend/tests/seed_data.py`

**Setup test database:**
```bash
cd backend
uv run python tests/seed_data.py
```

**Test data includes:**
- 3 leverandører (Tine SA, Eget Kjøkken, Kavli AS)
- 5 kategorier
- 5 produkter (3 with GTIN, 2 without)
- 4 Matinfo products with allergens and nutrients

**Run backend with test database:**
```bash
cd backend
./run_test_server.sh
```

### E2E Testing with Playwright
- Tests located in: `frontend/e2e/`
- Configuration: `frontend/playwright.config.ts`
- Frontend runs on port 3001, backend on port 8000
- See TESTING.md for comprehensive testing guide

**Run E2E tests:**
```bash
cd frontend
npx playwright test
```

## Development Notes

### Database Migrations
**IMPORTANT**: Always add new migrations to the existing migration system in `app/core/migrations.py`
- The application automatically runs migrations on startup
- DO NOT use Alembic for migrations - use the custom migration system
- Add new migration classes that inherit from `Migration`
- Register migrations in `get_migration_runner()` function
- Migrations are tracked in the `_migrations` table

### API Configuration
- Backend runs on port 8000
- Frontend expects API at http://localhost:8000/api
- CORS is configured for http://localhost:3000
- Auth bypass is enabled for development

### Commands to Run
- Lint: `npm run lint`
- Type check: `npm run typecheck`

### Git Configuration
- Consolidated .gitignore at root level
- Export catalog (`backend/exportcatalog/`) is excluded from version control
- All export files and zip archives are automatically ignored