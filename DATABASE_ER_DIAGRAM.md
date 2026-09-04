# AgroGuard Database - Entity Relationship Diagram

**Database:** agroguard.db (SQLite 3.x)  
**Analysis Date:** January 2026  
**Total Tables:** 10  
**Total Records:** 422+

---

## Database Overview

| Table | Records | Purpose |
|-------|---------|---------|
| **farmers** | 18 | Farmer accounts and profiles |
| **scans** | 359 | Crop disease scan records |
| **aeo** | 2 | Agricultural Extension Officers |
| **alerts** | 10 | Broadcast alerts to farmers |
| **superadmin** | 2 | System administrators |
| **audit_log** | 16 | Action audit trail |
| **support_tickets** | 4 | AEO support requests |
| **farmer_support_requests** | 1 | Farmer support requests |
| **users** | 4 | Legacy officer accounts |
| **sqlite_sequence** | 8 | Auto-increment tracking |

---

## Complete Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ FARMERS                                                          │
│ Purpose: Farmer registration and profile management             │
├─────────────────────────────────────────────────────────────────┤
│ PK  device_id              TEXT (Unique device identifier)      │
│     name                   TEXT (Farmer name)                    │
│     phone                  TEXT (Phone number)                   │
│     ghana_card             TEXT (Ghana Card ID - optional)       │
│     district               TEXT (Location district)              │
│     crops                  TEXT (Crops grown)                    │
│     registration_method    TEXT (How registered)                 │
│     registered_by          TEXT (Who registered them)            │
│     first_seen             TIMESTAMP (First app use)             │
│     last_seen              TIMESTAMP (Last activity)             │
└─────────────────────────────────────────────────────────────────┘
              │
              │ 1:N (One farmer, many scans)
              ▼
┌─────────────────────────────────────────────────────────────────┐
│ SCANS                                                            │
│ Purpose: Disease detection scan history                         │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│ FK  farmer_device_id       TEXT → FARMERS(device_id)            │
│     crop                   TEXT (Corn, Rice, etc.)               │
│     disease                TEXT (Disease detected)               │
│     confidence             REAL (0.0 - 1.0 AI confidence)        │
│     location               TEXT (GPS location name)              │
│     status                 TEXT (Healthy, High Risk, etc.)       │
│     segment_id             TEXT (GPS segment for deduplication)  │
│     timestamp              TIMESTAMP (When scan occurred)        │
└─────────────────────────────────────────────────────────────────┘

              ┌───────────────────┐
              │ FARMERS           │
              │ 1:N relationship  │
              └───────┬───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ FARMER_SUPPORT_REQUESTS                                          │
│ Purpose: Farmers submit support/help requests                   │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│ FK  farmer_device_id       TEXT → FARMERS(device_id)            │
│     farmer_name            TEXT (Cached from farmer profile)     │
│     farmer_phone           TEXT (Cached contact)                 │
│     category               TEXT (technical, disease, other)      │
│     subject                TEXT (Brief title)                    │
│     message                TEXT (Full description)               │
│     status                 TEXT (pending, resolved)              │
│     priority               TEXT (normal, urgent)                 │
│     created_at             DATETIME (Submission time)            │
│     resolved_at            DATETIME (Resolution time)            │
│ FK  resolved_by            INTEGER → SUPERADMIN(id)             │
│     admin_notes            TEXT (Admin resolution notes)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ AEO (Agricultural Extension Officers)                            │
│ Purpose: Field officer accounts with authentication             │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│ UK  staff_id               TEXT UNIQUE (AEO-XXXX format)         │
│ UK  ghana_card             TEXT UNIQUE (GHA-XXXXXXXXX-X)         │
│ UK  phone                  TEXT UNIQUE (Contact number)          │
│     name                   TEXT (Full name)                      │
│     email                  TEXT (Email address - optional)       │
│     district               TEXT (Assignment district)            │
│     region                 TEXT (Assignment region)              │
│     hashed_password        TEXT (Bcrypt hash)                    │
│     must_change_password   INTEGER (1=force change on login)     │
│     is_active              INTEGER (1=active, 0=disabled)        │
│     biometric_id           TEXT (Biometric identifier)           │
│     biometric_public_key   TEXT (Public key for biometric)       │
│     profile_completed      INTEGER (1=profile filled)            │
│     last_login             TIMESTAMP (Last login time)           │
│     profile_picture        TEXT (Base64 image data)              │
└─────────────────────────────────────────────────────────────────┘
              │
              │ 1:N (One AEO, many alerts)
              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ALERTS                                                           │
│ Purpose: AEO broadcasts alerts to farmers                       │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│     alert_type             TEXT (critical, weather, training)    │
│     title                  TEXT (Alert headline)                 │
│     message                TEXT (Full alert message)             │
│     priority               TEXT (high, medium, low)              │
│     target_type            TEXT (all, region, phone)             │
│     target_audience        TEXT (Who receives it)                │
│     target_phone           TEXT (Specific phones if targeted)    │
│     district               TEXT (District if location-targeted)  │
│ FK  sent_by                INTEGER → AEO(id)                     │
│     recipient_count        INTEGER (Number of recipients)        │
│     created_at             DATETIME (When sent)                  │
└─────────────────────────────────────────────────────────────────┘

              ┌───────────────────┐
              │ AEO               │
              │ 1:N relationship  │
              └───────┬───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ SUPPORT_TICKETS                                                  │
│ Purpose: AEOs submit support tickets to admins                  │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│     category               TEXT (technical, data, training)      │
│     priority               TEXT (low, medium, high, critical)    │
│     subject                TEXT (Ticket title)                   │
│     description            TEXT (Full description)               │
│     contact                TEXT (AEO contact for follow-up)      │
│ FK  submitted_by           INTEGER → AEO(id)                     │
│     status                 TEXT (open, in_progress, resolved)    │
│     created_at             DATETIME (Submission time)            │
│     resolved_at            DATETIME (Resolution time)            │
│     resolved_by            INTEGER (Admin who resolved)          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SUPERADMIN                                                       │
│ Purpose: System administrators with full access                 │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│ UK  username               TEXT UNIQUE (Login username)          │
│     hashed_password        TEXT (Bcrypt hash)                    │
│     full_name              TEXT (Full name)                      │
│     is_active              INTEGER (1=active, 0=disabled)        │
│     created_at             TIMESTAMP (Account creation)          │
└─────────────────────────────────────────────────────────────────┘
              │
              │ 1:N (One admin, many actions)
              ▼
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT_LOG                                                        │
│ Purpose: Track all admin/system actions for accountability      │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│     action                 TEXT (create_aeo, send_alert, etc.)   │
│     entity                 TEXT (aeo, alert, farmer)             │
│     entity_id              INTEGER (ID of affected record)       │
│     performed_by           INTEGER (Admin/AEO who did action)    │
│     timestamp              DATETIME (When action occurred)       │
│     details                TEXT (Additional context)             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ USERS (Legacy)                                                   │
│ Purpose: Original officer accounts (pre-AEO system)             │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                     INTEGER AUTO_INCREMENT                │
│     username               TEXT UNIQUE (Login username)          │
│     password_hash          TEXT (Bcrypt hash)                    │
│     role                   TEXT (officer - default)              │
│     created_at             TIMESTAMP (Account creation)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Relationship Summary

### Primary Relationships

```
FARMERS (1) ────< (N) SCANS
├─ Relationship: One-to-Many
├─ Foreign Key: scans.farmer_device_id → farmers.device_id
├─ Purpose: Track all disease scans per farmer
└─ Cascade: None (soft delete recommended)

FARMERS (1) ────< (N) FARMER_SUPPORT_REQUESTS
├─ Relationship: One-to-Many
├─ Foreign Key: farmer_support_requests.farmer_device_id → farmers.device_id
├─ Purpose: Track support requests from farmers
└─ Cascade: None (preserve support history)

AEO (1) ────< (N) ALERTS
├─ Relationship: One-to-Many
├─ Foreign Key: alerts.sent_by → aeo.id
├─ Purpose: Track which AEO sent which alerts
└─ Cascade: None (preserve alert history)

AEO (1) ────< (N) SUPPORT_TICKETS
├─ Relationship: One-to-Many
├─ Foreign Key: support_tickets.submitted_by → aeo.id
├─ Purpose: Track support tickets from AEOs
└─ Cascade: None (preserve ticket history)

SUPERADMIN (1) ────< (N) AUDIT_LOG
├─ Relationship: One-to-Many (implicit)
├─ Foreign Key: audit_log.performed_by (references admin ID)
├─ Purpose: Track all admin actions for accountability
└─ Cascade: None (never delete audit logs)

SUPERADMIN (1) ────< (N) FARMER_SUPPORT_REQUESTS (resolved_by)
├─ Relationship: One-to-Many
├─ Foreign Key: farmer_support_requests.resolved_by → superadmin.id
├─ Purpose: Track which admin resolved farmer requests
└─ Cascade: None (preserve resolution history)
```

---

## Key Insights

### Data Volume Analysis

| Entity | Current Count | Growth Rate | Notes |
|--------|---------------|-------------|-------|
| **Scans** | 359 | High | Primary transaction table |
| **Farmers** | 18 | Medium | Growing with user adoption |
| **Alerts** | 10 | Low | Periodic broadcasts |
| **Audit Log** | 16 | Medium | Tracks all admin actions |
| **Support Tickets** | 4 | Low | AEO support requests |
| **Farmer Requests** | 1 | Low | Farmer help requests |

### Unique Constraints

**FARMERS:**
- device_id (Primary Key) - Unique per device/browser

**AEO:**
- staff_id (Unique) - AEO-XXXX format
- ghana_card (Unique) - GHA-XXXXXXXXX-X format
- phone (Unique) - Contact number

**SUPERADMIN:**
- username (Unique) - Login credential

### Indexing Opportunities

**High-Value Indexes:**
- `scans.farmer_device_id` - Frequently joined
- `scans.timestamp` - Time-based queries
- `scans.disease` - Disease distribution analysis
- `alerts.sent_by` - AEO activity tracking
- `farmers.phone` - Contact lookup

**Composite Indexes:**
- `scans(farmer_device_id, timestamp)` - Farmer history queries
- `scans(disease, status)` - Disease outbreak analysis
- `alerts(sent_by, created_at)` - AEO alert history

---

## Data Integrity Rules

### Referential Integrity

✅ **Enforced:**
- scans.farmer_device_id → farmers.device_id
- alerts.sent_by → aeo.id
- support_tickets.submitted_by → aeo.id
- farmer_support_requests.farmer_device_id → farmers.device_id
- farmer_support_requests.resolved_by → superadmin.id

❌ **Not Enforced (Soft References):**
- audit_log.performed_by (can be AEO or Superadmin ID)
- support_tickets.resolved_by (optional, admin ID)

### Cascade Rules

**Current Behavior:**
- No CASCADE DELETE configured
- All foreign keys use default (RESTRICT)
- Deletions require manual cleanup

**Recommendation:**
- Keep current behavior for audit trail
- Implement soft deletes (is_deleted flag)
- Archive old data instead of deletion

---

## Sample Data Patterns

### Farmer Device IDs
```
Format: did_[random9chars]
Examples:
  - did_a3awqytn3
  - did_vh635i9r2
  - did_qmz4rdzxz
```

### AEO Staff IDs
```
Format: AEO-[4-5digits]
Examples:
  - AEO-02345
  - AEO-1234
```

### Ghana Card IDs
```
Format: GHA-[8-9digits]-[1digit]
Examples:
  - GHA-71888591-0
  - GHA-71888591-1
```

### Scan Disease Values
```
Format: [Crop]___[Disease_State]
Examples:
  - Corn___Healthy
  - Corn___Common_Rust
  - Corn___Gray_Leaf_Spot
  - Corn___Northern_Leaf_Blight
```

### GPS Segment IDs
```
Format: [latitude]_[longitude] (rounded to 4 decimals)
Purpose: Geospatial deduplication
Example: 4.9204_-1.7636
```

---

## Database Statistics

### Storage Information
- Database File: agroguard.db
- Estimated Size: ~2-5 MB
- Schema Version: SQLite 3.x
- Foreign Keys: ENABLED

### Record Distribution
```
Total Records: 422+
├─ Scans: 85.1% (359)
├─ Farmers: 4.3% (18)
├─ Audit Log: 3.8% (16)
├─ Alerts: 2.4% (10)
├─ Support Tickets: 0.9% (4)
├─ Users: 0.9% (4)
├─ AEO: 0.5% (2)
├─ Superadmin: 0.5% (2)
└─ Farmer Requests: 0.2% (1)
```

### Growth Projections
- **Scans:** ~50-100 per day (active season)
- **Farmers:** ~2-5 new per week
- **Alerts:** ~1-2 per week
- **Support:** ~1-2 per week

---

## Security & Privacy Notes

### Password Storage
- ✅ All passwords use bcrypt hashing
- ✅ Cost factor: 12 (2^12 = 4096 iterations)
- ✅ Salted automatically by bcrypt

### Sensitive Fields
- `hashed_password` (all user tables)
- `biometric_id`, `biometric_public_key` (AEO table)
- `phone` (farmers, AEO)
- `ghana_card` (farmers, AEO)

### Data Minimization
- ✅ Farmer registration requires only: device_id, name, phone
- ✅ Optional fields: ghana_card, district, crops
- ✅ No email collection for farmers (privacy-first)

---

## Schema Evolution Notes

### Added Fields (Post-Launch)
**farmers table:**
- ghana_card, district, crops
- registration_method, registered_by

**scans table:**
- segment_id (for GPS deduplication)

**aeo table:**
- email, district, region
- biometric_id, biometric_public_key
- profile_completed, last_login, profile_picture

**alerts table:**
- title, priority, target_type, target_phone

### Migration Strategy
- Safe column additions using `ALTER TABLE`
- Try/except blocks in database.py for backwards compatibility
- No data loss during schema updates

---

## Query Performance Considerations

### Frequent Queries
1. Dashboard stats (joins farmers, scans, aeo)
2. Recent scans (ORDER BY timestamp DESC LIMIT 10)
3. Disease distribution (GROUP BY disease)
4. Farmer scan history (WHERE farmer_device_id = ?)
5. Alert recipients (complex filtering by target_type)

### Optimization Opportunities
- Add index on `scans.timestamp`
- Add index on `scans.disease`
- Consider materialized view for dashboard stats
- Cache disease distribution counts

---

*Database analysis complete - No changes made to database*
