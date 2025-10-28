import pandas as pd
import sqlite3
import os

# --- CONFIG ---
DB_PATH = "agriculture_data.db"  # SQLite database file
CROP_CSV = "commercial_crops__csv.csv"
RAINFALL_CSV = "rainfall__csv.csv"

# --- STEP 1: Check CSVs ---
if not os.path.exists(CROP_CSV) or not os.path.exists(RAINFALL_CSV):
    print("❌ One or both CSV files not found in project folder.")
    print(f"Expected files:\n- {CROP_CSV}\n- {RAINFALL_CSV}")
    exit()

print("✅ Found CSV files.")

# --- STEP 2: Load CSV files ---
try:
    df_crops = pd.read_csv(CROP_CSV)
    df_rain = pd.read_csv(RAINFALL_CSV)
    print("✅ CSV files loaded successfully.")
except Exception as e:
    print("❌ Error loading CSV files:", e)
    exit()

# --- STEP 3: Connect to SQLite ---
conn = sqlite3.connect(DB_PATH)
print(f"✅ Connected to SQLite database: {DB_PATH}")

# --- STEP 4: Store data into tables ---
df_crops.to_sql("commercial_crops", conn, if_exists="replace", index=False)
df_rain.to_sql("rainfall", conn, if_exists="replace", index=False)
print("✅ Data stored in SQLite database.")

# --- STEP 5: Test the data ---
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM commercial_crops;")
crop_rows = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM rainfall;")
rain_rows = cursor.fetchone()[0]

print(f"🌾 commercial_crops rows: {crop_rows}")
print(f"🌧️ rainfall rows: {rain_rows}")

conn.close()
print("✅ Phase 1 complete — data successfully saved to agriculture_data.db!")
