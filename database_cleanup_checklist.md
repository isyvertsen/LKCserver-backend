# Database Schema Cleanup Checklist
Generated: 2025-07-01 21:43:58

## Instructions
1. Mark columns you want to **REMOVE** with [x]
2. Add new table names in parentheses after current names
3. Add any notes about data migration in the comments section
4. Tables marked with [x] will be DROPPED entirely

## Summary
- Total Tables: 84
- Total Columns: 967

---

## Tables to Drop

- [ ] `account`
- [ ] `allergens`
- [ ] `askony`
- [ ] `eventlog`
- [ ] `inn`
- [ ] `lagringsfeil_ved_autokorrigering_av_navn`
- [ ] `matvarer`
- [ ] `mottakskjokkenitems`
- [ ] `msyscompacterror`
- [ ] `nutrients`
- [ ] `products`
- [ ] `qrytmpordrebestillingtest`
- [ ] `session`
- [ ] `sysdiagrams`
- [ ] `tbl_identepostkobling`
- [ ] `tbl_rpembalasje`
- [ ] `tbl_rpkalkyldetaljer_tblallergener`
- [ ] `tbl_rpkalkyle`
- [ ] `tbl_rpkalkyledetaljer`
- [ ] `tbl_rpkalkylegruppe`
- [ ] `tbl_rpproduksjon`
- [ ] `tbl_rpproduksjondetaljer`
- [ ] `tbl_rptabenheter`
- [ ] `tbl_systemverdier`
- [ ] `tblaccessmenyer`
- [ ] `tblallergener`
- [ ] `tblansatte`
- [ ] `tblasko`
- [ ] `tblbestillinger`
- [ ] `tblbestillingsposter`
- [ ] `tblbetalingsmate`
- [ ] `tblgarnetyr`
- [ ] `tblkalkyleallergen`
- [ ] `tblkategorier`
- [ ] `tblkjopsordredetaljer`
- [ ] `tblkjopsordrer`
- [ ] `tblkjopsordrestatus`
- [ ] `tblkontaktpersoner`
- [ ] `tblkontonummer`
- [ ] `tblkunde_kundeinfoprodukt`
- [ ] `tblkundeinfoprodukt`
- [ ] `tblkunder`
- [ ] `tblkundersomikkeharbestilt`
- [ ] `tblkundgruppe`
- [ ] `tbllagerlokasjon`
- [ ] `tbllagertransaksjoner`
- [ ] `tbllagertransaksjonstyper`
- [ ] `tbllevbestillinger`
- [ ] `tbllevbestillingshode`
- [ ] `tblleverandorer`
- [ ] `tblleveringsdag`
- [ ] `tbllog`
- [ ] `tblmeny`
- [ ] `tblmenygruppe`
- [ ] `tblmenyprodukt`
- [ ] `tblmenysykehjem`
- [ ] `tblmva`
- [ ] `tblmva_kundekategori`
- [ ] `tblneringstabellen`
- [ ] `tblordredetaljer`
- [ ] `tblordrer`
- [ ] `tblordrestatus`
- [ ] `tblperiode`
- [ ] `tblperiodemeny`
- [ ] `tblprodukt_allergen`
- [ ] `tblprodukter`
- [ ] `tblruteplan`
- [ ] `tblsone`
- [ ] `tbltmpkundergruppeordre`
- [ ] `tbltmpordre`
- [ ] `tbltmpordrebestilling`
- [ ] `tbltmpordrebestillingsykehjem`
- [ ] `tblvarebestillingbekreftelseasko`
- [ ] `tblvaremottak`
- [ ] `test`
- [ ] `tmpordredetaljer`
- [ ] `tmpordredetaljer2`
- [ ] `tmpproduksjonsordre`
- [ ] `tmpproduksjonsordredetaljer`
- [ ] `tmptblkundersomikkeharbestilt`
- [ ] `tsttbl2`
- [ ] `user`
- [ ] `users`
- [ ] `verificationtoken`

---

## Table: `account` → (new name: _______________)

**Primary Key:** id

**Foreign Keys:**
- `userid` → `user(id)` [account_userid_fkey]

**Indexes:**
- `account_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - character varying(1000), NOT NULL
- [ ] `userid` - character varying(1000), NOT NULL
- [ ] `type` - character varying(1000), NOT NULL
- [ ] `provider` - character varying(1000), NOT NULL
- [ ] `provideraccountid` - character varying(1000), NOT NULL
- [ ] `refresh_token` - text, NULL
- [ ] `access_token` - text, NULL
- [ ] `expires_at` - int4, NULL
- [ ] `token_type` - character varying(1000), NULL
- [ ] `scope` - character varying(1000), NULL
- [ ] `id_token` - text, NULL
- [ ] `session_state` - character varying(1000), NULL

### Column Mapping (old → new):
```
id → 
userid → 
type → 
provider → 
provideraccountid → 
refresh_token → 
access_token → 
expires_at → 
token_type → 
scope → 
id_token → 
session_state → 
```

### Migration Notes:
_____________________________

---

## Table: `allergens` → (new name: _______________)

**Primary Key:** allergenid, code

**Foreign Keys:**
- `productid` → `products(id)` [fk_allergens_products]

**Indexes:**
- `allergens_pkey` on (allergenid, code) (UNIQUE)

### Columns to Remove:

- [ ] `allergenid` - int4, NOT NULL
- [ ] `productid` - character varying(24), NOT NULL
- [ ] `level` - int4, NULL
- [ ] `code` - character varying(50), NOT NULL
- [ ] `name` - character varying(255), NULL

### Column Mapping (old → new):
```
allergenid → 
productid → 
level → 
code → 
name → 
```

### Migration Notes:
_____________________________

---

## Table: `askony` → (new name: _______________)

**Primary Key:** epdnummer

**Indexes:**
- `askony_pkey` on (epdnummer) (UNIQUE)

### Columns to Remove:

- [ ] `epdnummer` - character varying(255), NOT NULL
- [ ] `eannummer` - character varying(255), NULL
- [ ] `varenavn` - character varying(255), NULL

### Column Mapping (old → new):
```
epdnummer → 
eannummer → 
varenavn → 
```

### Migration Notes:
_____________________________

---

## Table: `eventlog` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `eventlog_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int8, NOT NULL
- [ ] `created` - timestamp, NOT NULL, DEFAULT: CURRENT_TIMESTAMP
- [ ] `eventtype` - character(1), NOT NULL
- [ ] `eventvalue` - character(1), NOT NULL

### Column Mapping (old → new):
```
id → 
created → 
eventtype → 
eventvalue → 
```

### Migration Notes:
_____________________________

---

## Table: `inn` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `inn_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `felt1` - character varying(255), NULL
- [ ] `felt2` - int4, NULL
- [ ] `felt3` - int4, NULL
- [ ] `felt4` - character varying(255), NULL
- [ ] `felt5` - int4, NULL
- [ ] `felt6` - int4, NULL
- [ ] `felt7` - character varying(255), NULL

### Column Mapping (old → new):
```
id → 
felt1 → 
felt2 → 
felt3 → 
felt4 → 
felt5 → 
felt6 → 
felt7 → 
```

### Migration Notes:
_____________________________

---

## Table: `lagringsfeil_ved_autokorrigering_av_navn` → (new name: _______________)

### Columns to Remove:

- [ ] `objektnavn` - character varying(255), NULL
- [ ] `objekttype` - character varying(255), NULL
- [ ] `feilarsak` - character varying(255), NULL
- [ ] `klokkeslett` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP

### Column Mapping (old → new):
```
objektnavn → 
objekttype → 
feilarsak → 
klokkeslett → 
```

### Migration Notes:
_____________________________

---

## Table: `matvarer` → (new name: _______________)

### Columns to Remove:

- [ ] `f1` - character varying(255), NULL
- [ ] `den_norske_matvaretabellen_2018` - character varying(255), NULL
- [ ] `f3` - character varying(255), NULL
- [ ] `f4` - character varying(255), NULL
- [ ] `f5` - character varying(255), NULL
- [ ] `f6` - character varying(255), NULL
- [ ] `f7` - character varying(255), NULL
- [ ] `f8` - character varying(255), NULL
- [ ] `f9` - character varying(255), NULL
- [ ] `f10` - character varying(255), NULL
- [ ] `f11` - character varying(255), NULL
- [ ] `f12` - character varying(255), NULL
- [ ] `f13` - character varying(255), NULL
- [ ] `f14` - character varying(255), NULL
- [ ] `f15` - character varying(255), NULL
- [ ] `f16` - character varying(255), NULL
- [ ] `f17` - character varying(255), NULL
- [ ] `f18` - character varying(255), NULL
- [ ] `f19` - character varying(255), NULL
- [ ] `f20` - character varying(255), NULL
- [ ] `f21` - character varying(255), NULL
- [ ] `f22` - character varying(255), NULL
- [ ] `f23` - character varying(255), NULL
- [ ] `f24` - character varying(255), NULL
- [ ] `f25` - character varying(255), NULL
- [ ] `f26` - character varying(255), NULL
- [ ] `f27` - character varying(255), NULL
- [ ] `f28` - character varying(255), NULL
- [ ] `f29` - character varying(255), NULL
- [ ] `f30` - character varying(255), NULL
- [ ] `f31` - character varying(255), NULL
- [ ] `f32` - character varying(255), NULL
- [ ] `f33` - character varying(255), NULL
- [ ] `f34` - character varying(255), NULL
- [ ] `f35` - character varying(255), NULL
- [ ] `f36` - character varying(255), NULL
- [ ] `f37` - character varying(255), NULL
- [ ] `f38` - character varying(255), NULL
- [ ] `f39` - character varying(255), NULL
- [ ] `f40` - character varying(255), NULL
- [ ] `f41` - character varying(255), NULL
- [ ] `f42` - character varying(255), NULL
- [ ] `f43` - character varying(255), NULL
- [ ] `f44` - character varying(255), NULL
- [ ] `f45` - character varying(255), NULL
- [ ] `f46` - character varying(255), NULL
- [ ] `f47` - character varying(255), NULL
- [ ] `f48` - character varying(255), NULL
- [ ] `f49` - character varying(255), NULL
- [ ] `f50` - character varying(255), NULL
- [ ] `f51` - character varying(255), NULL
- [ ] `f52` - character varying(255), NULL
- [ ] `f53` - character varying(255), NULL
- [ ] `f54` - character varying(255), NULL
- [ ] `f55` - character varying(255), NULL
- [ ] `f56` - character varying(255), NULL
- [ ] `f57` - character varying(255), NULL
- [ ] `f58` - character varying(255), NULL
- [ ] `f59` - character varying(255), NULL
- [ ] `f60` - character varying(255), NULL
- [ ] `f61` - character varying(255), NULL
- [ ] `f62` - character varying(255), NULL
- [ ] `f63` - character varying(255), NULL
- [ ] `f64` - character varying(255), NULL
- [ ] `f65` - character varying(255), NULL
- [ ] `f66` - character varying(255), NULL
- [ ] `f67` - character varying(255), NULL
- [ ] `f68` - character varying(255), NULL
- [ ] `f69` - character varying(255), NULL
- [ ] `f70` - character varying(255), NULL
- [ ] `f71` - character varying(255), NULL
- [ ] `f72` - character varying(255), NULL
- [ ] `f73` - character varying(255), NULL
- [ ] `f74` - character varying(255), NULL
- [ ] `f75` - character varying(255), NULL
- [ ] `f76` - character varying(255), NULL
- [ ] `f77` - character varying(255), NULL
- [ ] `f78` - character varying(255), NULL
- [ ] `f79` - character varying(255), NULL
- [ ] `f80` - character varying(255), NULL
- [ ] `f81` - character varying(255), NULL
- [ ] `f82` - character varying(255), NULL
- [ ] `f83` - character varying(255), NULL
- [ ] `f84` - character varying(255), NULL
- [ ] `f85` - character varying(255), NULL
- [ ] `f86` - character varying(255), NULL
- [ ] `f87` - character varying(255), NULL
- [ ] `f88` - character varying(255), NULL
- [ ] `f89` - character varying(255), NULL
- [ ] `f90` - character varying(255), NULL
- [ ] `f91` - character varying(255), NULL
- [ ] `f92` - character varying(255), NULL
- [ ] `f93` - character varying(255), NULL
- [ ] `f94` - character varying(255), NULL
- [ ] `f95` - character varying(255), NULL
- [ ] `f96` - character varying(255), NULL
- [ ] `f97` - character varying(255), NULL
- [ ] `f98` - character varying(255), NULL
- [ ] `f99` - character varying(255), NULL
- [ ] `f100` - character varying(255), NULL
- [ ] `f101` - character varying(255), NULL
- [ ] `f102` - character varying(255), NULL
- [ ] `f103` - character varying(255), NULL
- [ ] `f104` - character varying(255), NULL
- [ ] `f105` - character varying(255), NULL
- [ ] `f106` - character varying(255), NULL
- [ ] `f107` - character varying(255), NULL
- [ ] `f108` - character varying(255), NULL
- [ ] `f109` - character varying(255), NULL
- [ ] `f110` - character varying(255), NULL
- [ ] `f111` - character varying(255), NULL
- [ ] `f112` - character varying(255), NULL
- [ ] `f113` - character varying(255), NULL
- [ ] `f114` - character varying(255), NULL
- [ ] `f115` - character varying(255), NULL
- [ ] `f116` - character varying(255), NULL
- [ ] `f117` - character varying(255), NULL
- [ ] `f118` - character varying(255), NULL
- [ ] `f119` - character varying(255), NULL

### Column Mapping (old → new):
```
f1 → 
den_norske_matvaretabellen_2018 → 
f3 → 
f4 → 
f5 → 
f6 → 
f7 → 
f8 → 
f9 → 
f10 → 
f11 → 
f12 → 
f13 → 
f14 → 
f15 → 
f16 → 
f17 → 
f18 → 
f19 → 
f20 → 
f21 → 
f22 → 
f23 → 
f24 → 
f25 → 
f26 → 
f27 → 
f28 → 
f29 → 
f30 → 
f31 → 
f32 → 
f33 → 
f34 → 
f35 → 
f36 → 
f37 → 
f38 → 
f39 → 
f40 → 
f41 → 
f42 → 
f43 → 
f44 → 
f45 → 
f46 → 
f47 → 
f48 → 
f49 → 
f50 → 
f51 → 
f52 → 
f53 → 
f54 → 
f55 → 
f56 → 
f57 → 
f58 → 
f59 → 
f60 → 
f61 → 
f62 → 
f63 → 
f64 → 
f65 → 
f66 → 
f67 → 
f68 → 
f69 → 
f70 → 
f71 → 
f72 → 
f73 → 
f74 → 
f75 → 
f76 → 
f77 → 
f78 → 
f79 → 
f80 → 
f81 → 
f82 → 
f83 → 
f84 → 
f85 → 
f86 → 
f87 → 
f88 → 
f89 → 
f90 → 
f91 → 
f92 → 
f93 → 
f94 → 
f95 → 
f96 → 
f97 → 
f98 → 
f99 → 
f100 → 
f101 → 
f102 → 
f103 → 
f104 → 
f105 → 
f106 → 
f107 → 
f108 → 
f109 → 
f110 → 
f111 → 
f112 → 
f113 → 
f114 → 
f115 → 
f116 → 
f117 → 
f118 → 
f119 → 
```

### Migration Notes:
_____________________________

---

## Table: `mottakskjokkenitems` → (new name: _______________)

### Columns to Remove:

- [ ] `mottakskjokken` - text, NULL
- [ ] `linjenr` - int8, NULL
- [ ] `produksjonskode` - int8, NULL
- [ ] `dag` - int8, NULL
- [ ] `produktid` - int8, NULL
- [ ] `varenavn` - text, NULL
- [ ] `pris` - text, NULL
- [ ] `antallporsjoner` - text, NULL
- [ ] `porsjonsmengde` - text, NULL
- [ ] `enh` - text, NULL

### Column Mapping (old → new):
```
mottakskjokken → 
linjenr → 
produksjonskode → 
dag → 
produktid → 
varenavn → 
pris → 
antallporsjoner → 
porsjonsmengde → 
enh → 
```

### Migration Notes:
_____________________________

---

## Table: `msyscompacterror` → (new name: _______________)

### Columns to Remove:

- [ ] `errorcode` - int4, NULL
- [ ] `errordescription` - text, NULL
- [ ] `errorrecid` - bytea, NULL
- [ ] `errortable` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
errorcode → 
errordescription → 
errorrecid → 
errortable → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `nutrients` → (new name: _______________)

**Primary Key:** nutrientid, code

**Foreign Keys:**
- `productid` → `products(id)` [fk_nutrients_products]

**Indexes:**
- `nutrients_pkey` on (nutrientid, code) (UNIQUE)

### Columns to Remove:

- [ ] `nutrientid` - int4, NOT NULL
- [ ] `productid` - character varying(24), NOT NULL
- [ ] `code` - character varying(50), NOT NULL
- [ ] `measurement` - numeric, NULL
- [ ] `measurementprecision` - character varying(50), NULL
- [ ] `measurementtype` - character varying(50), NULL
- [ ] `name` - character varying(255), NULL

### Column Mapping (old → new):
```
nutrientid → 
productid → 
code → 
measurement → 
measurementprecision → 
measurementtype → 
name → 
```

### Migration Notes:
_____________________________

---

## Table: `products` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `products_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - character varying(24), NOT NULL
- [ ] `gtin` - character varying(20), NULL
- [ ] `name` - character varying(255), NULL
- [ ] `itemnumber` - character varying(50), NULL
- [ ] `epdnumber` - character varying(50), NULL
- [ ] `producername` - character varying(255), NULL
- [ ] `providername` - character varying(255), NULL
- [ ] `brandname` - character varying(255), NULL
- [ ] `ingredientstatement` - text, NULL
- [ ] `producturl` - character varying(500), NULL
- [ ] `markings` - text, NULL
- [ ] `images` - text, NULL
- [ ] `packagesize` - character varying(100), NULL

### Column Mapping (old → new):
```
id → 
gtin → 
name → 
itemnumber → 
epdnumber → 
producername → 
providername → 
brandname → 
ingredientstatement → 
producturl → 
markings → 
images → 
packagesize → 
```

### Migration Notes:
_____________________________

---

## Table: `qrytmpordrebestillingtest` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `qrytmpordrebestillingtest_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `felt1` - character varying(255), NULL
- [ ] `felt2` - character varying(255), NULL
- [ ] `felt3` - character varying(255), NULL
- [ ] `felt4` - character varying(255), NULL
- [ ] `felt5` - character varying(255), NULL

### Column Mapping (old → new):
```
id → 
felt1 → 
felt2 → 
felt3 → 
felt4 → 
felt5 → 
```

### Migration Notes:
_____________________________

---

## Table: `session` → (new name: _______________)

**Primary Key:** id

**Foreign Keys:**
- `userid` → `user(id)` [session_userid_fkey]

**Indexes:**
- `session_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - character varying(1000), NOT NULL
- [ ] `sessiontoken` - character varying(1000), NOT NULL
- [ ] `userid` - character varying(1000), NOT NULL
- [ ] `expires` - timestamp, NOT NULL

### Column Mapping (old → new):
```
id → 
sessiontoken → 
userid → 
expires → 
```

### Migration Notes:
_____________________________

---

## Table: `sysdiagrams` → (new name: _______________)

**Primary Key:** diagram_id

**Indexes:**
- `PK__sysdiagr__C2B05B615059E4D7` on (diagram_id) (UNIQUE)
- `UK_principal_name` on (name, principal_id) (UNIQUE)
- `sysdiagrams_pkey` on (diagram_id) (UNIQUE)

### Columns to Remove:

- [ ] `name` - text, NULL
- [ ] `principal_id` - int8, NULL
- [ ] `diagram_id` - int8, NOT NULL
- [ ] `version` - int8, NULL
- [ ] `definition` - text, NULL

### Column Mapping (old → new):
```
name → 
principal_id → 
diagram_id → 
version → 
definition → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_identepostkobling` → (new name: _______________)

**Primary Key:** ident

**Indexes:**
- `tbl_identepostkobling_pkey` on (ident) (UNIQUE)

### Columns to Remove:

- [ ] `ident` - character varying(256), NOT NULL
- [ ] `epost` - character varying(256), NOT NULL

### Column Mapping (old → new):
```
ident → 
epost → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpembalasje` → (new name: _______________)

**Primary Key:** embalasjeid

**Indexes:**
- `tbl_rpembalasje_pkey` on (embalasjeid) (UNIQUE)

### Columns to Remove:

- [ ] `embalasjeid` - int4, NOT NULL
- [ ] `beskrivelse` - character(1), NOT NULL
- [ ] `holdbarhetsdager` - int4, NOT NULL

### Column Mapping (old → new):
```
embalasjeid → 
beskrivelse → 
holdbarhetsdager → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpkalkyldetaljer_tblallergener` → (new name: _______________)

**Primary Key:** kalkyledetaljer_tblkalkyledetaljerid, allergener_allergenid

**Foreign Keys:**
- `allergener_allergenid` → `tblallergener(allergenid)` [fk_tbl_rpkalkyldetaljer_tblallergener_tblallergener]

**Indexes:**
- `tbl_rpkalkyldetaljer_tblallergener_pkey` on (kalkyledetaljer_tblkalkyledetaljerid, allergener_allergenid) (UNIQUE)

### Columns to Remove:

- [ ] `kalkyledetaljer_tblkalkyledetaljerid` - int4, NOT NULL
- [ ] `allergener_allergenid` - int4, NOT NULL

### Column Mapping (old → new):
```
kalkyledetaljer_tblkalkyledetaljerid → 
allergener_allergenid → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpkalkyle` → (new name: _______________)

**Primary Key:** kalkylekode

**Foreign Keys:**
- `gruppeid` → `tbl_rpkalkylegruppe(gruppeid)` [fk_tbl_rpkalkyle_tbl_rpkalkylegruppe]
- `ansattid` → `tblansatte(ansattid)` [fk_tbl_rpkalkyle_tblansatte]

**Indexes:**
- `tbl_rpkalkyle_pkey` on (kalkylekode) (UNIQUE)

### Columns to Remove:

- [ ] `kalkylekode` - int4, NOT NULL
- [ ] `kalkylenavn` - character varying(255), NULL
- [ ] `ansattid` - int4, NOT NULL
- [ ] `opprettetdato` - timestamp, NULL
- [ ] `revidertdato` - timestamp, NULL
- [ ] `informasjon` - text, NULL
- [ ] `refporsjon` - character varying(255), NULL
- [ ] `kategorikode` - character varying(255), NULL
- [ ] `antallporsjoner` - int4, NULL
- [ ] `produksjonsmetode` - character varying(255), NULL
- [ ] `gruppeid` - int4, NULL
- [ ] `alergi` - character varying(255), NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `merknad` - text, NULL
- [ ] `brukestil` - character varying(255), NULL
- [ ] `enhet` - character varying(50), NULL
- [ ] `naeringsinnhold` - text, NULL
- [ ] `twporsjon` - float8, NULL

### Column Mapping (old → new):
```
kalkylekode → 
kalkylenavn → 
ansattid → 
opprettetdato → 
revidertdato → 
informasjon → 
refporsjon → 
kategorikode → 
antallporsjoner → 
produksjonsmetode → 
gruppeid → 
alergi → 
leveringsdato → 
merknad → 
brukestil → 
enhet → 
naeringsinnhold → 
twporsjon → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpkalkyledetaljer` → (new name: _______________)

**Primary Key:** kalkylekode, produktid

**Foreign Keys:**
- `produktid` → `tblprodukter(produktid)` [fk_tbl_rpkalkyledetaljer_tblprodukter]

**Indexes:**
- `tbl_rpkalkyledetaljer_pkey` on (kalkylekode, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `kalkylekode` - int8, NOT NULL
- [ ] `produktid` - int8, NOT NULL
- [ ] `produktnavn` - text, NULL
- [ ] `leverandorsproduktnr` - text, NULL
- [ ] `pris` - float8, NULL
- [ ] `porsjonsmengde` - int8, NULL
- [ ] `enh` - text, NULL
- [ ] `totmeng` - float8, NULL
- [ ] `kostpris` - text, NULL
- [ ] `visningsenhet` - text, NULL
- [ ] `svinnprosent` - text, NULL
- [ ] `tblkalkyledetaljerid` - int8, NULL
- [ ] `energikj` - text, NULL
- [ ] `kalorier` - text, NULL
- [ ] `fett` - text, NULL
- [ ] `mettetfett` - text, NULL
- [ ] `karbohydrater` - text, NULL
- [ ] `sukkerarter` - text, NULL
- [ ] `kostfiber` - text, NULL
- [ ] `protein` - text, NULL
- [ ] `salt` - text, NULL
- [ ] `monodisakk` - text, NULL

### Column Mapping (old → new):
```
kalkylekode → 
produktid → 
produktnavn → 
leverandorsproduktnr → 
pris → 
porsjonsmengde → 
enh → 
totmeng → 
kostpris → 
visningsenhet → 
svinnprosent → 
tblkalkyledetaljerid → 
energikj → 
kalorier → 
fett → 
mettetfett → 
karbohydrater → 
sukkerarter → 
kostfiber → 
protein → 
salt → 
monodisakk → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpkalkylegruppe` → (new name: _______________)

**Primary Key:** gruppeid

**Indexes:**
- `tbl_rpkalkylegruppe_pkey` on (gruppeid) (UNIQUE)

### Columns to Remove:

- [ ] `gruppeid` - int4, NOT NULL
- [ ] `kalykegruppenavn` - character varying(50), NULL

### Column Mapping (old → new):
```
gruppeid → 
kalykegruppenavn → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpproduksjon` → (new name: _______________)

**Primary Key:** produksjonkode

**Foreign Keys:**
- `kundeid` → `tblkunder(kundeid)` [fk_tbl_rpproduksjon_tblkunder]

**Indexes:**
- `tbl_rpproduksjon_pkey` on (produksjonkode) (UNIQUE)

### Columns to Remove:

- [ ] `produksjonkode` - int4, NOT NULL
- [ ] `kundeid` - int4, NOT NULL
- [ ] `ansattid` - int4, NOT NULL
- [ ] `informasjon` - text, NULL
- [ ] `refporsjon` - character varying(255), NULL
- [ ] `antallporsjoner` - int4, NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `merknad` - character varying(255), NULL
- [ ] `created` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP

### Column Mapping (old → new):
```
produksjonkode → 
kundeid → 
ansattid → 
informasjon → 
refporsjon → 
antallporsjoner → 
leveringsdato → 
merknad → 
created → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rpproduksjondetaljer` → (new name: _______________)

**Primary Key:** produksjonskode, produktid

**Foreign Keys:**
- `produktid` → `tblprodukter(produktid)` [fk_tbl_rpproduksjondetaljer_tblprodukter]

**Indexes:**
- `tbl_rpproduksjondetaljer_pkey` on (produksjonskode, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `produksjonskode` - int8, NOT NULL
- [ ] `produktid` - int8, NOT NULL
- [ ] `produktnavn` - text, NULL
- [ ] `leverandorsproduktnr` - text, NULL
- [ ] `pris` - float8, NULL
- [ ] `porsjonsmengde` - float8, NULL
- [ ] `enh` - text, NULL
- [ ] `totmeng` - float8, NULL
- [ ] `kostpris` - float8, NULL
- [ ] `visningsenhet` - text, NULL
- [ ] `dag` - float8, NULL
- [ ] `antallporsjoner` - float8, NULL

### Column Mapping (old → new):
```
produksjonskode → 
produktid → 
produktnavn → 
leverandorsproduktnr → 
pris → 
porsjonsmengde → 
enh → 
totmeng → 
kostpris → 
visningsenhet → 
dag → 
antallporsjoner → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_rptabenheter` → (new name: _______________)

**Primary Key:** enhet

**Indexes:**
- `tbl_rptabenheter_pkey` on (enhet) (UNIQUE)

### Columns to Remove:

- [ ] `enhet` - character varying(255), NOT NULL
- [ ] `enhfaktor` - int4, NULL
- [ ] `visningsfaktor` - int4, NULL
- [ ] `visningstype` - character(1), NULL
- [ ] `kalkuler` - bool, NOT NULL, DEFAULT: false
- [ ] `naeringsinnholdsfaktor` - float8, NULL

### Column Mapping (old → new):
```
enhet → 
enhfaktor → 
visningsfaktor → 
visningstype → 
kalkuler → 
naeringsinnholdsfaktor → 
```

### Migration Notes:
_____________________________

---

## Table: `tbl_systemverdier` → (new name: _______________)

**Primary Key:** systemverdi

**Indexes:**
- `tbl_systemverdier_pkey` on (systemverdi) (UNIQUE)

### Columns to Remove:

- [ ] `systemverdi` - character varying(50), NOT NULL
- [ ] `value` - character(1), NOT NULL

### Column Mapping (old → new):
```
systemverdi → 
value → 
```

### Migration Notes:
_____________________________

---

## Table: `tblaccessmenyer` → (new name: _______________)

**Primary Key:** programnavn

**Indexes:**
- `tblaccessmenyer_pkey` on (programnavn) (UNIQUE)

### Columns to Remove:

- [ ] `programnavn` - character varying(50), NOT NULL
- [ ] `menynavn` - character varying(50), NULL
- [ ] `beskrivelse` - character varying(50), NULL
- [ ] `gruppe` - character varying(50), NULL

### Column Mapping (old → new):
```
programnavn → 
menynavn → 
beskrivelse → 
gruppe → 
```

### Migration Notes:
_____________________________

---

## Table: `tblallergener` → (new name: _______________)

**Primary Key:** allergenid

**Indexes:**
- `tblallergener_pkey` on (allergenid) (UNIQUE)

### Columns to Remove:

- [ ] `allergenid` - int4, NOT NULL
- [ ] `navn` - character varying(50), NULL

### Column Mapping (old → new):
```
allergenid → 
navn → 
```

### Migration Notes:
_____________________________

---

## Table: `tblansatte` → (new name: _______________)

**Primary Key:** ansattid

**Indexes:**
- `tblansatte_pkey` on (ansattid) (UNIQUE)

### Columns to Remove:

- [ ] `ansattid` - int8, NOT NULL
- [ ] `fornavn` - text, NULL
- [ ] `etternavn` - text, NULL
- [ ] `tittel` - text, NULL
- [ ] `adresse` - text, NULL
- [ ] `postnr` - text, NULL
- [ ] `poststed` - text, NULL
- [ ] `tlfprivat` - text, NULL
- [ ] `avdeling` - text, NULL
- [ ] `fodselsdato` - text, NULL
- [ ] `personnr` - float8, NULL
- [ ] `sluttet` - bool, NULL
- [ ] `stillings_prosent` - float8, NULL
- [ ] `resussnr` - int8, NULL
- [ ] `e_postjobb` - text, NULL
- [ ] `e_postprivat` - text, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `windowsbruker` - text, NULL
- [ ] `defaultprinter` - text, NULL

### Column Mapping (old → new):
```
ansattid → 
fornavn → 
etternavn → 
tittel → 
adresse → 
postnr → 
poststed → 
tlfprivat → 
avdeling → 
fodselsdato → 
personnr → 
sluttet → 
stillings_prosent → 
resussnr → 
e_postjobb → 
e_postprivat → 
ssma_timestamp → 
windowsbruker → 
defaultprinter → 
```

### Migration Notes:
_____________________________

---

## Table: `tblasko` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tblasko_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `varenummer` - int4, NULL
- [ ] `varenavn` - character varying(255), NULL
- [ ] `produsent` - character varying(255), NULL
- [ ] `antall_bestilt` - int4, NULL
- [ ] `pakningstype` - character varying(255), NULL
- [ ] `pakningsstorrelse` - character varying(255), NULL
- [ ] `pris` - float8, NULL
- [ ] `bestilt_kolli` - int4, NULL
- [ ] `bestilt` - int4, NULL
- [ ] `levert_kolli` - int4, NULL
- [ ] `levert` - int4, NULL
- [ ] `melding` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
id → 
varenummer → 
varenavn → 
produsent → 
antall_bestilt → 
pakningstype → 
pakningsstorrelse → 
pris → 
bestilt_kolli → 
bestilt → 
levert_kolli → 
levert → 
melding → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblbestillinger` → (new name: _______________)

**Primary Key:** bestillingsid

**Foreign Keys:**
- `leverandorid` → `tblleverandorer(leverandorid)` [tblbestillinger_tblleverandorertblbestillinger]

**Indexes:**
- `tblbestillinger_pkey` on (bestillingsid) (UNIQUE)

### Columns to Remove:

- [ ] `bestillingsid` - int4, NOT NULL
- [ ] `leverandorid` - int4, NULL, DEFAULT: 0
- [ ] `leverandor` - character varying(50), NULL
- [ ] `bestillingsdato` - timestamp, NULL
- [ ] `onsketlevering` - timestamp, NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `ansattid` - int4, NULL, DEFAULT: 0
- [ ] `bestillt` - bool, NULL, DEFAULT: false
- [ ] `lageroppdatering` - bool, NULL, DEFAULT: false
- [ ] `merknad` - text, NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
bestillingsid → 
leverandorid → 
leverandor → 
bestillingsdato → 
onsketlevering → 
leveringsdato → 
ansattid → 
bestillt → 
lageroppdatering → 
merknad → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblbestillingsposter` → (new name: _______________)

**Primary Key:** bestillingsposterid

**Foreign Keys:**
- `bestillingsid` → `tblbestillinger(bestillingsid)` [tblbestillingsposter_tblbestillingertblbestillingsposter]
- `produktid` → `tblprodukter(produktid)` [tblbestillingsposter_tblproduktertblbestillingsposter]

**Indexes:**
- `tblbestillingsposter_pkey` on (bestillingsposterid) (UNIQUE)

### Columns to Remove:

- [ ] `bestillingsposterid` - int4, NOT NULL
- [ ] `bestillingsid` - int4, NULL, DEFAULT: 0
- [ ] `produktid` - int4, NULL
- [ ] `levarandorsproduktnr` - character varying(50), NULL
- [ ] `varenavn` - character varying(250), NULL
- [ ] `pakningsstorrelse` - character varying(20), NULL
- [ ] `pris` - float8, NULL, DEFAULT: 0
- [ ] `antall_bestillt` - float8, NULL, DEFAULT: 0
- [ ] `sum` - float8, NULL
- [ ] `mottatt` - bool, NULL, DEFAULT: false
- [ ] `oppdatert` - bool, NULL, DEFAULT: false
- [ ] `bestmengde` - character varying(50), NULL
- [ ] `mva_prosent` - float8, NULL, DEFAULT: 0
- [ ] `levkode` - int4, NULL, DEFAULT: 0
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
bestillingsposterid → 
bestillingsid → 
produktid → 
levarandorsproduktnr → 
varenavn → 
pakningsstorrelse → 
pris → 
antall_bestillt → 
sum → 
mottatt → 
oppdatert → 
bestmengde → 
mva_prosent → 
levkode → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblbetalingsmate` → (new name: _______________)

### Columns to Remove:

- [ ] `beskrivelse` - character varying(50), NULL
- [ ] `betalingsmate` - int4, NULL, DEFAULT: 0

### Column Mapping (old → new):
```
beskrivelse → 
betalingsmate → 
```

### Migration Notes:
_____________________________

---

## Table: `tblgarnetyr` → (new name: _______________)

**Primary Key:** garnetyrid

**Indexes:**
- `tblgarnetyr_pkey` on (garnetyrid) (UNIQUE)

### Columns to Remove:

- [ ] `garnetyrid` - int4, NOT NULL
- [ ] `gronnsaker` - character varying(255), NULL
- [ ] `stuinger` - character varying(255), NULL
- [ ] `rakost` - character varying(255), NULL
- [ ] `sauser` - character varying(255), NULL
- [ ] `produktid` - int4, NULL

### Column Mapping (old → new):
```
garnetyrid → 
gronnsaker → 
stuinger → 
rakost → 
sauser → 
produktid → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkalkyleallergen` → (new name: _______________)

**Primary Key:** allergenid, kalkylekode

**Foreign Keys:**
- `allergenid` → `tblallergener(allergenid)` [fk_tblkalkyleallergen_tblallergener]

**Indexes:**
- `tblkalkyleallergen_pkey` on (allergenid, kalkylekode) (UNIQUE)

### Columns to Remove:

- [ ] `allergenid` - int4, NOT NULL
- [ ] `kalkylekode` - int4, NOT NULL

### Column Mapping (old → new):
```
allergenid → 
kalkylekode → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkategorier` → (new name: _______________)

**Primary Key:** kategoriid

**Indexes:**
- `tblkategorier_pkey` on (kategoriid) (UNIQUE)

### Columns to Remove:

- [ ] `kategoriid` - int4, NOT NULL
- [ ] `kategori` - character varying(50), NULL
- [ ] `beskrivelse` - text, NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
kategoriid → 
kategori → 
beskrivelse → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkjopsordredetaljer` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tblkjopsordredetaljer_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `kjopsordreid` - int4, NOT NULL
- [ ] `produktkode` - int4, NULL
- [ ] `antall` - float8, NOT NULL
- [ ] `enhetskostnad` - numeric, NOT NULL
- [ ] `mottatt_dato` - timestamp, NULL
- [ ] `registrertpalager` - bool, NOT NULL, DEFAULT: false
- [ ] `lagerid` - int4, NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
id → 
kjopsordreid → 
produktkode → 
antall → 
enhetskostnad → 
mottatt_dato → 
registrertpalager → 
lagerid → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkjopsordrer` → (new name: _______________)

**Primary Key:** kjopsordreid

**Indexes:**
- `tblkjopsordrer_pkey` on (kjopsordreid) (UNIQUE)

### Columns to Remove:

- [ ] `kjopsordreid` - int4, NOT NULL
- [ ] `leverandorid` - int4, NULL
- [ ] `opprettet_av` - int4, NULL
- [ ] `sendt_dato` - timestamp, NULL
- [ ] `opprettelsesdato` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP
- [ ] `statusid` - int4, NULL, DEFAULT: 0
- [ ] `ventet_dato` - timestamp, NULL
- [ ] `spedisjon` - numeric, NOT NULL, DEFAULT: 0
- [ ] `avgifter` - numeric, NOT NULL, DEFAULT: 0
- [ ] `betalingsdato` - timestamp, NULL
- [ ] `betalingsbelop` - numeric, NULL, DEFAULT: 0
- [ ] `betalingsmate` - character varying(50), NULL
- [ ] `merknader` - text, NULL
- [ ] `godkjent_av` - int4, NULL
- [ ] `godkjent_dato` - timestamp, NULL
- [ ] `sendt_av` - int4, NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
kjopsordreid → 
leverandorid → 
opprettet_av → 
sendt_dato → 
opprettelsesdato → 
statusid → 
ventet_dato → 
spedisjon → 
avgifter → 
betalingsdato → 
betalingsbelop → 
betalingsmate → 
merknader → 
godkjent_av → 
godkjent_dato → 
sendt_av → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkjopsordrestatus` → (new name: _______________)

**Primary Key:** statusid

**Indexes:**
- `tblkjopsordrestatus_pkey` on (statusid) (UNIQUE)

### Columns to Remove:

- [ ] `statusid` - int4, NOT NULL
- [ ] `status` - character varying(255), NULL

### Column Mapping (old → new):
```
statusid → 
status → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkontaktpersoner` → (new name: _______________)

**Primary Key:** kontaktid

**Foreign Keys:**
- `leverandorkode` → `tblleverandorer(leverandorid)` [tblkontaktpersoner_leverandorertblkontaktpersoner]

**Indexes:**
- `tblkontaktpersoner_pkey` on (kontaktid) (UNIQUE)

### Columns to Remove:

- [ ] `kontaktid` - int4, NOT NULL
- [ ] `fornavn` - character varying(255), NULL
- [ ] `etternavn` - character varying(255), NULL
- [ ] `tittel` - character varying(255), NULL
- [ ] `telefon` - character varying(30), NULL
- [ ] `e_post` - character varying(255), NULL
- [ ] `leverandorkode` - int4, NULL
- [ ] `kundekode` - int4, NULL

### Column Mapping (old → new):
```
kontaktid → 
fornavn → 
etternavn → 
tittel → 
telefon → 
e_post → 
leverandorkode → 
kundekode → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkontonummer` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tblkontonummer_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `salg_sykehjem` - character varying(50), NULL
- [ ] `salg_kantiner_catering` - character varying(50), NULL
- [ ] `salg_hjemmeboende` - character varying(50), NULL

### Column Mapping (old → new):
```
id → 
salg_sykehjem → 
salg_kantiner_catering → 
salg_hjemmeboende → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkunde_kundeinfoprodukt` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tblkunde_kundeinfoprodukt_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `kundeid` - int4, NULL
- [ ] `kundeinfoproduktid` - int4, NULL

### Column Mapping (old → new):
```
id → 
kundeid → 
kundeinfoproduktid → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkundeinfoprodukt` → (new name: _______________)

**Primary Key:** ekstrakundeinfoid

**Indexes:**
- `tblkundeinfoprodukt_pkey` on (ekstrakundeinfoid) (UNIQUE)

### Columns to Remove:

- [ ] `ekstrakundeinfoid` - int4, NOT NULL
- [ ] `beskrivelse` - character varying(255), NULL

### Column Mapping (old → new):
```
ekstrakundeinfoid → 
beskrivelse → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkunder` → (new name: _______________)

**Primary Key:** kundeid

**Foreign Keys:**
- `ansattid` → `tblansatte(ansattid)` [tblkunder_tblansattetblkunder]
- `kundegruppe` → `tblkundgruppe(gruppeid)` [tblkunder_tblkundgruppetblkunder]
- `leveringsdag` → `tblleveringsdag(levid)` [tblkunder_tblleveringsdagtblkunder]
- `velgsone` → `tblsone(idsone)` [tblkunder_tblsonetblkunder]
- `rute` → `tblruteplan(rutenr)` [tblkunder_tblruteplantblkunder]
- `sykehjemid` → `tblkunder(kundeid)` [fk_tblkunder_tblkunder]

**Indexes:**
- `tblkunder_pkey` on (kundeid) (UNIQUE)

### Columns to Remove:

- [ ] `kundeid` - int8, NOT NULL
- [ ] `kundenavn` - text, NULL
- [ ] `avdeling` - text, NULL
- [ ] `kontaktid` - text, NULL
- [ ] `telefonnummer` - text, NULL
- [ ] `bestillernr` - text, NULL
- [ ] `lopenr` - float8, NULL
- [ ] `merknad` - text, NULL
- [ ] `adresse` - text, NULL
- [ ] `postboks` - float8, NULL
- [ ] `postnr` - text, NULL
- [ ] `sted` - text, NULL
- [ ] `velgsone` - int4, NULL
- [ ] `leveringsdag` - int4, NULL
- [ ] `kundeinaktiv` - bool, NULL
- [ ] `kundenragresso` - float8, NULL
- [ ] `e_post` - text, NULL
- [ ] `webside` - text, NULL
- [ ] `kundegruppe` - int4, NULL
- [ ] `bestillerselv` - bool, NULL
- [ ] `rute` - int8, NULL
- [ ] `menyinfo` - text, NULL
- [ ] `ansattid` - int8, NULL
- [ ] `sjaforparute` - float8, NULL
- [ ] `diett` - bool, NULL
- [ ] `menygruppeid` - float8, NULL
- [ ] `utdato` - timestamp, NULL
- [ ] `inndato` - timestamp, NULL
- [ ] `avsluttet` - bool, NULL
- [ ] `eksportkatalog` - text, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `mobilnummer` - text, NULL
- [ ] `formkost` - bool, NULL
- [ ] `sykehjemid` - int8, NULL
- [ ] `e_post2` - text, NULL

### Column Mapping (old → new):
```
kundeid → 
kundenavn → 
avdeling → 
kontaktid → 
telefonnummer → 
bestillernr → 
lopenr → 
merknad → 
adresse → 
postboks → 
postnr → 
sted → 
velgsone → 
leveringsdag → 
kundeinaktiv → 
kundenragresso → 
e_post → 
webside → 
kundegruppe → 
bestillerselv → 
rute → 
menyinfo → 
ansattid → 
sjaforparute → 
diett → 
menygruppeid → 
utdato → 
inndato → 
avsluttet → 
eksportkatalog → 
ssma_timestamp → 
mobilnummer → 
formkost → 
sykehjemid → 
e_post2 → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkundersomikkeharbestilt` → (new name: _______________)

### Columns to Remove:

- [ ] `kundeid` - int8, NULL
- [ ] `kundenavn` - text, NULL
- [ ] `avdeling` - text, NULL
- [ ] `kontaktid` - text, NULL
- [ ] `telefonnummer` - text, NULL
- [ ] `bestillernr` - text, NULL
- [ ] `lopenr` - float8, NULL
- [ ] `merknad` - text, NULL
- [ ] `adresse` - text, NULL
- [ ] `postboks` - float8, NULL
- [ ] `postnr` - text, NULL
- [ ] `sted` - text, NULL
- [ ] `velgsone` - int8, NULL
- [ ] `leveringsdag` - int8, NULL
- [ ] `kundeinaktiv` - bool, NULL
- [ ] `kundenragresso` - float8, NULL
- [ ] `e_post` - text, NULL
- [ ] `webside` - text, NULL
- [ ] `kundegruppe` - int8, NULL
- [ ] `bestillerselv` - bool, NULL
- [ ] `rute` - int8, NULL
- [ ] `menyinfo` - text, NULL
- [ ] `ansattid` - float8, NULL
- [ ] `sjaforparute` - int8, NULL
- [ ] `diett` - bool, NULL
- [ ] `menygruppeid` - int8, NULL
- [ ] `utdato` - text, NULL
- [ ] `inndato` - timestamp, NULL
- [ ] `avsluttet` - bool, NULL
- [ ] `eksportkatalog` - text, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `ordreid` - text, NULL
- [ ] `expr1` - text, NULL
- [ ] `expr2` - text, NULL
- [ ] `expr3` - text, NULL
- [ ] `ordredato` - text, NULL
- [ ] `leveringsdato` - text, NULL
- [ ] `fakturadato` - text, NULL
- [ ] `sendestil` - text, NULL
- [ ] `betalingsmate` - text, NULL
- [ ] `lagerok` - text, NULL
- [ ] `informasjon` - text, NULL
- [ ] `ordrestatusid` - text, NULL
- [ ] `fakturaid` - text, NULL
- [ ] `kansellertdato` - text, NULL
- [ ] `sentbekreftelse` - text, NULL

### Column Mapping (old → new):
```
kundeid → 
kundenavn → 
avdeling → 
kontaktid → 
telefonnummer → 
bestillernr → 
lopenr → 
merknad → 
adresse → 
postboks → 
postnr → 
sted → 
velgsone → 
leveringsdag → 
kundeinaktiv → 
kundenragresso → 
e_post → 
webside → 
kundegruppe → 
bestillerselv → 
rute → 
menyinfo → 
ansattid → 
sjaforparute → 
diett → 
menygruppeid → 
utdato → 
inndato → 
avsluttet → 
eksportkatalog → 
ssma_timestamp → 
ordreid → 
expr1 → 
expr2 → 
expr3 → 
ordredato → 
leveringsdato → 
fakturadato → 
sendestil → 
betalingsmate → 
lagerok → 
informasjon → 
ordrestatusid → 
fakturaid → 
kansellertdato → 
sentbekreftelse → 
```

### Migration Notes:
_____________________________

---

## Table: `tblkundgruppe` → (new name: _______________)

**Primary Key:** gruppeid

**Indexes:**
- `tblkundgruppe_pkey` on (gruppeid) (UNIQUE)

### Columns to Remove:

- [ ] `gruppeid` - int4, NOT NULL
- [ ] `gruppe` - character varying(255), NOT NULL
- [ ] `webshop` - bool, NOT NULL
- [ ] `autofaktura` - bool, NOT NULL

### Column Mapping (old → new):
```
gruppeid → 
gruppe → 
webshop → 
autofaktura → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllagerlokasjon` → (new name: _______________)

**Primary Key:** lagerid

**Indexes:**
- `tbllagerlokasjon_pkey` on (lagerid) (UNIQUE)

### Columns to Remove:

- [ ] `lagerid` - int4, NOT NULL
- [ ] `beskrivelse` - character varying(50), NULL

### Column Mapping (old → new):
```
lagerid → 
beskrivelse → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllagertransaksjoner` → (new name: _______________)

**Primary Key:** transaksjonsid

**Foreign Keys:**
- `lagertransaksjontypeid` → `tbllagertransaksjonstyper(lagertransaksjontypeid)` [tbllagertransaksjoner_tbllagertransaksjonstypertbllagertransaks]
- `produktid` → `tblprodukter(produktid)` [tbllagertransaksjoner_tblproduktertbllagertransaksjoner]

**Indexes:**
- `tbllagertransaksjoner_pkey` on (transaksjonsid) (UNIQUE)

### Columns to Remove:

- [ ] `transaksjonsid` - int4, NOT NULL
- [ ] `lagertransaksjontypeid` - int4, NULL
- [ ] `transaksjonopprettet` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP
- [ ] `transaksjonendret` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP
- [ ] `produktid` - int4, NULL
- [ ] `antall` - int4, NULL
- [ ] `kjopsordreid` - int4, NULL
- [ ] `kundeordreid` - int4, NULL

### Column Mapping (old → new):
```
transaksjonsid → 
lagertransaksjontypeid → 
transaksjonopprettet → 
transaksjonendret → 
produktid → 
antall → 
kjopsordreid → 
kundeordreid → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllagertransaksjonstyper` → (new name: _______________)

**Primary Key:** lagertransaksjontypeid

**Indexes:**
- `tbllagertransaksjonstyper_pkey` on (lagertransaksjontypeid) (UNIQUE)

### Columns to Remove:

- [ ] `lagertransaksjontypeid` - int4, NOT NULL
- [ ] `typenavn` - character varying(50), NOT NULL

### Column Mapping (old → new):
```
lagertransaksjontypeid → 
typenavn → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllevbestillinger` → (new name: _______________)

**Primary Key:** bestillingid

**Foreign Keys:**
- `bestillingsnr` → `tbllevbestillingshode(bestillingsnr)` [fk_tbllevbestillinger_tbllevbestillingshode]

**Indexes:**
- `tbllevbestillinger_pkey` on (bestillingid) (UNIQUE)

### Columns to Remove:

- [ ] `bestillingid` - int4, NOT NULL
- [ ] `leverandorid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `leverandorsproduktnr` - character varying(50), NULL
- [ ] `produktnavn` - character varying(255), NULL
- [ ] `summeravantall` - float8, NULL
- [ ] `pakningstype` - character varying(255), NULL
- [ ] `bestillingsnr` - int4, NOT NULL
- [ ] `leveringsdato` - date, NOT NULL

### Column Mapping (old → new):
```
bestillingid → 
leverandorid → 
produktid → 
leverandorsproduktnr → 
produktnavn → 
summeravantall → 
pakningstype → 
bestillingsnr → 
leveringsdato → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllevbestillingshode` → (new name: _______________)

**Primary Key:** bestillingsnr

**Foreign Keys:**
- `leverandor` → `tblleverandorer(leverandorid)` [fk_tbllevbestillingshode_tblleverandorer]

**Indexes:**
- `tbllevbestillingshode_pkey` on (bestillingsnr) (UNIQUE)

### Columns to Remove:

- [ ] `bestillingsnr` - int4, NOT NULL
- [ ] `leveringsdato` - date, NOT NULL
- [ ] `bestillingsdato` - date, NOT NULL
- [ ] `vaarreferanse` - character varying(150), NULL
- [ ] `deresreferanse` - character varying(150), NULL
- [ ] `leverandor` - int4, NOT NULL
- [ ] `datosendt` - date, NULL

### Column Mapping (old → new):
```
bestillingsnr → 
leveringsdato → 
bestillingsdato → 
vaarreferanse → 
deresreferanse → 
leverandor → 
datosendt → 
```

### Migration Notes:
_____________________________

---

## Table: `tblleverandorer` → (new name: _______________)

**Primary Key:** leverandorid

**Indexes:**
- `tblleverandorer_pkey` on (leverandorid) (UNIQUE)

### Columns to Remove:

- [ ] `leverandorid` - int4, NOT NULL
- [ ] `refkundenummer` - float8, NULL, DEFAULT: 0
- [ ] `leverandornavn` - character varying(50), NULL
- [ ] `adresse` - character varying(255), NULL
- [ ] `e_post` - text, NULL
- [ ] `postnummer` - int4, NULL
- [ ] `poststed` - character varying(50), NULL
- [ ] `telefonnummer` - character varying(30), NULL
- [ ] `bestillingsnr` - float8, NULL, DEFAULT: 0
- [ ] `utgatt` - bool, NULL, DEFAULT: false
- [ ] `webside` - text, NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
leverandorid → 
refkundenummer → 
leverandornavn → 
adresse → 
e_post → 
postnummer → 
poststed → 
telefonnummer → 
bestillingsnr → 
utgatt → 
webside → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblleveringsdag` → (new name: _______________)

**Primary Key:** levid

**Indexes:**
- `tblleveringsdag_pkey` on (levid) (UNIQUE)

### Columns to Remove:

- [ ] `levid` - int4, NOT NULL
- [ ] `leveringsdag` - character varying(255), NULL

### Column Mapping (old → new):
```
levid → 
leveringsdag → 
```

### Migration Notes:
_____________________________

---

## Table: `tbllog` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tbllog_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `logtype` - character varying(50), NOT NULL
- [ ] `melding` - text, NULL
- [ ] `ansatt` - int4, NULL
- [ ] `dato` - timestamp, NOT NULL, DEFAULT: CURRENT_TIMESTAMP

### Column Mapping (old → new):
```
id → 
logtype → 
melding → 
ansatt → 
dato → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmeny` → (new name: _______________)

**Primary Key:** menyid

**Indexes:**
- `tblmeny_pkey` on (menyid) (UNIQUE)

### Columns to Remove:

- [ ] `menyid` - int4, NOT NULL
- [ ] `beskrivelse` - character varying(255), NULL
- [ ] `menygruppe` - int4, NULL

### Column Mapping (old → new):
```
menyid → 
beskrivelse → 
menygruppe → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmenygruppe` → (new name: _______________)

**Primary Key:** menygruppeid

**Indexes:**
- `tblmenygruppe_pkey` on (menygruppeid) (UNIQUE)

### Columns to Remove:

- [ ] `menygruppeid` - int4, NOT NULL
- [ ] `beskrivelse` - character varying(255), NULL
- [ ] `kode` - character varying(255), NULL

### Column Mapping (old → new):
```
menygruppeid → 
beskrivelse → 
kode → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmenyprodukt` → (new name: _______________)

**Primary Key:** menyid, produktid

**Indexes:**
- `tblmenyprodukt_pkey` on (menyid, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `menyid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL

### Column Mapping (old → new):
```
menyid → 
produktid → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmenysykehjem` → (new name: _______________)

### Columns to Remove:

- [ ] `menyid` - int4, NOT NULL
- [ ] `produktid` - int4, NULL
- [ ] `fradato` - timestamp, NOT NULL
- [ ] `tildato` - timestamp, NOT NULL

### Column Mapping (old → new):
```
menyid → 
produktid → 
fradato → 
tildato → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmva` → (new name: _______________)

**Primary Key:** avgiftsid

**Indexes:**
- `tblmva_pkey` on (avgiftsid) (UNIQUE)

### Columns to Remove:

- [ ] `avgiftsid` - int4, NOT NULL
- [ ] `mva` - float4, NULL
- [ ] `mvatype` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
avgiftsid → 
mva → 
mvatype → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tblmva_kundekategori` → (new name: _______________)

**Primary Key:** mva_kundekategoriid

**Foreign Keys:**
- `gruppeid` → `tblkundgruppe(gruppeid)` [fk_tblmva_kundekatagori_tblkundgruppe]
- `avgiftsid` → `tblmva(avgiftsid)` [fk_tblmva_kundekatagori_tblmva]

**Indexes:**
- `tblmva_kundekategori_pkey` on (mva_kundekategoriid) (UNIQUE)

### Columns to Remove:

- [ ] `mva_kundekategoriid` - int4, NOT NULL
- [ ] `gruppeid` - int4, NOT NULL
- [ ] `avgiftsid` - int4, NOT NULL
- [ ] `kontoregenskap` - character varying(50), NOT NULL

### Column Mapping (old → new):
```
mva_kundekategoriid → 
gruppeid → 
avgiftsid → 
kontoregenskap → 
```

### Migration Notes:
_____________________________

---

## Table: `tblneringstabellen` → (new name: _______________)

**Primary Key:** neringstabellid

**Indexes:**
- `tblneringstabellen_pkey` on (neringstabellid) (UNIQUE)

### Columns to Remove:

- [ ] `neringstabellid` - int4, NOT NULL
- [ ] `matvareid` - character varying(150), NULL
- [ ] `matvare` - character varying(150), NULL
- [ ] `spiselig_del` - character varying(50), NULL
- [ ] `ref1` - character varying(50), NULL
- [ ] `vann` - character varying(50), NULL
- [ ] `ref2` - character varying(50), NULL
- [ ] `kilojoule` - character varying(50), NULL
- [ ] `ref3` - character varying(50), NULL
- [ ] `kilokalorier` - character varying(50), NULL
- [ ] `ref4` - character varying(50), NULL
- [ ] `fett` - character varying(50), NULL
- [ ] `ref5` - character varying(50), NULL
- [ ] `mettet` - character varying(50), NULL
- [ ] `ref6` - character varying(50), NULL
- [ ] `c12_0` - character varying(50), NULL
- [ ] `ref7` - character varying(50), NULL
- [ ] `c14_0` - character varying(50), NULL
- [ ] `ref8` - character varying(50), NULL
- [ ] `c16_0` - character varying(50), NULL
- [ ] `ref9` - character varying(50), NULL
- [ ] `c18_0` - character varying(50), NULL
- [ ] `ref10` - character varying(50), NULL
- [ ] `trans` - character varying(50), NULL
- [ ] `ref11` - character varying(50), NULL
- [ ] `enumettet` - character varying(50), NULL
- [ ] `ref12` - character varying(50), NULL
- [ ] `c16_1_sum` - character varying(50), NULL
- [ ] `ref13` - character varying(50), NULL
- [ ] `c18_1_sum` - character varying(50), NULL
- [ ] `ref14` - character varying(50), NULL
- [ ] `flerumettet` - character varying(50), NULL
- [ ] `ref15` - character varying(50), NULL
- [ ] `c18_2n_6` - character varying(50), NULL
- [ ] `ref16` - character varying(50), NULL
- [ ] `c18_3n_3` - character varying(50), NULL
- [ ] `ref17` - character varying(50), NULL
- [ ] `c20_3n_3` - character varying(50), NULL
- [ ] `ref18` - character varying(50), NULL
- [ ] `c20_3n_6` - character varying(50), NULL
- [ ] `ref19` - character varying(50), NULL
- [ ] `c20_4n_3` - character varying(50), NULL
- [ ] `ref20` - character varying(50), NULL
- [ ] `c20_4n_6` - character varying(50), NULL
- [ ] `ref21` - character varying(50), NULL
- [ ] `c20_5n_3_epa` - character varying(50), NULL
- [ ] `ref22` - character varying(50), NULL
- [ ] `c22_5n_3_dpa` - character varying(50), NULL
- [ ] `ref23` - character varying(50), NULL
- [ ] `c22_6n_3_dha` - character varying(50), NULL
- [ ] `ref24` - character varying(50), NULL
- [ ] `omega_3` - character varying(50), NULL
- [ ] `ref25` - character varying(50), NULL
- [ ] `omega_6` - character varying(50), NULL
- [ ] `ref26` - character varying(50), NULL
- [ ] `kolesterol` - character varying(50), NULL
- [ ] `ref27` - character varying(50), NULL
- [ ] `karbohydrat` - character varying(50), NULL
- [ ] `ref28` - character varying(50), NULL
- [ ] `stivelse` - character varying(50), NULL
- [ ] `ref29` - character varying(50), NULL
- [ ] `mono_disakk` - character varying(50), NULL
- [ ] `ref30` - character varying(50), NULL
- [ ] `sukker_tilsatt` - character varying(50), NULL
- [ ] `ref31` - character varying(50), NULL
- [ ] `kostfiber` - character varying(50), NULL
- [ ] `ref32` - character varying(50), NULL
- [ ] `protein` - character varying(50), NULL
- [ ] `ref33` - character varying(50), NULL
- [ ] `salt` - character varying(50), NULL
- [ ] `ref34` - character varying(50), NULL
- [ ] `alkohol` - character varying(50), NULL
- [ ] `ref35` - character varying(50), NULL
- [ ] `vitamin_a` - character varying(50), NULL
- [ ] `ref36` - character varying(50), NULL
- [ ] `retinol` - character varying(50), NULL
- [ ] `ref37` - character varying(50), NULL
- [ ] `beta_karoten` - character varying(50), NULL
- [ ] `ref38` - character varying(50), NULL
- [ ] `vitamin_d` - character varying(50), NULL
- [ ] `ref39` - character varying(50), NULL
- [ ] `vitamin_e` - character varying(50), NULL
- [ ] `ref40` - character varying(50), NULL
- [ ] `tiamin` - character varying(50), NULL
- [ ] `ref41` - character varying(50), NULL
- [ ] `riboflavin` - character varying(50), NULL
- [ ] `ref42` - character varying(50), NULL
- [ ] `niacin` - character varying(50), NULL
- [ ] `ref43` - character varying(50), NULL
- [ ] `vitamin_b6` - character varying(50), NULL
- [ ] `ref44` - character varying(50), NULL
- [ ] `folat` - character varying(50), NULL
- [ ] `ref45` - character varying(50), NULL
- [ ] `vitamin_b12` - character varying(50), NULL
- [ ] `ref46` - character varying(50), NULL
- [ ] `vitamin_c` - character varying(50), NULL
- [ ] `ref47` - character varying(50), NULL
- [ ] `kalsium` - character varying(50), NULL
- [ ] `ref48` - character varying(50), NULL
- [ ] `jern` - character varying(50), NULL
- [ ] `ref49` - character varying(50), NULL
- [ ] `natrium` - character varying(50), NULL
- [ ] `ref50` - character varying(50), NULL
- [ ] `kalium` - character varying(50), NULL
- [ ] `ref51` - character varying(50), NULL
- [ ] `magnesium` - character varying(50), NULL
- [ ] `ref52` - character varying(50), NULL
- [ ] `sink` - character varying(50), NULL
- [ ] `ref53` - character varying(50), NULL
- [ ] `selen` - character varying(50), NULL
- [ ] `ref54` - character varying(50), NULL
- [ ] `kopper` - character varying(50), NULL
- [ ] `ref55` - character varying(50), NULL
- [ ] `fosfor` - character varying(50), NULL
- [ ] `ref56` - character varying(50), NULL
- [ ] `jod` - character varying(50), NULL
- [ ] `ref57` - character varying(50), NULL
- [ ] `column_116` - character varying(50), NULL
- [ ] `column_117` - character varying(50), NULL
- [ ] `column_118` - character varying(50), NULL

### Column Mapping (old → new):
```
neringstabellid → 
matvareid → 
matvare → 
spiselig_del → 
ref1 → 
vann → 
ref2 → 
kilojoule → 
ref3 → 
kilokalorier → 
ref4 → 
fett → 
ref5 → 
mettet → 
ref6 → 
c12_0 → 
ref7 → 
c14_0 → 
ref8 → 
c16_0 → 
ref9 → 
c18_0 → 
ref10 → 
trans → 
ref11 → 
enumettet → 
ref12 → 
c16_1_sum → 
ref13 → 
c18_1_sum → 
ref14 → 
flerumettet → 
ref15 → 
c18_2n_6 → 
ref16 → 
c18_3n_3 → 
ref17 → 
c20_3n_3 → 
ref18 → 
c20_3n_6 → 
ref19 → 
c20_4n_3 → 
ref20 → 
c20_4n_6 → 
ref21 → 
c20_5n_3_epa → 
ref22 → 
c22_5n_3_dpa → 
ref23 → 
c22_6n_3_dha → 
ref24 → 
omega_3 → 
ref25 → 
omega_6 → 
ref26 → 
kolesterol → 
ref27 → 
karbohydrat → 
ref28 → 
stivelse → 
ref29 → 
mono_disakk → 
ref30 → 
sukker_tilsatt → 
ref31 → 
kostfiber → 
ref32 → 
protein → 
ref33 → 
salt → 
ref34 → 
alkohol → 
ref35 → 
vitamin_a → 
ref36 → 
retinol → 
ref37 → 
beta_karoten → 
ref38 → 
vitamin_d → 
ref39 → 
vitamin_e → 
ref40 → 
tiamin → 
ref41 → 
riboflavin → 
ref42 → 
niacin → 
ref43 → 
vitamin_b6 → 
ref44 → 
folat → 
ref45 → 
vitamin_b12 → 
ref46 → 
vitamin_c → 
ref47 → 
kalsium → 
ref48 → 
jern → 
ref49 → 
natrium → 
ref50 → 
kalium → 
ref51 → 
magnesium → 
ref52 → 
sink → 
ref53 → 
selen → 
ref54 → 
kopper → 
ref55 → 
fosfor → 
ref56 → 
jod → 
ref57 → 
column_116 → 
column_117 → 
column_118 → 
```

### Migration Notes:
_____________________________

---

## Table: `tblordredetaljer` → (new name: _______________)

**Primary Key:** ordreid, produktid, unik

**Foreign Keys:**
- `ordreid` → `tblordrer(ordreid)` [tblordredetaljer_tblordrertblordredetaljer]
- `produktid` → `tblprodukter(produktid)` [tblordredetaljer_tblproduktertblordredetaljer]

**Indexes:**
- `tblordredetaljer_pkey` on (ordreid, produktid, unik) (UNIQUE)

### Columns to Remove:

- [ ] `ordreid` - int8, NOT NULL
- [ ] `produktid` - int8, NOT NULL
- [ ] `levdato` - timestamp, NULL
- [ ] `pris` - float8, NULL
- [ ] `antall` - float8, NULL
- [ ] `rabatt` - float8, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `ident` - text, NULL
- [ ] `unik` - int8, NOT NULL

### Column Mapping (old → new):
```
ordreid → 
produktid → 
levdato → 
pris → 
antall → 
rabatt → 
ssma_timestamp → 
ident → 
unik → 
```

### Migration Notes:
_____________________________

---

## Table: `tblordrer` → (new name: _______________)

**Primary Key:** ordreid

**Foreign Keys:**
- `ordrestatusid` → `tblordrestatus(statusid)` [tblordrer_tblordrestatustblordrer]
- `ansattid` → `tblansatte(ansattid)` [tblordrer_tblansattetblordrer]
- `kundeid` → `tblkunder(kundeid)` [tblordrer_tblkundertblordrer]

**Indexes:**
- `tblordrer_pkey` on (ordreid) (UNIQUE)

### Columns to Remove:

- [ ] `ordreid` - int8, NOT NULL
- [ ] `kundeid` - int8, NULL
- [ ] `ansattid` - int8, NULL
- [ ] `kundenavn` - text, NULL
- [ ] `ordredato` - timestamp, NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `fakturadato` - timestamp, NULL
- [ ] `sendestil` - text, NULL
- [ ] `betalingsmate` - int8, NULL
- [ ] `lagerok` - bool, NULL
- [ ] `informasjon` - text, NULL
- [ ] `ordrestatusid` - int8, NULL
- [ ] `fakturaid` - float8, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `kansellertdato` - timestamp, NULL
- [ ] `sentbekreftelse` - bool, NULL
- [ ] `sentregnskap` - timestamp, NULL
- [ ] `ordrelevert` - text, NULL
- [ ] `levertagresso` - text, NULL

### Column Mapping (old → new):
```
ordreid → 
kundeid → 
ansattid → 
kundenavn → 
ordredato → 
leveringsdato → 
fakturadato → 
sendestil → 
betalingsmate → 
lagerok → 
informasjon → 
ordrestatusid → 
fakturaid → 
ssma_timestamp → 
kansellertdato → 
sentbekreftelse → 
sentregnskap → 
ordrelevert → 
levertagresso → 
```

### Migration Notes:
_____________________________

---

## Table: `tblordrestatus` → (new name: _______________)

**Primary Key:** statusid

**Indexes:**
- `tblordrestatus_pkey` on (statusid) (UNIQUE)

### Columns to Remove:

- [ ] `statusid` - int4, NOT NULL
- [ ] `status` - character varying(255), NULL

### Column Mapping (old → new):
```
statusid → 
status → 
```

### Migration Notes:
_____________________________

---

## Table: `tblperiode` → (new name: _______________)

**Primary Key:** menyperiodeid

**Indexes:**
- `tblperiode_pkey` on (menyperiodeid) (UNIQUE)

### Columns to Remove:

- [ ] `menyperiodeid` - int4, NOT NULL
- [ ] `ukenr` - int4, NULL
- [ ] `fradato` - timestamp, NULL
- [ ] `tildato` - timestamp, NULL

### Column Mapping (old → new):
```
menyperiodeid → 
ukenr → 
fradato → 
tildato → 
```

### Migration Notes:
_____________________________

---

## Table: `tblperiodemeny` → (new name: _______________)

**Primary Key:** periodeid, menyid

**Foreign Keys:**
- `menyid` → `tblmeny(menyid)` [fk_tblperiodemeny_tblmeny]
- `periodeid` → `tblperiode(menyperiodeid)` [fk_tblperiodemeny_tblperiode]

**Indexes:**
- `tblperiodemeny_pkey` on (periodeid, menyid) (UNIQUE)

### Columns to Remove:

- [ ] `periodeid` - int4, NOT NULL
- [ ] `menyid` - int4, NOT NULL

### Column Mapping (old → new):
```
periodeid → 
menyid → 
```

### Migration Notes:
_____________________________

---

## Table: `tblprodukt_allergen` → (new name: _______________)

**Primary Key:** produktid, allergenid

**Foreign Keys:**
- `allergenid` → `tblallergener(allergenid)` [fk_tblprodukt_allergen_tblallergener]
- `produktid` → `tblprodukter(produktid)` [fk_tblprodukt_allergen_tblprodukter]

**Indexes:**
- `tblprodukt_allergen_pkey` on (produktid, allergenid) (UNIQUE)

### Columns to Remove:

- [ ] `produktid` - int4, NOT NULL
- [ ] `allergenid` - int4, NOT NULL

### Column Mapping (old → new):
```
produktid → 
allergenid → 
```

### Migration Notes:
_____________________________

---

## Table: `tblprodukter` → (new name: _______________)

**Primary Key:** produktid

**Foreign Keys:**
- `levrandorid` → `tblleverandorer(leverandorid)` [tblprodukter_ac242a1e_d084_4f03_83d6_7d50b5290410]
- `kategoriid` → `tblkategorier(kategoriid)` [tblprodukter_tblkategoriertblprodukter]

**Indexes:**
- `tblprodukter_pkey` on (produktid) (UNIQUE)

### Columns to Remove:

- [ ] `produktid` - int8, NOT NULL
- [ ] `produktnavn` - text, NULL
- [ ] `leverandorsproduktnr` - text, NULL
- [ ] `antalleht` - float8, NULL
- [ ] `pakningstype` - text, NULL
- [ ] `pakningsstorrelse` - text, NULL
- [ ] `pris` - float8, NULL
- [ ] `paknpris` - text, NULL
- [ ] `levrandorid` - int8, NULL
- [ ] `kategoriid` - int8, NULL
- [ ] `lagermengde` - float8, NULL
- [ ] `bestillingsgrense` - float8, NULL
- [ ] `bestillingsmengde` - float8, NULL
- [ ] `ean_kode` - text, NULL
- [ ] `utgatt` - bool, NULL
- [ ] `oppdatert` - bool, NULL
- [ ] `webshop` - bool, NULL
- [ ] `mvaverdi` - float8, NULL
- [ ] `ssma_timestamp` - text, NULL
- [ ] `lagerid` - float8, NULL
- [ ] `utregningsfaktor` - float8, NULL
- [ ] `utregnetpris` - float8, NULL
- [ ] `visningsnavn` - text, NULL
- [ ] `visningsnavn2` - text, NULL
- [ ] `allergenprodukt` - bool, NULL
- [ ] `energikj` - float8, NULL
- [ ] `kalorier` - float8, NULL
- [ ] `fett` - float8, NULL
- [ ] `mettetfett` - float8, NULL
- [ ] `karbohydrater` - float8, NULL
- [ ] `sukkerarter` - float8, NULL
- [ ] `kostfiber` - float8, NULL
- [ ] `protein` - float8, NULL
- [ ] `salt` - float8, NULL
- [ ] `monodisakk` - float8, NULL
- [ ] `matvareid` - text, NULL
- [ ] `webshopsted` - text, NULL

### Column Mapping (old → new):
```
produktid → 
produktnavn → 
leverandorsproduktnr → 
antalleht → 
pakningstype → 
pakningsstorrelse → 
pris → 
paknpris → 
levrandorid → 
kategoriid → 
lagermengde → 
bestillingsgrense → 
bestillingsmengde → 
ean_kode → 
utgatt → 
oppdatert → 
webshop → 
mvaverdi → 
ssma_timestamp → 
lagerid → 
utregningsfaktor → 
utregnetpris → 
visningsnavn → 
visningsnavn2 → 
allergenprodukt → 
energikj → 
kalorier → 
fett → 
mettetfett → 
karbohydrater → 
sukkerarter → 
kostfiber → 
protein → 
salt → 
monodisakk → 
matvareid → 
webshopsted → 
```

### Migration Notes:
_____________________________

---

## Table: `tblruteplan` → (new name: _______________)

**Primary Key:** rutenr

**Indexes:**
- `tblruteplan_pkey` on (rutenr) (UNIQUE)

### Columns to Remove:

- [ ] `rutenr` - int8, NOT NULL
- [ ] `rutenavn` - text, NULL
- [ ] `stoppnr` - text, NULL
- [ ] `dinref` - text, NULL

### Column Mapping (old → new):
```
rutenr → 
rutenavn → 
stoppnr → 
dinref → 
```

### Migration Notes:
_____________________________

---

## Table: `tblsone` → (new name: _______________)

**Primary Key:** idsone

**Indexes:**
- `tblsone_pkey` on (idsone) (UNIQUE)

### Columns to Remove:

- [ ] `idsone` - int4, NOT NULL
- [ ] `sone` - character varying(50), NULL

### Column Mapping (old → new):
```
idsone → 
sone → 
```

### Migration Notes:
_____________________________

---

## Table: `tbltmpkundergruppeordre` → (new name: _______________)

**Primary Key:** kundeid

**Indexes:**
- `tbltmpkundergruppeordre_pkey` on (kundeid) (UNIQUE)

### Columns to Remove:

- [ ] `kundeid` - int4, NOT NULL
- [ ] `kundenavn` - character varying(255), NULL

### Column Mapping (old → new):
```
kundeid → 
kundenavn → 
```

### Migration Notes:
_____________________________

---

## Table: `tbltmpordre` → (new name: _______________)

**Primary Key:** kundeid, produktid

**Indexes:**
- `tbltmpordre_pkey` on (kundeid, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `kundeid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `antall` - int4, NULL
- [ ] `overforttilordre` - bool, NULL, DEFAULT: false
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
kundeid → 
produktid → 
antall → 
overforttilordre → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `tbltmpordrebestilling` → (new name: _______________)

**Primary Key:** kundeid, produktid

**Indexes:**
- `tbltmpordrebestilling_pkey` on (kundeid, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `produktnavn` - character varying(255), NULL
- [ ] `pakningstype` - character varying(255), NULL
- [ ] `antalleht` - int4, NULL
- [ ] `pris` - numeric, NULL
- [ ] `kundeid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `sistebestilling` - int4, NULL
- [ ] `antall` - int4, NULL
- [ ] `overforttilordre` - bool, NULL, DEFAULT: false
- [ ] `bildelink` - text, NULL
- [ ] `ssma_timestamp` - text, NOT NULL
- [ ] `ident` - character varying(255), NULL

### Column Mapping (old → new):
```
produktnavn → 
pakningstype → 
antalleht → 
pris → 
kundeid → 
produktid → 
sistebestilling → 
antall → 
overforttilordre → 
bildelink → 
ssma_timestamp → 
ident → 
```

### Migration Notes:
_____________________________

---

## Table: `tbltmpordrebestillingsykehjem` → (new name: _______________)

**Primary Key:** id

**Foreign Keys:**
- `kundeid` → `tblkunder(kundeid)` [fk_tbltmpordrebestillingkunder_tblkunder]

**Indexes:**
- `tbltmpordrebestillingsykehjem_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `kundeid` - int4, NOT NULL
- [ ] `produktid` - character varying(255), NULL
- [ ] `pris` - numeric, NULL
- [ ] `antall` - numeric, NOT NULL
- [ ] `leveringsdato` - timestamp, NOT NULL
- [ ] `ident` - character varying(255), NULL

### Column Mapping (old → new):
```
id → 
kundeid → 
produktid → 
pris → 
antall → 
leveringsdato → 
ident → 
```

### Migration Notes:
_____________________________

---

## Table: `tblvarebestillingbekreftelseasko` → (new name: _______________)

**Primary Key:** varenummer

**Indexes:**
- `tblvarebestillingbekreftelseasko_pkey` on (varenummer) (UNIQUE)

### Columns to Remove:

- [ ] `varenummer` - character varying(50), NOT NULL
- [ ] `varenavn` - character varying(255), NULL
- [ ] `produsent` - character varying(255), NULL
- [ ] `antall` - int4, NULL
- [ ] `pakningstype` - character varying(255), NULL
- [ ] `pakningsstorrelse` - character varying(255), NULL
- [ ] `pris` - float8, NULL
- [ ] `bestilt_kolli` - int4, NULL
- [ ] `bestilt` - int4, NULL
- [ ] `levert_kolli` - int4, NULL
- [ ] `levert` - int4, NULL
- [ ] `melding` - character varying(255), NULL
- [ ] `strtext` - character varying(10), NULL
- [ ] `strnum` - numeric, NULL
- [ ] `kalkuleringsfaktor` - numeric, NULL

### Column Mapping (old → new):
```
varenummer → 
varenavn → 
produsent → 
antall → 
pakningstype → 
pakningsstorrelse → 
pris → 
bestilt_kolli → 
bestilt → 
levert_kolli → 
levert → 
melding → 
strtext → 
strnum → 
kalkuleringsfaktor → 
```

### Migration Notes:
_____________________________

---

## Table: `tblvaremottak` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `tblvaremottak_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `leverandorid` - int4, NULL
- [ ] `mottakdato` - timestamp, NULL
- [ ] `bestillingsid` - int4, NULL
- [ ] `varenummer` - int4, NULL
- [ ] `varenavn` - character varying(255), NULL
- [ ] `produsent` - character varying(255), NULL
- [ ] `antall_besilt` - int4, NULL
- [ ] `pakningstype` - character varying(255), NULL
- [ ] `pakningsstorrelse` - character varying(255), NULL
- [ ] `pris` - float8, NULL
- [ ] `bestilt_kolli` - int4, NULL
- [ ] `bestilt` - int4, NULL
- [ ] `levert_kolli` - int4, NULL
- [ ] `levert` - int4, NULL
- [ ] `melding` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL

### Column Mapping (old → new):
```
id → 
leverandorid → 
mottakdato → 
bestillingsid → 
varenummer → 
varenavn → 
produsent → 
antall_besilt → 
pakningstype → 
pakningsstorrelse → 
pris → 
bestilt_kolli → 
bestilt → 
levert_kolli → 
levert → 
melding → 
ssma_timestamp → 
```

### Migration Notes:
_____________________________

---

## Table: `test` → (new name: _______________)

### Columns to Remove:

- [ ] `kundeid` - int4, NOT NULL
- [ ] `kundenavn` - character varying(50), NULL
- [ ] `avdeling` - character varying(255), NULL
- [ ] `kontaktid` - int4, NULL
- [ ] `telefonnummer` - character varying(30), NULL
- [ ] `bestillernr` - character varying(255), NULL
- [ ] `lopenr` - int4, NULL
- [ ] `merknad` - text, NULL
- [ ] `adresse` - character varying(50), NULL
- [ ] `postboks` - int4, NULL
- [ ] `postnr` - character varying(4), NULL
- [ ] `sted` - character varying(30), NULL
- [ ] `velgsone` - int4, NULL
- [ ] `leveringsdag` - int4, NULL
- [ ] `kundeinaktiv` - bool, NULL
- [ ] `kundenragresso` - int4, NULL
- [ ] `e_post` - text, NULL
- [ ] `webside` - text, NULL
- [ ] `kundegruppe` - int4, NULL
- [ ] `bestillerselv` - bool, NULL
- [ ] `rute` - int4, NULL
- [ ] `menyinfo` - character varying(255), NULL
- [ ] `ansattid` - int4, NULL
- [ ] `sjaforparute` - int4, NULL
- [ ] `diett` - bool, NULL
- [ ] `menygruppeid` - int4, NULL
- [ ] `utdato` - timestamp, NULL
- [ ] `inndato` - timestamp, NULL
- [ ] `avsluttet` - bool, NULL
- [ ] `eksportkatalog` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL
- [ ] `ordreid` - int4, NULL
- [ ] `expr1` - int4, NULL
- [ ] `expr2` - int4, NULL
- [ ] `expr3` - character varying(50), NULL
- [ ] `ordredato` - timestamp, NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `fakturadato` - timestamp, NULL
- [ ] `sendestil` - character varying(50), NULL
- [ ] `betalingsmate` - int4, NULL
- [ ] `lagerok` - bool, NULL
- [ ] `informasjon` - text, NULL
- [ ] `ordrestatusid` - int4, NULL
- [ ] `fakturaid` - int4, NULL
- [ ] `kansellertdato` - timestamp, NULL
- [ ] `sentbekreftelse` - bool, NULL

### Column Mapping (old → new):
```
kundeid → 
kundenavn → 
avdeling → 
kontaktid → 
telefonnummer → 
bestillernr → 
lopenr → 
merknad → 
adresse → 
postboks → 
postnr → 
sted → 
velgsone → 
leveringsdag → 
kundeinaktiv → 
kundenragresso → 
e_post → 
webside → 
kundegruppe → 
bestillerselv → 
rute → 
menyinfo → 
ansattid → 
sjaforparute → 
diett → 
menygruppeid → 
utdato → 
inndato → 
avsluttet → 
eksportkatalog → 
ssma_timestamp → 
ordreid → 
expr1 → 
expr2 → 
expr3 → 
ordredato → 
leveringsdato → 
fakturadato → 
sendestil → 
betalingsmate → 
lagerok → 
informasjon → 
ordrestatusid → 
fakturaid → 
kansellertdato → 
sentbekreftelse → 
```

### Migration Notes:
_____________________________

---

## Table: `tmpordredetaljer` → (new name: _______________)

### Columns to Remove:

- [ ] `ordreid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `levdato` - timestamp, NULL
- [ ] `pris` - numeric, NOT NULL
- [ ] `antall` - float8, NOT NULL
- [ ] `rabatt` - float4, NULL
- [ ] `ssma_timestamp` - text, NOT NULL
- [ ] `ident` - character varying(255), NULL
- [ ] `unik` - int4, NOT NULL

### Column Mapping (old → new):
```
ordreid → 
produktid → 
levdato → 
pris → 
antall → 
rabatt → 
ssma_timestamp → 
ident → 
unik → 
```

### Migration Notes:
_____________________________

---

## Table: `tmpordredetaljer2` → (new name: _______________)

### Columns to Remove:

- [ ] `ordreid` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `levdato` - timestamp, NULL
- [ ] `pris` - numeric, NOT NULL
- [ ] `antall` - float8, NOT NULL
- [ ] `rabatt` - float4, NULL
- [ ] `ssma_timestamp` - text, NOT NULL
- [ ] `ident` - character varying(255), NULL

### Column Mapping (old → new):
```
ordreid → 
produktid → 
levdato → 
pris → 
antall → 
rabatt → 
ssma_timestamp → 
ident → 
```

### Migration Notes:
_____________________________

---

## Table: `tmpproduksjonsordre` → (new name: _______________)

**Primary Key:** dag, produktid

**Foreign Keys:**
- `produktid` → `tblprodukter(produktid)` [fk_tmpproduksjonsordre_tblprodukter]

**Indexes:**
- `tmpproduksjonsordre_pkey` on (dag, produktid) (UNIQUE)

### Columns to Remove:

- [ ] `dag` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `dato` - timestamp, NOT NULL
- [ ] `antall` - int4, NOT NULL
- [ ] `mengde` - float8, NULL

### Column Mapping (old → new):
```
dag → 
produktid → 
dato → 
antall → 
mengde → 
```

### Migration Notes:
_____________________________

---

## Table: `tmpproduksjonsordredetaljer` → (new name: _______________)

### Columns to Remove:

- [ ] `produksjonskode` - int4, NOT NULL
- [ ] `produktid` - int4, NOT NULL
- [ ] `produktnavn` - character varying(255), NULL
- [ ] `leverandorsproduktnr` - character varying(255), NULL
- [ ] `pris` - numeric, NULL
- [ ] `porsjonsmengde` - int4, NULL
- [ ] `enh` - character varying(255), NULL
- [ ] `totmeng` - numeric, NULL
- [ ] `kostpris` - numeric, NULL
- [ ] `visningsenhet` - character varying(255), NULL
- [ ] `dag` - int2, NULL
- [ ] `antallporsjoner` - int4, NULL

### Column Mapping (old → new):
```
produksjonskode → 
produktid → 
produktnavn → 
leverandorsproduktnr → 
pris → 
porsjonsmengde → 
enh → 
totmeng → 
kostpris → 
visningsenhet → 
dag → 
antallporsjoner → 
```

### Migration Notes:
_____________________________

---

## Table: `tmptblkundersomikkeharbestilt` → (new name: _______________)

### Columns to Remove:

- [ ] `kundeid` - int4, NOT NULL
- [ ] `kundenavn` - character varying(50), NULL
- [ ] `avdeling` - character varying(255), NULL
- [ ] `kontaktid` - int4, NULL
- [ ] `telefonnummer` - character varying(30), NULL
- [ ] `bestillernr` - character varying(255), NULL
- [ ] `lopenr` - int4, NULL
- [ ] `merknad` - text, NULL
- [ ] `adresse` - character varying(50), NULL
- [ ] `postboks` - int4, NULL
- [ ] `postnr` - character varying(4), NULL
- [ ] `sted` - character varying(30), NULL
- [ ] `velgsone` - int4, NULL
- [ ] `leveringsdag` - int4, NULL
- [ ] `kundeinaktiv` - bool, NULL
- [ ] `kundenragresso` - int4, NULL
- [ ] `e_post` - text, NULL
- [ ] `webside` - text, NULL
- [ ] `kundegruppe` - int4, NULL
- [ ] `bestillerselv` - bool, NULL
- [ ] `rute` - int4, NULL
- [ ] `menyinfo` - character varying(255), NULL
- [ ] `ansattid` - int4, NULL
- [ ] `sjaforparute` - int4, NULL
- [ ] `diett` - bool, NULL
- [ ] `menygruppeid` - int4, NULL
- [ ] `utdato` - timestamp, NULL
- [ ] `inndato` - timestamp, NULL
- [ ] `avsluttet` - bool, NULL
- [ ] `eksportkatalog` - character varying(255), NULL
- [ ] `ssma_timestamp` - text, NOT NULL
- [ ] `ordreid` - int4, NULL
- [ ] `expr1` - int4, NULL
- [ ] `expr2` - int4, NULL
- [ ] `expr3` - character varying(50), NULL
- [ ] `ordredato` - timestamp, NULL
- [ ] `leveringsdato` - timestamp, NULL
- [ ] `fakturadato` - timestamp, NULL
- [ ] `sendestil` - character varying(50), NULL
- [ ] `betalingsmate` - int4, NULL
- [ ] `lagerok` - bool, NULL
- [ ] `informasjon` - text, NULL
- [ ] `ordrestatusid` - int4, NULL
- [ ] `fakturaid` - int4, NULL
- [ ] `kansellertdato` - timestamp, NULL
- [ ] `sentbekreftelse` - bool, NULL

### Column Mapping (old → new):
```
kundeid → 
kundenavn → 
avdeling → 
kontaktid → 
telefonnummer → 
bestillernr → 
lopenr → 
merknad → 
adresse → 
postboks → 
postnr → 
sted → 
velgsone → 
leveringsdag → 
kundeinaktiv → 
kundenragresso → 
e_post → 
webside → 
kundegruppe → 
bestillerselv → 
rute → 
menyinfo → 
ansattid → 
sjaforparute → 
diett → 
menygruppeid → 
utdato → 
inndato → 
avsluttet → 
eksportkatalog → 
ssma_timestamp → 
ordreid → 
expr1 → 
expr2 → 
expr3 → 
ordredato → 
leveringsdato → 
fakturadato → 
sendestil → 
betalingsmate → 
lagerok → 
informasjon → 
ordrestatusid → 
fakturaid → 
kansellertdato → 
sentbekreftelse → 
```

### Migration Notes:
_____________________________

---

## Table: `tsttbl2` → (new name: _______________)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL
- [ ] `felt1` - character varying(255), NULL
- [ ] `felt2` - character varying(255), NULL

### Column Mapping (old → new):
```
id → 
felt1 → 
felt2 → 
```

### Migration Notes:
_____________________________

---

## Table: `user` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `user_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - text, NOT NULL
- [ ] `name` - text, NULL
- [ ] `email` - text, NULL
- [ ] `emailverified` - text, NULL
- [ ] `password` - text, NULL
- [ ] `image` - text, NULL
- [ ] `createdat` - timestamp, NULL
- [ ] `updatedat` - timestamp, NULL

### Column Mapping (old → new):
```
id → 
name → 
email → 
emailverified → 
password → 
image → 
createdat → 
updatedat → 
```

### Migration Notes:
_____________________________

---

## Table: `users` → (new name: _______________)

**Primary Key:** id

**Indexes:**
- `idx_users_email` on (email)
- `idx_users_google_id` on (google_id)
- `users_email_key` on (email) (UNIQUE)
- `users_google_id_key` on (google_id) (UNIQUE)
- `users_pkey` on (id) (UNIQUE)

### Columns to Remove:

- [ ] `id` - int4, NOT NULL, DEFAULT: nextval('users_id_seq'::regclass)
- [ ] `email` - character varying(255), NOT NULL
- [ ] `hashed_password` - character varying(255), NULL
- [ ] `full_name` - character varying(255), NOT NULL
- [ ] `is_active` - bool, NULL, DEFAULT: true
- [ ] `is_superuser` - bool, NULL, DEFAULT: false
- [ ] `google_id` - character varying(255), NULL
- [ ] `created_at` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP
- [ ] `updated_at` - timestamp, NULL, DEFAULT: CURRENT_TIMESTAMP

### Column Mapping (old → new):
```
id → 
email → 
hashed_password → 
full_name → 
is_active → 
is_superuser → 
google_id → 
created_at → 
updated_at → 
```

### Migration Notes:
_____________________________

---

## Table: `verificationtoken` → (new name: _______________)

### Columns to Remove:

- [ ] `identifier` - character varying(1000), NOT NULL
- [ ] `token` - character varying(1000), NOT NULL
- [ ] `expires` - timestamp, NOT NULL

### Column Mapping (old → new):
```
identifier → 
token → 
expires → 
```

### Migration Notes:
_____________________________

---

## Migration Strategy

### Step 1: Create New Schema
```sql
-- Create new tables with desired structure
-- Example:
CREATE TABLE new_table_name (
    id SERIAL PRIMARY KEY,
    -- columns from mapping above
);
```

### Step 2: Data Migration Scripts
```sql
-- Transfer data with column mapping
-- Example:
INSERT INTO new_table_name (new_col1, new_col2)
SELECT old_col1, old_col2
FROM old_table_name
WHERE -- any conditions;
```

### Step 3: Update Foreign Keys
```sql
-- Re-establish relationships
ALTER TABLE new_table_name
ADD CONSTRAINT fk_name
FOREIGN KEY (column_name)
REFERENCES other_table(column_name);
```

### Step 4: Verification
- [ ] Row counts match
- [ ] Data integrity verified
- [ ] Foreign key relationships work
- [ ] Application tests pass

### Step 5: Cleanup
```sql
-- Drop old tables
DROP TABLE IF EXISTS old_table_name CASCADE;
```

### Notes:
_____________________________

## Related Tables Analysis

### Tables with Foreign Key Dependencies:

**account:**
  - References: user

**allergens:**
  - References: products

**nutrients:**
  - References: products

**products:**
  - Referenced by: allergens, nutrients

**session:**
  - References: user

**tbl_rpkalkyldetaljer_tblallergener:**
  - References: tblallergener

**tbl_rpkalkyle:**
  - References: tblansatte, tbl_rpkalkylegruppe

**tbl_rpkalkyledetaljer:**
  - References: tblprodukter

**tbl_rpkalkylegruppe:**
  - Referenced by: tbl_rpkalkyle

**tbl_rpproduksjon:**
  - References: tblkunder

**tbl_rpproduksjondetaljer:**
  - References: tblprodukter

**tblallergener:**
  - Referenced by: tblkalkyleallergen, tblprodukt_allergen, tbl_rpkalkyldetaljer_tblallergener

**tblansatte:**
  - Referenced by: tblkunder, tblordrer, tbl_rpkalkyle

**tblbestillinger:**
  - References: tblleverandorer
  - Referenced by: tblbestillingsposter

**tblbestillingsposter:**
  - References: tblbestillinger, tblprodukter

**tblkalkyleallergen:**
  - References: tblallergener

**tblkategorier:**
  - Referenced by: tblprodukter

**tblkontaktpersoner:**
  - References: tblleverandorer

**tblkunder:**
  - References: tblkundgruppe, tblkunder, tblsone, tblansatte, tblleveringsdag, tblruteplan
  - Referenced by: tblkunder, tbltmpordrebestillingsykehjem, tblordrer, tbl_rpproduksjon

**tblkundgruppe:**
  - Referenced by: tblkunder, tblmva_kundekategori

**tbllagertransaksjoner:**
  - References: tbllagertransaksjonstyper, tblprodukter

**tbllagertransaksjonstyper:**
  - Referenced by: tbllagertransaksjoner

**tbllevbestillinger:**
  - References: tbllevbestillingshode

**tbllevbestillingshode:**
  - References: tblleverandorer
  - Referenced by: tbllevbestillinger

**tblleverandorer:**
  - Referenced by: tblkontaktpersoner, tblbestillinger, tbllevbestillingshode, tblprodukter

**tblleveringsdag:**
  - Referenced by: tblkunder

**tblmeny:**
  - Referenced by: tblperiodemeny

**tblmva:**
  - Referenced by: tblmva_kundekategori

**tblmva_kundekategori:**
  - References: tblmva, tblkundgruppe

**tblordredetaljer:**
  - References: tblordrer, tblprodukter

**tblordrer:**
  - References: tblkunder, tblordrestatus, tblansatte
  - Referenced by: tblordredetaljer

**tblordrestatus:**
  - Referenced by: tblordrer

**tblperiode:**
  - Referenced by: tblperiodemeny

**tblperiodemeny:**
  - References: tblperiode, tblmeny

**tblprodukt_allergen:**
  - References: tblallergener, tblprodukter

**tblprodukter:**
  - References: tblleverandorer, tblkategorier
  - Referenced by: tblordredetaljer, tbl_rpproduksjondetaljer, tbllagertransaksjoner, tblbestillingsposter, tmpproduksjonsordre, tblprodukt_allergen, tbl_rpkalkyledetaljer

**tblruteplan:**
  - Referenced by: tblkunder

**tblsone:**
  - Referenced by: tblkunder

**tbltmpordrebestillingsykehjem:**
  - References: tblkunder

**tmpproduksjonsordre:**
  - References: tblprodukter

**user:**
  - Referenced by: account, session
