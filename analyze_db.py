import sqlite3
import json

conn = sqlite3.connect('agroguard.db', timeout=10.0)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("=" * 80)
print("AGROGUARD DATABASE ANALYSIS")
print("=" * 80)
print()

db_structure = {}

for (table_name,) in tables:
    print(f"\n{'='*80}")
    print(f"TABLE: {table_name}")
    print('='*80)
    
    # Get table info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    print(f"Row Count: {row_count}")
    print()
    print("Columns:")
    print("-" * 80)
    
    table_cols = []
    for col in columns:
        cid, name, col_type, not_null, default_val, pk = col
        pk_marker = " [PRIMARY KEY]" if pk else ""
        not_null_marker = " NOT NULL" if not_null else ""
        default_marker = f" DEFAULT {default_val}" if default_val else ""
        
        print(f"  {name:25} {col_type:15} {pk_marker}{not_null_marker}{default_marker}")
        table_cols.append({
            'name': name,
            'type': col_type,
            'is_pk': bool(pk),
            'not_null': bool(not_null)
        })
    
    # Get foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    fks = cursor.fetchall()
    
    if fks:
        print()
        print("Foreign Keys:")
        print("-" * 80)
        for fk in fks:
            fk_id, seq, ref_table, from_col, to_col, on_update, on_delete, match = fk
            print(f"  {from_col} → {ref_table}({to_col})")
    
    # Get sample data (first 3 rows)
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    sample_rows = cursor.fetchall()
    
    if sample_rows:
        print()
        print("Sample Data (first 3 rows):")
        print("-" * 80)
        col_names = [desc[0] for desc in cursor.description]
        
        for i, row in enumerate(sample_rows, 1):
            print(f"  Row {i}:")
            for col_name, value in zip(col_names, row):
                display_value = str(value)[:50] if value else "NULL"
                print(f"    {col_name}: {display_value}")
    
    db_structure[table_name] = {
        'columns': table_cols,
        'row_count': row_count,
        'foreign_keys': [{'from': fk[3], 'to_table': fk[2], 'to_col': fk[4]} for fk in fks]
    }

conn.close()

print()
print("=" * 80)
print("DATABASE RELATIONSHIPS SUMMARY")
print("=" * 80)
print()

for table_name, info in db_structure.items():
    if info['foreign_keys']:
        print(f"{table_name}:")
        for fk in info['foreign_keys']:
            print(f"  └─→ {fk['to_table']}.{fk['to_col']} (via {fk['from']})")
        print()

print()
print("=" * 80)
print("CARDINALITY ANALYSIS")
print("=" * 80)
print()

print("FARMERS (1) ────< (N) SCANS")
print("  One farmer can have multiple scans")
print()

print("FARMERS (1) ────< (N) FARMER_SUPPORT_REQUESTS")
print("  One farmer can submit multiple support requests")
print()

print("AEO (1) ────< (N) ALERTS")
print("  One AEO can send multiple alerts")
print()

print("AEO (1) ────< (N) SUPPORT_TICKETS")
print("  One AEO can submit multiple support tickets")
print()

print("SUPERADMIN (1) ────< (N) AUDIT_LOG")
print("  One superadmin performs multiple auditable actions")
print()

print()
print("=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
