import csv
import os
import sqlite3

def load_and_clean(filepath):
    cleaned_rows = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean column names (lowercase, replace spaces)
            cleaned_row = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in row.items()}
            if all(cleaned_row.values()):  # Drop rows with missing values
                cleaned_rows.append(cleaned_row)
    return cleaned_rows

def save_cleaned_csv(rows, output_path):
    if not rows:
        print("❌ No data to save.")
        return

    fieldnames = rows[0].keys()
    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Cleaned CSV saved to {output_path}")

def save_to_sqlite(rows, db_path="data.db"):
    if not rows:
        print("❌ No data to save to DB.")
        return

    fieldnames = rows[0].keys()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    columns = ', '.join([f"{field} TEXT" for field in fieldnames])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS software_defects ({columns})")

    # Insert rows
    placeholders = ', '.join(['?' for _ in fieldnames])
    cursor.executemany(
        f"INSERT INTO software_defects ({', '.join(fieldnames)}) VALUES ({placeholders})",
        [tuple(row.values()) for row in rows]
    )

    conn.commit()
    conn.close()
    print(f"✅ Data saved to SQLite DB: {db_path}")

if __name__ == "__main__":
    raw_path = os.path.join("datasets", "software_defects.csv")
    clean_path = os.path.join("datasets", "cleaned_software_defects.csv")

    rows = load_and_clean(raw_path)
    save_cleaned_csv(rows, clean_path)
    save_to_sqlite(rows)
